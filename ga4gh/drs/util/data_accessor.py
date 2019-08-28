# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.data_accessor.py
Contains the DataAccessor class, which manages the byte download of a single 
DRSObject. Attempts to download the full file by all available access methods
until the download has completed successfully.
"""

import ga4gh.drs.config.globals as gl
from ga4gh.drs.definitions.checksum import Checksum

class DataAccessor(object):
    """Manages the byte download of a single DRSObject

    Attributes:
        drs_object (DRSObject): reference to DRSObject to be downloaded
        cli_kwargs (dict): cli args/options
        headers (dict): headers to be supplied to download request
        download_status (int): current status of the file download
        checksum_status (int): current status of checksum validation
        checksum_algo (str): name of algorithm used in checksum validation
        checksum_exp (str): expected checksum digest value given the algorithm
        checksum_obs (str): observed checksum digest value given the algorithm
        logger (Logger): global logger
    """
    
    def __init__(self, drs_object, cli_kwargs, headers):
        """Instantiates a DataAccessor object

        Arguments:
            drs_object (DRSObject): reference to DRSObject
            cli_kwargs (dict): cli args/options
            headers (dict): headers to be supplied to download request
        """

        self.drs_object = drs_object
        self.cli_kwargs = cli_kwargs
        self.headers = headers
        self.download_status = gl.DownloadStatus.NOT_STARTED
        self.checksum_status = gl.ChecksumStatus.NOT_APPLICABLE
        self.checksum_algo = "N/A"
        self.checksum_exp = "N/A"
        self.checksum_obs = "N/A"
        self.logger = gl.logger
    
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
        self.download_status = gl.DownloadStatus.STARTED

        # for each access method, execute the 'download_retry_loop' function,
        # if the access method is successful, then this loop will break
        # if not, the next access method is attempted
        # if an access method is successful, the data accessor's download 
        # status is set to 'COMPLETED'
        # if all access methods are exhausted without success, the data
        # accessor's download status is set to 'FAILED'
        access_method_status = gl.DownloadStatus.NOT_STARTED
        for access_method in self.drs_object.access_methods:
            if access_method_status != gl.DownloadStatus.COMPLETED:
                access_method_status = gl.DownloadStatus.STARTED
                access_method.set_data_accessor(self)
                access_method.download_retry_loop()
                access_method_status = access_method.download_status
        
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

        filepath = self.drs_object.access_methods[0].get_output_file_path()

        hashfuncs_d = Checksum.HASHFUNCS
        hashfuncs_l = Checksum.RANKED_HASHFUNCS
        checksums_by_type = {c.type: c for c in self.drs_object.checksums}
        
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
                self.checksum_status = gl.ChecksumStatus.FAILED
            else:
                self.checksum_status = gl.ChecksumStatus.PASSED

        # if no suitable hashing algorithm has been found, check status is set
        # to FAILED
        else:
            msg = "could not perform checksum validation for {filepath}, " \
                + "no suitable hashing algorithm found"
            format_dict = {"filepath": filepath}
            self.logger.warning(msg.format(**format_dict))
            self.checksum_status = gl.ChecksumStatus.FAILED
    
    def report_line(self):
        """Get data accessor status as a line for the report

        Returns:
            (str): data accessor status formatted for download report
        """

        fields = [
            self.drs_object.id,
            self.drs_object.name if self.drs_object.name else "N/A",
            self.drs_object.access_methods[0].get_output_file_path(), # outfile
            gl.DOWNLOAD_STATUS[self.download_status],
            gl.CHECKSUM_STATUS[self.checksum_status],
            self.checksum_algo,
            self.checksum_exp,
            self.checksum_obs
        ]

        return "\t".join(fields)
