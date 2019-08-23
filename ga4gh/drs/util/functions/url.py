from urllib.parse import urlparse

def parse_drs_url(drs_url):
    
    parsed = urlparse(drs_url)
    path_s = parsed.path.split("/")
    prefix_path = "/".join(path_s[:-1])
    object_id = path_s[-1]
    
    new_base_url = "https://" + parsed.netloc + prefix_path

    return [new_base_url, object_id]
