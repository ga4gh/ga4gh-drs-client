import os
import re
import sh
import requests
import subprocess
import ga4gh.drs.config.globals as gl
from ga4gh.drs.util.method_types.method_type import MethodType
from ga4gh.drs.util.method_types.method_type import DownloadSubmethod
from ga4gh.drs.exceptions.drs_exceptions import DownloadSubmethodException

class GS(MethodType):
    
    def __init__(self, json, drs_obj):
        super(GS, self).__init__(json, drs_obj)
        self.download_submethods = [
            self.__download_by_https,
            self.__download_by_gsutil
        ]

    def __convert_gs_to_https(self):
        gs_url = self.access_url.get_url()
        sub_from = "^gs://"
        sub_to = "https://storage.googleapis.com/"

        new_url = re.sub(sub_from, sub_to, gs_url)
        return new_url

    @DownloadSubmethod()
    def __download_by_https(self, write_config):
        submethod_status = gl.DownloadStatus.STARTED
        https_url = self.__convert_gs_to_https()        
        with requests.get(https_url, headers=self.data_accessor.headers,
            stream=True) as r:
            iterator_func = r.iter_content
            self.download_write_stream(iterator_func, write_config)
    
    @DownloadSubmethod()
    def __download_by_gsutil(self, write_config):
        def iterator_func(chunk_size=8192):
            url = self.access_url.get_url()
            cmd = "gsutil cp " + url + " -"

            task = subprocess.Popen(cmd, shell=True, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            file_not_complete = True
            while file_not_complete:
                chunk = task.stdout.read(chunk_size)
                if chunk:
                    yield chunk
                else:
                    file_not_complete = False

            task.poll()
            if task.returncode != 0:
                raise DownloadSubmethodException(
                    write_config["opath"] + ": exception when downloading "
                    + "by gsutil: " + str(task.stderr.read()))
            
        self.download_write_stream(iterator_func, write_config)
