# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.method_types.method_type.py
Contains the MethodType class, a child and extension of AccessMethod. MethodType
is further extended into separate classes for each of the different supported
access types, or schemes (gs, https, htsget, etc.). MethodType contains methods
that are common to all specific Access Types/Schemes. 
"""

import os
import ga4gh.drs.config.globals as gl
from ga4gh.drs.definitions.access_method import AccessMethod
from ga4gh.drs.exceptions.drs_exceptions import DownloadSubmethodException
from tqdm import tqdm

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

        def wrapper(method_type_obj):
            """Inner wrapper function

            Arguments:
                method_type_obj (MethodType): MethodType object

            Returns:
                (int): status of download submethod
            """
            
            # initialize submethod status as 'STARTED'
            submethod_status = gl.DownloadStatus.STARTED

            # set up the write config, including output file name, path,
            # file size, and chunk size
            output_file_path = method_type_obj.get_output_file_path()
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

                # if AccessMethod already has access url, execute the download 
                # submethod, otherwise get the access url from the access id,
                # then execute submethod
                # if neither is submitted, raise an error
                # catch any errors, setting this submethod status to FAILED 
                if method_type_obj.access_id:
                    pass
                elif method_type_obj.access_url:
                    submethod_func(method_type_obj, write_config)
                else:
                    raise DownloadSubmethodException(
                        "Neither access_url or access_id is specified")
                submethod_status = gl.DownloadStatus.COMPLETED
            except DownloadSubmethodException as e:
                submethod_status = gl.DownloadStatus.FAILED
                gl.logger.error(str(e))
            except Exception as e:
                submethod_status = gl.DownloadStatus.FAILED
                gl.logger.error(str(e))
            
            return submethod_status
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
        download_status (int): current status of DRSObject byte download
        download_submethods (list): multiple methods to attempt byte download
    """

    def __init__(self, json, drs_obj):
        """Instantiates a MethodType object

        Arguments:
            json (dict): parsed AccessMethod JSON, used to set other attributes
            drs_obj (DRSObject): reference to parent DRSObject object
        """

        super(MethodType, self).__init__(json, drs_obj)
        self.data_accessor = None
        self.download_status = gl.DownloadStatus.NOT_STARTED
        self.download_submethods = []

    def download_retry_loop(self):
        """Execute each download submethod until one downloads object bytes

        For each method in download_submethods, execute the method, which 
        attempts to download the file. If it succeeds, the retry loop is broken.
        If not, the next method is attempted. If all methods are tried and there
        is no success, the status of this MethodType is set to FAILED
        """

        self.download_status = gl.DownloadStatus.STARTED
        
        submethod_status = gl.DownloadStatus.NOT_STARTED
        for submethod in self.download_submethods:
            if submethod_status != gl.DownloadStatus.COMPLETED:
                submethod_status = gl.DownloadStatus.STARTED
                submethod_status = submethod()
        
        self.download_status = submethod_status
    
    def set_data_accessor(self, data_accessor):
        """Set MethodType data accessor

        Arguments:
            data_accessor (DataAccessor): reference to DataAccessor
        """

        self.data_accessor = data_accessor
    
    def get_output_file_path(self):
        """Get the path of download file destination on local machine

        Returns:
            (str): destination of downloaded file
        """

        fname = self.drs_obj.name if self.drs_obj.name else self.drs_obj.id
        dirname = self.data_accessor.cli_kwargs["output_dir"]
        if dirname:
            fname = os.path.join(dirname, fname)
        return fname

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
