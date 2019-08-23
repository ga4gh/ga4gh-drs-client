import hashlib
import crc32c

def hashfunc_md5(input_file):
    
    hash_func = hashlib.md5()
    with open(input_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()
    

def hashfunc_crc32c(input_file):

    #TODO: get hashfunc crc32c to work correctly
    content = open(input_file, "rb").read()
    digest = crc32c.crc32(content)
    return digest