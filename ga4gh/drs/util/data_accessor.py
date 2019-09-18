# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.data_accessor.py
Contains the DataAccessor class, which manages the byte download of a single 
DRSObject. Attempts to download the full file by all available access methods
until the download has completed successfully.
"""

import ga4gh.drs.config.checksum_status as cs
import ga4gh.drs.config.download_status as ds
import os
from ga4gh.drs.config.global_state import GLOBALSTATE
from ga4gh.drs.definitions.checksum import Checksum
from urllib.parse import urlparse

class DataAccessor(object):
    """Manages the byte download of a single DRSObject

    Attributes:
        drs_obj (DRSObject): reference to DRSObject to be downloaded
        cli_kwargs (dict): cli args/options
        logger (Logger): logger
        headers (dict): headers to be supplied to download request
        download_status (int): current status of the file download
        checksum_status (int): current status of checksum validation
        checksum_algo (str): name of algorithm used in checksum validation
        checksum_exp (str): expected checksum digest value given the algorithm
        checksum_obs (str): observed checksum digest value given the algorithm
        logger (Logger): global logger
    """
    
    def __init__(self, drs_obj, headers):
        """Instantiates a DataAccessor object

        Arguments:
            drs_obj (DRSObject): reference to DRSObject
            headers (dict): headers to be supplied to download request
        """

        self.drs_obj = drs_obj
        self.cli_kwargs = GLOBALSTATE.get_prop("cli")
        self.logger = GLOBALSTATE.get_prop("logger")
        self.headers = headers
        self.download_status = ds.DownloadStatus.NOT_STARTED
        self.checksum_status = cs.ChecksumStatus.NOT_APPLICABLE
        self.checksum_algo = "N/A"
        self.checksum_exp = "N/A"
        self.checksum_obs = "N/A"
    
    def download(self):
        """Attempt byte download by all access methods

        Since a DRSObject can contain multiple AccessMethods, this method
        will attempt to download the file by each AccessMethod until the 
        download successfully completes. If the file could not be downloaded 
        by an AccessMethod, then the DataAccessor will try the next 
        AccessMethod. If all AccessMethod options are exhausted, then the
        download status is set to failed.
        """

        # download by any access method has started
        self.download_status = ds.DownloadStatus.STARTED

        no_method_msg_template = "{objid} has no valid access methods with " \
            + "which to attempt download. Status: {status}"
        start_msg_template = "{objid}: attempting download by '{scheme}' scheme"
        end_msg_template = "{objid}: finished download attempt by '{scheme}' " \
            + "scheme. Status: {status}"

        # for each access method, execute the 'download_retry_loop' function,
        # if the access method is successful, then this loop will break
        # if not, the next access method is attempted
        # if an access method is successful, the data accessor's download 
        # status is set to 'COMPLETED'
        # if all access methods are exhausted without success, the data
        # accessor's download status is set to 'FAILED'
        access_method_status = ds.DownloadStatus.NOT_STARTED
        if len(self.drs_obj.access_methods) < 1:
            access_method_status = ds.DownloadStatus.FAILED
            msg = no_method_msg_template.format(objid=self.drs_obj.id,
                status=ds.DOWNLOAD_STATUS[access_method_status])
            self.logger.debug(msg)

        for access_method in self.drs_obj.access_methods:
            scheme = urlparse(access_method.access_url.url).scheme
            if access_method_status != ds.DownloadStatus.COMPLETED:
                start_msg = start_msg_template.format(
                    objid=self.drs_obj.id, scheme=scheme)
                self.logger.debug(start_msg)
                access_method_status = ds.DownloadStatus.STARTED
                access_method.set_data_accessor(self)
                access_method.download_retry_loop()
                
                access_method_status = access_method.download_status
                
                end_msg = end_msg_template.format(
                    objid=self.drs_obj.id,
                    scheme=scheme, 
                    status=ds.DOWNLOAD_STATUS[access_method_status]
                )
                self.logger.debug(end_msg)

        self.download_status = access_method_status
    
    def validate_checksum(self):
        """Validate the checksum of a successfully downloaded file

        If a file has been successfully downloaded 
        (download_status == COMPLETED), this method will find the first suitable
        hashing algorithm (ie. supported by the client and included in the 
        'checksums' property of the DRS object). Checks the expected checksum
        value against the checksum of the downloaded file, setting validation
        status based on the results
        """

        filepath = self.get_output_file_path()

        hashfuncs_d = Checksum.HASHFUNCS
        hashfuncs_l = Checksum.RANKED_HASHFUNCS
        checksums_by_type = {c.type: c for c in self.drs_obj.checksums}
        
        # find the most suitable hashing algorithm, for each algorithm in the 
        # ranked list, check if the DRSObject has a checksum of that type 
        hashfunc = None
        hashfunc_not_found = True
        for hashfunc_key in hashfuncs_l:
            if hashfunc_not_found:
                if hashfunc_key in checksums_by_type.keys():
                    self.checksum_algo = hashfunc_key
                    hashfunc = hashfuncs_d[hashfunc_key]
                    self.checksum_exp = checksums_by_type[hashfunc_key].checksum
                    hashfunc_not_found = False
        
        # if a suitable hashing algorithm has been found, perform the hashfunc
        # on the downloaded file, then compare the expected to observed
        # if expected matches observed, checksum status is set to PASSED
        # otherwise, checksum status is set to FAILED
        if hashfunc:
            self.checksum_obs = str(hashfunc(filepath))
            if str(self.checksum_exp) != str(self.checksum_obs):
                msg = "output file {filepath} expected {type} checksum: " \
                    + "{expected} does not match observed: {observed}"
                format_dict = {"filepath": filepath, "type": self.checksum_algo,
                    "expected": self.checksum_exp, 
                    "observed": self.checksum_obs}
                self.logger.error(msg.format(**format_dict))
                self.checksum_status = cs.ChecksumStatus.FAILED
            else:
                self.checksum_status = cs.ChecksumStatus.PASSED

        # if no suitable hashing algorithm has been found, check status is set
        # to FAILED
        else:
            msg = "could not perform checksum validation for {filepath}, " \
                + "no suitable hashing algorithm found"
            format_dict = {"filepath": filepath}
            self.logger.warning(msg.format(**format_dict))
            self.checksum_status = cs.ChecksumStatus.FAILED

    def get_output_file_path(self):
        """Get the path of download file destination on local machine

        Returns:
            (str): destination of downloaded file
        """

        dirname = os.path.join(self.cli_kwargs["output_dir"], self.drs_obj.id)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        fname = self.drs_obj.name if self.drs_obj.name else self.drs_obj.id
        fname = os.path.basename(fname)
        if dirname:
            fname = os.path.join(dirname, fname)
        return fname
    
    def report_line(self):
        """Get data accessor status as a line for the report

        Returns:
            (str): data accessor status formatted for download report
        """

        fields = [
            self.drs_obj.id,
            self.drs_obj.name if self.drs_obj.name else "N/A",
            self.get_output_file_path(), # outfile
            ds.DOWNLOAD_STATUS[self.download_status],
            cs.CHECKSUM_STATUS[self.checksum_status],
            self.checksum_algo,
            self.checksum_exp,
            self.checksum_obs
        ]

        return "\t".join(fields)
    
    def was_successful(self):
        """Determine if a data accessor's download and validation succeeded

        Returns:
            (bool): True if successful download/validation
        """

        # download status must be SUCCESS
        # if checksum validation was requested, validation status must be PASSED
        # otherwise, do not check checksum status
        success = False
        if self.download_status == ds.DownloadStatus.COMPLETED:
            if self.cli_kwargs["validate_checksum"]:
                if self.checksum_status == cs.ChecksumStatus.PASSED:
                    success = True
            else:
                success = True
        return success
