# -*- coding: utf-8 -*-
"""Module ga4gh.drs.util.functions.logging.py
Supplementary methods for logging program state to logfile/console
"""

def sanitize(d):
    """Sanitize sensitive information, preventing it from being logged

    Given a dictionary, look up all keys that may contain sensitive information
    (eg. "authtoken", "Authorization"). Returns a dict with the value of these
    keys replaced with "omitted"

    Arguments:
        d (dict): dictionary containing potentially sensitive information
    
    Returns:
        (dict): sensitive information removed from dict
    """
    
    sanitize_keys = [
        "authtoken",
        "Authorization"
    ]
    
    r = d.copy()
    sanitized = {k: "omitted" for k in sanitize_keys if k in r.keys()}
    r.update(sanitized)
    return r

