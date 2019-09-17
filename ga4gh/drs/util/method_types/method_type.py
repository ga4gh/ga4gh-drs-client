# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.method_types.method_type.py
Contains the MethodType class, a child and extension of AccessMethod. MethodType
is further extended into separate classes for each of the different supported
access types, or schemes (gs, https, htsget, etc.). MethodType contains methods
that are common to all specific Access Types/Schemes. 
"""

# import ga4gh.drs.config.constants as c
import ga4gh.drs.config.download_status as ds
import ga4gh.drs.config.logger as l
import os
import requests
from functools import wraps
from ga4gh.drs.definitions.access_method import AccessMethod
from ga4gh.drs.definitions.access_url import AccessUrl
from ga4gh.drs.exceptions.drs_exceptions import DownloadSubmethodException
from ga4gh.drs.routes.route_fetch_bytes import RouteFetchBytes
from ga4gh.drs.util.functions import http
from tqdm import tqdm
from urllib.parse import urlparse

def DownloadSubmethod():
    """Get a decorator function for universal file download template

    This function yields a decorator. The decorator function serves as a 
    wrapper for other download submethods. the decorator will set up 
    write config details, and will check if the AccessMethod has an access id
    or access url, executing the download submethod as appropriate.

    Returns:
        (function): outer decorator function
    
    """

    def decorator_func(submethod_func):
        """Outer decorator function

        Arguments:
            submethod_func (function): download submethod to be executed in the
                wrapper

        Returns:
            (function): Inner wrapper function
        """

        @wraps(submethod_func)
        def wrapper(method_type_obj):
            """Inner wrapper function

            Arguments:
                method_type_obj (MethodType): MethodType object

            Returns:
                (int): status of download submethod
            """
            
            # initialize submethod status as 'STARTED'
            submethod_status = ds.DownloadStatus.STARTED
            err_message = None

            # set up the write config, including output file name, path,
            # file size, and chunk size
            data_accessor = method_type_obj.data_accessor
            output_file_path = data_accessor.get_output_file_path()
            output_file_name = os.path.basename(output_file_path)
            output_file = open(output_file_path, "wb")
            chunk_size = 8192
            file_size_bytes = method_type_obj.drs_obj.size
            write_config = {"opath": output_file_path, 
                "oname": output_file_name, "ofile": output_file, 
                "csize": chunk_size, "fsize": file_size_bytes,
                "tchunks": file_size_bytes / chunk_size
            }
            
            try:
                # Access Id has already been converted to Access Url from the
                # DRSObject constructor.
                # execute download submethod based on url scheme
                submethod_func(method_type_obj, write_config)
                submethod_status = ds.DownloadStatus.COMPLETED
            except DownloadSubmethodException as e:
                submethod_status = ds.DownloadStatus.FAILED
                err_message = str(e)
            except Exception as e:
                submethod_status = ds.DownloadStatus.FAILED
                err_message = str(e)
            
            return [submethod_status, err_message]
        return wrapper
    return decorator_func

class MethodType(AccessMethod):
    """Abstract parent of scheme-specific Access Method Types

    Each subclass of MethodType should have 1 or more methods defined and 
    referenced in download_submethods. These methods are called in sequence
    in the download_retry_loop, until one method successfully downloads the
    complete file.

    Attributes:
        data_accessor (DataAccessor): DataAccessor managing this MethodType
        cli_kwargs (dict): command-line arguments/options
        download_status (int): current status of DRSObject byte download
        download_submethods (list): multiple methods to attempt byte download
    """

    def __init__(self, json, drs_obj, cli_kwargs):
        """Instantiates a MethodType object

        Arguments:
            json (dict): parsed AccessMethod JSON, used to set other attributes
            drs_obj (DRSObject): reference to parent DRSObject object
            cli_kwargs (dict): command-line arguments/options
        """

        super(MethodType, self).__init__(json, drs_obj)
        self.data_accessor = None
        self.cli_kwargs = cli_kwargs
        self.download_status = ds.DownloadStatus.NOT_STARTED
        self.download_submethods = []

    def download_retry_loop(self):
        """Execute each download submethod until one downloads object bytes

        For each method in download_submethods, execute the method, which 
        attempts to download the file. If it succeeds, the retry loop is broken.
        If not, the next method is attempted. If all methods are tried and there
        is no success, the status of this MethodType is set to FAILED
        """

        start_msg_template = "{objid}: '{scheme}' starting download attempt " \
            "by submethod {method}"
        end_msg_template = "{objid}: '{scheme}' finished download attempt " \
            + "by submethod {method}. Status: {status}"
        err_msg_template = end_msg_template + ". Message: {message}"

        self.download_status = ds.DownloadStatus.STARTED
        submethod_status = ds.DownloadStatus.NOT_STARTED
        scheme = urlparse(self.access_url.url).scheme
        for submethod in self.download_submethods:
            if submethod_status != ds.DownloadStatus.COMPLETED:
                start_msg = start_msg_template.format(objid=self.drs_obj.id,
                    scheme=scheme, method=submethod.__name__)
                l.logger.debug(start_msg)
                
                submethod_status = ds.DownloadStatus.STARTED
                submethod_status, err_message = submethod()

                end_msg_d = {
                    "objid": self.drs_obj.id, "scheme": scheme,
                    "method": submethod.__name__,
                    "status": ds.DOWNLOAD_STATUS[submethod_status]
                }
                end_msg = ""
                if not err_message:
                    end_msg = end_msg_template.format(**end_msg_d)
                else:
                    end_msg_d["message"] = err_message
                    end_msg = err_msg_template.format(**end_msg_d)
                l.logger.debug(end_msg)

        self.download_status = submethod_status
    
    def set_data_accessor(self, data_accessor):
        """Set MethodType data accessor

        Arguments:
            data_accessor (DataAccessor): reference to DataAccessor
        """

        self.data_accessor = data_accessor

    def download_write_stream(self, iterator_func, write_config):
        """Write the downloading file as a stream to local output file

        As the DRS blob file is downloading, open an output file stream,
        writing chunks of the file to the destination. Provides a download 
        progress bar that appears on the terminal (if user has not specified
        'silent')

        Arguments:
            iterator_func (function): an iterator that yields chunks of the 
                downloading file
            write_config (dict): output file, size, etc. parameters
        """

        # unpack the write_config dictionary, which contains output file name,
        # path, chunk size, file size, and total chunks
        oname, ofile, csize, fsize, tchunks = [write_config[k] for k in [
            "oname", "ofile", "csize", "fsize", "tchunks"]]

        silent = self.data_accessor.cli_kwargs["silent"]
        # supply chunk size to the iterator function
        iterator = iterator_func(chunk_size=csize)

        # if user has specified 'silent', do not wrap iterator function with
        # progress bar, otherwise include progress bar
        if not silent:
            iterator = tqdm(iterator, total=tchunks, desc=oname)
        # write each yielded chunk to the output file
        for chunk in iterator:
            ofile.write(chunk)
        ofile.close()

    def __download_by_requests_package(self, url, write_config):
        """Download submethod template, download object by Python Requests

        Multiple url scheme subclasses involve downloading an object using
        the Python requests package. This function serves as a template for 
        all subclasses implementing such download submethods. The request is
        made, and if the status code is successful, the iterator function is 
        passed to the write stream. Otherwise, an exception is raised, setting
        submethod status to FAILED.

        Arguments:
            url (str): request url
        """

        headers = {}
        verify = not self.cli_kwargs["suppress_ssl_verify"]
        if self.access_url.headers:
            if len(self.access_url.headers) > 0:
                headers = http.header_list_to_dict(self.access_url.headers)
            else:
                headers = self.data_accessor.headers
        else:
            headers = self.data_accessor.headers

        with requests.get(url, headers=headers, verify=verify, 
            stream=True) as r:
            if http.is_error(r.status_code):
                raise DownloadSubmethodException(
                    "Request yielded " + str(r.status_code) + " error code "
                    + "response"
                )
            iterator_func = r.iter_content
            self.download_write_stream(iterator_func, write_config)

    def __download_by_cli_subprocess(self, foo):
        pass
