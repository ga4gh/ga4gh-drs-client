from ga4gh.drs.definitions.checksum import Checksum
import ga4gh.drs.config.globals as gl

class DataAccessor(object):
    
    def __init__(self, drs_object, cli_kwargs, headers):

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
        self.download_status = gl.DownloadStatus.STARTED

        access_method_status = gl.DownloadStatus.NOT_STARTED
        for access_method in self.drs_object.access_methods:
            if access_method_status != gl.DownloadStatus.COMPLETED:
                access_method_status = gl.DownloadStatus.STARTED
                access_method.set_data_accessor(self)
                access_method.download_retry_loop()
                access_method_status = access_method.download_status
        
        self.download_status = access_method_status
    
    def validate_checksum(self):
        filepath = self.drs_object.access_methods[0].get_output_file_path()

        hashfuncs_d = Checksum.HASHFUNCS
        hashfuncs_l = Checksum.RANKED_HASHFUNCS
        checksums_by_type = {c.type: c for c in self.drs_object.checksums}
        
        hashfunc = None
        hashfunc_not_found = True
        for hashfunc_key in hashfuncs_l:
            if hashfunc_not_found:
                if hashfunc_key in checksums_by_type.keys():
                    self.checksum_algo = hashfunc_key
                    hashfunc = hashfuncs_d[hashfunc_key]
                    self.checksum_exp = checksums_by_type[hashfunc_key].checksum
                    hashfunc_not_found = False
        
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

        else:
            msg = "could not perform checksum validation for {filepath}, " \
                + "no suitable hashing algorithm found"
            format_dict = {"filepath": filepath}
            self.logger.warning(msg.format(**format_dict))
            self.checksum_status = gl.ChecksumStatus.FAILED
    
    def report_line(self):
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
