# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.download_manager.py
Contains the DownloadManager class, which manages all DataAccessor objects.
Launches DataAccessor download as separate threads, and is responsible for 
starting, stopping, and checking status of each thread.
"""

import datetime
import ga4gh.drs.config.download_status as ds
import threading
import os
from concurrent.futures import ThreadPoolExecutor
from ga4gh.drs.util.functions.logging import *

class DownloadManager(object):
    """Manages all DataAccessor objects as separate threads

    Attributes:
        data_accessors (list): list of instantiated DataAccessors
        cli_kwargs (dict): command-line arugments/options
        report_file (str): path to output download report file
        max_workers (int): max threads executing concurrently
    """

    def __init__(self, data_accessors, cli_kwargs):
        """Instantiates a DownloadManager object

        Arguments:
            data_accessors (list): list of instantiated DataAccessors
            cli_kwargs (dict): command-line arguments/options
        """

        self.data_accessors = data_accessors
        self.cli_kwargs = cli_kwargs
        self.report_file = os.path.join(
            self.data_accessors[0].cli_kwargs["output_dir"], 
            "drs_download_report.txt"
        )
        self.max_workers = cli_kwargs["max_threads"]
    
    def download_thread_func(self, data_accessor):
        """Thread worker function for DataAccessor download

        Arguments:
            data_accessor (DataAccessor): a DataAccessor object
        """

        # run the DataAccessor download method, then, if download was successful
        # execute the checksum validation method if the client has requested
        # it
        data_accessor.download()
        if data_accessor.download_status == ds.DownloadStatus.COMPLETED:
            if data_accessor.cli_kwargs["validate_checksum"]:
                data_accessor.validate_checksum()

    def execute_thread_pool(self):
        """Executes all download threads, holding until all have finished

        Given all DataAccessors, the DownloadManager will start unstarted
        threads, as long as the current thread count does not exceed max 
        threads. Program execution is held here by a while loop until all
        threads are shown to be finished.
        """

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.download_thread_func, self.data_accessors)
    
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
