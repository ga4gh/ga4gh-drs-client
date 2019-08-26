import datetime
import threading
import time
import os

from ga4gh.drs.util.functions.logging import *
import ga4gh.drs.config.globals as gl

class DownloadManager(object):

    def __init__(self, data_accessors):

        self.data_accessors = data_accessors
        self.report_file = os.path.join(
            self.data_accessors[0].cli_kwargs["output_dir"], 
            "drs_download_report.txt"
        )
        self.download_threads = self.__initialize_download_threads()
        self.threads_status = ["NOTSTARTED" for i in self.download_threads]
        self.has_started = [False for i in self.download_threads]
        self.max_threads = 2
    
    def download_thread_func(self, data_accessor):
        data_accessor.download()
        if data_accessor.download_status == gl.DownloadStatus.COMPLETED:
            if data_accessor.cli_kwargs["validate_checksum"]:
                data_accessor.validate_checksum()

    def execute_thread_pool(self):

        all_threads_finished = False
        while not all_threads_finished:

            for i in range(0, len(self.threads_status)):
                notstarted, inprogress, finished = self.__get_n_status()
                current_thread = self.download_threads[i]
                current_thread_status = self.threads_status[i]

                if current_thread_status == "NOTSTARTED" \
                and inprogress < self.max_threads:
                    current_thread.start()
                    self.has_started[i] = True
                
                self.__set_thread_status(current_thread, i)
                
                if finished == len(self.threads_status):
                    all_threads_finished = True
            
            time.sleep(5)
    
    def write_report(self):

        kwargs = self.data_accessors[0].cli_kwargs
        iso_format = "%Y-%m-%dT%H:%M:%S"

        header_template = "# DRS v1 Client Download Report\n" \
            + "# Report Generated: {now_strftime}\n" \
            + "# Arguments -> URL: {url}\tOBJECT_ID: {object_id}\n" \
            + "# Options: {options}"
        format_dict = {
            "now_strftime": datetime.datetime.now().strftime(iso_format),
            "url": kwargs["url"],
            "object_id": kwargs["object_id"],
            "options": str(sanitize(kwargs))
        }
        header = header_template.format(**format_dict)

        table_header = "\t".join(
            ["ID", "Name", "Output File", "Download Status", "Checksum Status",
            "Hash Algorithm", "Expected", "Observed"]
        )

        content = [header, table_header]
        for data_accessor in self.data_accessors:
            content.append(data_accessor.report_line())
        open(self.report_file, "w").write("\n".join(content) + "\n")

    def __initialize_download_threads(self):
        download_threads = []
        for data_accessor in self.data_accessors:
            thread = threading.Thread(
                target=self.download_thread_func, 
                args=(data_accessor,))
            download_threads.append(thread)
        
        return download_threads

    def __set_thread_status(self, thread, i):
        
        status = self.threads_status[i]
        has_started = self.has_started[i]

        if thread.isAlive():
            self.threads_status[i] = "INPROGRESS"
        else:
            if has_started:
                self.threads_status[i] = "FINISHED"
    
    def __get_n_status(self):

        d = {"NOTSTARTED": 0, "INPROGRESS": 0, "FINISHED": 0}
        for s in self.threads_status:
            d[s] += 1
        return [d["NOTSTARTED"], d["INPROGRESS"], d["FINISHED"]]
