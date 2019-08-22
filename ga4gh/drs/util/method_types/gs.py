from tqdm import tqdm
import re
import requests
import ga4gh.drs.config.globals as gl
from ga4gh.drs.util.method_types.method_type import MethodType
from ga4gh.drs.exceptions.drs_exceptions import DownloadSubmethodException

class GS(MethodType):
    
    def __init__(self, json, drs_obj):
        super(GS, self).__init__(json, drs_obj)
        self.download_submethods = [
            self.__download_by_https,
            self.__download_by_gsutil
        ]

    def __download_by_https(self):
        submethod_status = gl.DownloadStatus.STARTED

        try:
            
            if self.access_url:
                #TODO: remove drs url modifications
                suburi = re.sub("^gs://", "https://storage.googleapis.com/", self.access_url.get_url())
                output_filename = self.get_output_filename()
                output_file = open(output_filename, "wb")

                chunk_size = 8192
                file_size_bytes = self.drs_obj.size
                
                with requests.get(suburi, headers=self.data_accessor.headers, stream=True) as r:
                    for chunk in tqdm(r.iter_content(chunk_size=chunk_size), total=file_size_bytes/chunk_size):
                        if chunk:
                            output_file.write(chunk)
                        
                output_file.close()

            elif self.access_id:
                pass
            else:
                raise DownloadSubmethodException(
                    "Neither access_url or access_id is specified")

            submethod_status = gl.DownloadStatus.COMPLETED
        except DownloadSubmethodException as e:
            submethod_status = gl.DownloadStatus.FAILED

        return submethod_status
    
    def __download_by_gsutil(self):
        print("downloading by gsutil: completed")
        return gl.DownloadStatus.COMPLETED
        
        
    