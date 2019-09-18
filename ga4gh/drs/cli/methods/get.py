# -*- coding: utf-8 -*-
"""Module ga4gh.drs.cli.methods.get.py
Contains main entrypoint method(s) for the 'get' command group
"""

import click
import json
import logging
import sys
import traceback
import urllib3
from ga4gh.drs.config.global_state import GLOBALSTATE
from ga4gh.drs.definitions.object import DRSObject
from ga4gh.drs.exceptions import drs_exceptions as de
from ga4gh.drs.routes.route_object_info import RouteObjectInfo
from ga4gh.drs.routes.route_fetch_bytes import RouteFetchBytes
from ga4gh.drs.util.data_accessor import DataAccessor
from ga4gh.drs.util.download_tree import DownloadTree
from ga4gh.drs.util.download_manager import DownloadManager
from ga4gh.drs.util.functions.logging import *
from ga4gh.drs.util.logger import Logger
from ga4gh.drs.util.validators.get_cli_validator import GetCliValidator

def get(**kwargs):
    """Get a DRS object/bundle from a compliant service

    This method takes, at minimum, a DRS service base url and object ID, as 
    well as other cli-specified options. The method will fetch object 
    metadata (as JSON) and write it to stdout or output file. If specified, 
    downloads requested object bytes for a single object, or, if a bundle was
    requested, bytes of all objects in bundle. Checksum validation can also be
    performed.

    Arguments:
        kwargs (dict): command-line arguments parsed via Click package
    """

    GLOBALSTATE.set_prop("cli", kwargs)
    GLOBALSTATE.set_prop("exit_code", 0)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logger = None

    try:
        # validate get command cli args beyond what is handled by click
        # eg. check URL is in valid format 
        validator = GetCliValidator(**kwargs)
        validator.validate_all()

        GLOBALSTATE.set_prop("logger", Logger("drs.logger"))
        logger = GLOBALSTATE.get_prop("logger")
        logger.debug("command-line arguments: " + str(sanitize(kwargs)))

        # log warning if ssl verification is turned off
        if kwargs["suppress_ssl_verify"]:
            logger.warning("SSL verification is turned off. We recommend "
                + "turning verification on unless it is necessary that it be "
                + "off.")

        # create the first request object, which requests the object under
        # the cli-specified OBJECT_ID
        route_obj_args = [kwargs[k] for k in ["url", "object_id", "expand"]]
        route_obj_kwargs = {k: kwargs[k] for k in 
            ["suppress_ssl_verify", "authtoken"]}
        route_obj_info = RouteObjectInfo(*route_obj_args, **route_obj_kwargs)
        http_headers = route_obj_info.construct_headers()
        logger.info("issuing request to DRS Object endpoint")
        response = None
        try:
            response = route_obj_info.issue_request()
        except Exception as e:
            raise de.CLIException("Could not find any service/host by "
                                  "specified URL")
        
        # check if response was OK, or if it returned an error code
        # if program receives an error code, then do not proceed with 
        # outputting metadata or download, log failure
        status_code_series = str(response.status_code)[0] + "xx"
        if status_code_series in set(["4xx", "5xx"]):
            m = "Invalid status code ({code}) in https response. ".format(
                code=str(response.status_code)
            ) + "response body: " + str(response.content)
            raise de.StatusCodeException(m)

        # if response was OK, log success and write metadata JSON to stdout
        # or output file
        root_json = json.loads(response.content)
        logger.info("JSON for object " + kwargs["object_id"] + 
            " successfully retrieved")
        metadata_output = json.dumps(root_json, indent=4) + "\n"
        
        # output metadata to stdout or output file
        # if 'silent' was specified, do not print out metadata
        if kwargs["output_metadata"]:
            metadata_file = open(kwargs["output_metadata"], "w")
            metadata_file.write(metadata_output)
            metadata_file.close()
        else:
            if not kwargs["silent"]:
                print(metadata_output, end='')
        
        # if user requested to download object bytes
        if kwargs["download"]:
            logger.info("object/bundle download requested")

            # create a list of data accessors, which will handle downloading
            # for one object in a bundle
            # check whether the object requested at OBJECT_ID refers to a 
            # singular object, or a bundle
            # if singular object, create a single DataAccessor,
            # if bundle, program needs to find all terminal nodes (objects)
            # in the bundle hierarchy
            data_accessors = []
            root_object = DRSObject(root_json)
            if not root_object.is_bundle:
                logger.info("requested object is a single object")
                data_accessors.append(
                    DataAccessor(root_object, http_headers))
            else:
                # requested object is a bundle, create the DownloadTree,
                # which recurses through the bundle, finding all terminal
                # nodes/objects and adds them to data accessor list
                logger.info("requested object is a bundle, finding all "
                    + "downloadable objects referenced in the bundle tree")
                download_tree = DownloadTree(root_object)
                download_tree.recurse_find_leaves(download_tree.drs_object)
                data_accessors = download_tree.get_data_accessors_for_leaves(
                    headers=http_headers)
            
            # create the download manager, which accepts all the data accessors
            # and initiates/manages download threads for each accessor
            download_manager = DownloadManager(data_accessors)
            download_manager.execute_thread_pool()
            logger.info("all downloaded files written to output directory")
            download_manager.write_report()
            download_success = \
                False \
                if False in set([d.was_successful() for d in data_accessors]) \
                else True
            if not download_success:
                GLOBALSTATE.set_prop("exit_code", 2)

        else:
            logger.info("object/bundle download not requested")
                
    except de.DRSException as e:
        if logger:
            logger.error(str(e))
        else:
            print(str(e))
        GLOBALSTATE.set_prop("exit_code", 1)
    except Exception as e:
        if logger:
            logger.error(str(e))
        else:
            print(str(e))
        GLOBALSTATE.set_prop("exit_code", 1)
        traceback.print_exc()
    finally:
        if logger:
            logger.info("exiting with exit code: " + 
                str(GLOBALSTATE.get_prop("exit_code")))
        else:
            print("exiting with exit code: " 
                + str(GLOBALSTATE.get_prop("exit_code")))
        sys.exit(GLOBALSTATE.get_prop("exit_code"))
