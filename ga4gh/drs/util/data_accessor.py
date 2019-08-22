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
