# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.download_manager.py
Contains the DownloadManager class, which manages all DataAccessor objects.
Launches DataAccessor download as separate threads, and is responsible for 
starting, stopping, and checking status of each thread.
"""

import datetime
import ga4gh.drs.config.globals as gl
import threading
import time
import os
from ga4gh.drs.util.functions.logging import *

class DownloadManager(object):
    """Manages all DataAccessor objects as separate threads

    Attributes:
        data_accessors (list): list of instantiated DataAccessors
        report_file (str): path to output download report file
        download_threads (list): list of DataAccessor download threads
        threads_status (list): current status of each thread
        has_started (list): indicates whether each thread has been started
        max_threads (int): max executable threads
    """

    def __init__(self, data_accessors):
        """Instantiates a DownloadManager object

        Arguments:
            data_accessors (list): list of instantiated DataAccessors
        """

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
        """Thread worker function for DataAccessor download

        Arguments:
            data_accessor (DataAccessor): a DataAccessor object
        """

        # run the DataAccessor download method, then, if download was successful
        # execute the checksum validation method if the client has requested
        # it
        data_accessor.download()
        if data_accessor.download_status == gl.DownloadStatus.COMPLETED:
            if data_accessor.cli_kwargs["validate_checksum"]:
                data_accessor.validate_checksum()

    def execute_thread_pool(self):
        """Executes all download threads, holding until all have finished

        Given all DataAccessors, the DownloadManager will start unstarted
        threads, as long as the current thread count does not exceed max 
        threads. Program execution is held here by a while loop until all
        threads are shown to be finished.
        """

        all_threads_finished = False
        while not all_threads_finished:
            for i in range(0, len(self.threads_status)):
                # for each thread, check if thread has started, if not,
                # start the thread if the current working threads does not 
                # exceed maximum
                notstarted, inprogress, finished = self.__get_n_status()
                current_thread = self.download_threads[i]
                current_thread_status = self.threads_status[i]

                if current_thread_status == "NOTSTARTED" \
                and inprogress < self.max_threads:
                    current_thread.start()
                    self.has_started[i] = True
                
                self.__set_thread_status(current_thread, i)
                
                # if the number of finished threads equals the total number
                # of threads, then exit the while loop
                if finished == len(self.threads_status):
                    all_threads_finished = True
            
            time.sleep(5)
    
    def write_report(self):
        """Write the download status report to the output file"""

        # report headers include date-time, supplied command-line parameters
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

        # header row of table
        table_header = "\t".join(
            ["ID", "Name", "Output File", "Download Status", "Checksum Status",
            "Hash Algorithm", "Expected", "Observed"]
        )

        # get the status of each data accessor as a line
        content = [header, table_header]
        for data_accessor in self.data_accessors:
            content.append(data_accessor.report_line())

        # write all to output file
        open(self.report_file, "w").write("\n".join(content) + "\n")

    def __initialize_download_threads(self):
        """Initialize the DownloadManager's 'download_threads' property

        For each DataAccessor in data_accessors, create a thread, tying the
        data accessor to the worker function.

        Returns:
            (list): list of unstarted download threads
        """

        download_threads = []
        for data_accessor in self.data_accessors:
            thread = threading.Thread(
                target=self.download_thread_func, 
                args=(data_accessor,))
            download_threads.append(thread)
        
        return download_threads

    def __set_thread_status(self, thread, i):
        """Set the status of a thread

        Modifies the entry at position i in the threads_status list according
        to the status of the provided thread.

        Arguments:
            thread (Thread): a single download thread
            i (int): the thread's position in the thread/status list
        """
        
        status = self.threads_status[i]
        has_started = self.has_started[i]

        # if the thread is alive, then thread status is set to INPROGRESS,
        # if thread is not alive, it can be either STARTED or FINISHED
        # if thread was already started and is no longer alive, then its
        # status is FINISHED
        if thread.isAlive():
            self.threads_status[i] = "INPROGRESS"
        else:
            if has_started:
                self.threads_status[i] = "FINISHED"
    
    def __get_n_status(self):
        """Get the number of NOTSTARTED, INPROGRESS, and FINISHED threads

        Returns:
            (dict): count of NOTSTARTED, INPROGRESS, and FINISHED threads
        """

        # iterate through the status list, adding 1 to the overall counter
        # for the status it contains
        d = {"NOTSTARTED": 0, "INPROGRESS": 0, "FINISHED": 0}
        for s in self.threads_status:
            d[s] += 1
        return [d["NOTSTARTED"], d["INPROGRESS"], d["FINISHED"]]
