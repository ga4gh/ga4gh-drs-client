import os
import ga4gh.drs.config.globals as gl
from ga4gh.drs.definitions.access_method import AccessMethod
from ga4gh.drs.exceptions.drs_exceptions import DownloadSubmethodException
from tqdm import tqdm

def DownloadSubmethod():
    def decorator_func(submethod_func):
        def wrapper(method_type_obj):
            submethod_status = gl.DownloadStatus.STARTED

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
    
    def get_output_file_path(self):

        fname = self.drs_obj.name if self.drs_obj.name else self.drs_obj.id
        dirname = self.data_accessor.cli_kwargs["output_dir"]
        if dirname:
            fname = os.path.join(dirname, fname)
        return fname

    def download_write_stream(self, iterator_func, write_config):

        oname, ofile, csize, fsize, tchunks = [write_config[k] for k in [
            "oname", "ofile", "csize", "fsize", "tchunks"]]

        silent = self.data_accessor.cli_kwargs["silent"]
        iterator = iterator_func(chunk_size=csize)

        if not silent:
            iterator = tqdm(iterator, total=tchunks, desc=oname)
        for chunk in iterator:
            ofile.write(chunk)
        ofile.close()
