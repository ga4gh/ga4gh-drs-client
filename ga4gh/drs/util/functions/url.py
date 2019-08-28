# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.functions.url.py
Contains functions for modifying urls from one scheme to another
"""

from urllib.parse import urlparse

def parse_drs_url(drs_url):
    """Convert a drs url to an https url

    Arguments:
        drs_url (str): drs-scheme url (ie. drs://...)
    
    Returns:
        (list): https-scheme url, and object id
    """
    
    parsed = urlparse(drs_url)
    path_s = parsed.path.split("/")
    prefix_path = "/".join(path_s[:-1])
    object_id = path_s[-1]
    
    new_base_url = "https://" + parsed.netloc + prefix_path

    return [new_base_url, object_id]
