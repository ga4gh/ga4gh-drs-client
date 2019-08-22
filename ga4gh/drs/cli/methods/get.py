import click
import json
import logging
import sys
import traceback
import threading
import urllib3

import ga4gh.drs.config.globals as gl

from ga4gh.drs.definitions.object import DRSObject
from ga4gh.drs.exceptions import drs_exceptions as de
from ga4gh.drs.util.functions.logging import *
from ga4gh.drs.routes.route_object_info import RouteObjectInfo
from ga4gh.drs.routes.route_fetch_bytes import RouteFetchBytes
from ga4gh.drs.util.data_accessor import DataAccessor
from ga4gh.drs.util.download_tree import DownloadTree
from ga4gh.drs.util.validators.get_cli_validator import GetCliValidator
from urllib.parse import urlparse

def download_thread(data_accessor):
    data_accessor.download()

def get(**kwargs):

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    exit_code = 0

    try:

        loglevel = 1
        if kwargs["silent"]:
            loglevel = 100
        else:
            if kwargs["verbosity"]:
                loglevel = gl.LOGLEVELS[kwargs["verbosity"]]
        logger = gl.logger
        logger.set_handler(logfile=kwargs["logfile"], loglevel=loglevel)
        logger.debug("command-line arguments: " + str(sanitize(kwargs)))

        if kwargs["suppress_ssl_verify"]:
            logger.warning("SSL verification is turned off. We recommend "
                + "turning verification on unless it is necessary that it be "
                + "off.")

        logger.info("validating command-line arguments")
        validator = GetCliValidator(**kwargs)
        validator.validate_args()

        route_obj_args = [kwargs[k] for k in ["url", "object_id", "expand"]]
        route_obj_kwargs = {k: kwargs[k] for k in 
            ["suppress_ssl_verify", "authtoken"]}
        route_obj_info = RouteObjectInfo(*route_obj_args, **route_obj_kwargs)
        logger.info("issuing request to DRS Object endpoint")
        response = route_obj_info.issue_request()
        
        status_code_series = str(response.status_code)[0] + "xx"
        if status_code_series in set(["4xx", "5xx"]):
            m = "Invalid status code ({code}) in https response. ".format(
                code=str(response.status_code)
            ) + "response body: " + str(response.content)
            raise de.StatusCodeException(m)

        root_json = json.loads(response.content)
        logger.info("JSON for object " + kwargs["object_id"] + 
            " successfully retrieved" % kwargs)
        metadata_output = json.dumps(root_json, indent=4) + "\n"
        
        if kwargs["output_metadata"]:
            metadata_file = open(kwargs["output_metadata"], "w")
            metadata_file.write(metadata_output)
            metadata_file.close()
        else:
            if not kwargs["silent"]:
                print(metadata_output, end='')
            
        if kwargs["download"]:
            logger.info("object/bundle download requested")

            data_accessors = []
            root_object = DRSObject(root_json)
            if not root_object.is_bundle:
                logger.info("requested object is a single object")
                data_accessors.append(DataAccessor(root_object))
            else:
                logger.info("requested object is a bundle, finding all "
                    + "downloadable objects referenced in the bundle tree")
                download_tree = DownloadTree(root_object)
                download_tree.recurse_find_leaves(download_tree.drs_object)
                http_headers = route_obj_info.construct_headers()
                data_accessors = download_tree.get_data_accessors_for_leaves(
                    kwargs, http_headers)

            download_threads = []
            for data_accessor in data_accessors:
                thread = threading.Thread(target=download_thread, args=(data_accessor,))
                download_threads.append(thread)
                thread.start()

        else:
            logger.info("object/bundle download not requested")
                
    except de.DRSException as e:
        logger.error(str(e))
        exit_code = 1
    except Exception as e:
        logger.error(str(e))
        exit_code = 1
        traceback.print_exc()
    finally:
        logger.info("exiting with exit code: " + str(exit_code))
        sys.exit(exit_code)
