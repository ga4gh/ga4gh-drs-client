# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.functions.http.py
Contains helper functions for http-related objects
"""

import re

def is_client_error(sc):
    """Determine if a status code is one of client-series errors

    Arguments:
        sc (int): status code
    
    Returns:
        (bool): True if client error
    """
    
    return str(sc)[0] == "4"

def is_server_error(sc):
    """Determine if a status code is one of server-series errors

    Arguments:
        sc (int): status code
    
    Returns:
        (bool): True if server error
    """
    
    return str(sc)[0] == "5"

def is_error(sc):
    """Determine if a status code is one of error series

    Arguments:
        sc (int): status code
    
    Returns:
        (bool): True if any error
    """

    error = False
    funcs = [
        is_client_error,
        is_server_error
    ]

    for f in funcs:
        if not error:
            error = f(sc)
    return error

def header_list_to_dict(header_list):
    """Convert list of http headers to dictionary

    Arguments:
        header_list (list): list of strings, each string an HTTP header
    
    Returns:
        (dict): dictionary of http headers
    """

    def generator(header_list):
        """Generator. Split a header into a 2-tuple by ":" character

        Arguments:
            header_list (list): list of header strings
        
        Yields:
            (list): 2-tuple of header string
        """

        for h in header_list:
            yield [e.strip().replace(":", "") for e in re.split("\s|:\s", h)]

    return {k:v for k,v in generator(header_list)}
