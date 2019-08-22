def sanitize(d):
    
    sanitize_keys = [
        "authtoken",
        "Authorization"
    ]
    
    r = d.copy()
    sanitized = {k: "omitted" for k in sanitize_keys if k in r.keys()}
    r.update(sanitized)
    return r

