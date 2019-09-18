# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.method_types.gs.py
Contains the GS class, a child of MethodType. GS contains submethods to 
download DRS object bytes according to the Google Storage (gs) url scheme.
"""

import os
import re
import requests
import subprocess
from ga4gh.drs.exceptions.drs_exceptions import DownloadSubmethodException
from ga4gh.drs.util.method_types.method_type import DownloadSubmethod
from ga4gh.drs.util.method_types.method_type import MethodType

class GS(MethodType):
    """Download DRS object bytes according to Google Storage (gs) url scheme

    Attributes:
        download_submethods (list): multiple methods to attempt byte download
    """
    
    def __init__(self, json, drs_obj):
        """Instantiates a GS object

        Arguments:
            json (dict): parsed AccessMethod JSON, used to set other attributes
            drs_obj (DRSObject): reference to parent DRSObject object
        """

        super(GS, self).__init__(json, drs_obj)
        self.download_submethods = [
            self.__download_by_https,
            self.__download_by_gsutil
        ]

    def __convert_gs_to_https(self):
        """Convert a gs formatted URL to https

        Returns:
            (str): https-formatted url, references a Google Storage object
        """

        gs_url = self.access_url.get_url()
        sub_from = "^gs://"
        sub_to = "https://storage.googleapis.com/"

        new_url = re.sub(sub_from, sub_to, gs_url)
        return new_url

    @DownloadSubmethod()
    def __download_by_https(self, write_config):
        """Download submethod, get object bytes by https

        Arguments:
            write_config (dict): config to write downloaded file
        """

        # convert the gs url to https, and attempt to download it via
        # GET request
        https_url = self.__convert_gs_to_https()
        self._MethodType__download_by_requests_package(https_url, write_config)
    
    @DownloadSubmethod()
    def __download_by_gsutil(self, write_config):
        """Download submethod, get object bytes by gsutil cli tool

        Arguments:
            write_config (dict): config to write downloaded file
        """

        def iterator_func(chunk_size=8192):
            """Iterator function for chunked writing of output file

            Arguments:
                chunk_size (int): download chunk size in bytes
            """

            # create a subprocess based on gsutil command-line tool
            # as stdout is output is chunks, yield this to outer loop
            # poll for status at end of stdout stream, set status
            # according to exit code
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
