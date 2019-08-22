import ga4gh.drs.config.globals as gl
from ga4gh.drs.definitions.access_method import AccessMethod

class MethodType(AccessMethod):


    def __init__(self, json, drs_obj):
        super(MethodType, self).__init__(json, drs_obj)
        self.data_accessor = None
        self.download_status = gl.DownloadStatus.NOT_STARTED
        self.download_submethods = []

    def download_retry_loop(self):

        self.download_status = gl.DownloadStatus.STARTED
        
        submethod_status = gl.DownloadStatus.NOT_STARTED
        for submethod in self.download_submethods:
            if submethod_status != gl.DownloadStatus.COMPLETED:
                submethod_status = gl.DownloadStatus.STARTED
                submethod_status = submethod()
        
        self.download_status = submethod_status
    
    def set_data_accessor(self, data_accessor):
        self.data_accessor = data_accessor
    
    def get_output_filename(self):

        fname = self.drs_obj.name if self.drs_obj.name else self.drs_obj.id
        dirname = self.data_accessor.cli_kwargs["output_dir"]
        if dirname:
            fname = dirname + "/" + fname
        return fname
