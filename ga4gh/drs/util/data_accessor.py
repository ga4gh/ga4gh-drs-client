from ga4gh.drs.definitions.checksum import Checksum
import ga4gh.drs.config.globals as gl

class DataAccessor(object):
    
    def __init__(self, drs_object, cli_kwargs, headers):

        self.drs_object = drs_object
        self.cli_kwargs = cli_kwargs
        self.headers = headers
        self.download_status = gl.DownloadStatus.NOT_STARTED
    
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
        exp_digest = None
        digest = None
        for hashfunc_key in hashfuncs_l:
            if hashfunc_not_found:
                if hashfunc_key in checksums_by_type.keys():
                    hashfunc = hashfuncs_d[hashfunc_key]
                    exp_digest = checksums_by_type[hashfunc_key].checksum
                    hashfunc_not_found = False
        
        if hashfunc:
            digest = hashfunc(filepath)
            if exp_digest != digest:
                print("checksums don't match")
                print(exp_digest)
                print(digest)

        else:
            print("no suitable hashing function found for object")
                





