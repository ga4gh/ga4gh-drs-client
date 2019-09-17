ARGS_0 = [
    "-v",
    "-V", "DEBUG",
    "-o", "unittests/outdata/",
    "-d",
    "-m", 'unittests/outdata/metadata.json',
    "-l", 'unittests/outdata/log.txt',
    "-s",
    "https://localhost:5000",
    "abc123"
]

ARGS_1 = [a for a in ARGS_0] + ["-S"]

ARGS_2 = [a for a in ARGS_0]
ARGS_2.remove("-m")
ARGS_2.remove("unittests/outdata/metadata.json")

ARGS_3 = [a for a in ARGS_0]
ARGS_3.remove("abc123")
ARGS_3.append("ghi789")

ARGS_4 = [a for a in ARGS_0]
ARGS_4.remove("-d")

ARGS_5 = [a for a in ARGS_0]
ARGS_5.remove("abc123")
ARGS_5.append("obj5")

ARGS_FAIL_0 = [
    "https://nonexistenthost172583467534.com",
    "FOOID"
]

ARGS_FAIL_1 = [
    "-s",
    "https://localhost:5000/",
    "FOOID"   
]

ARGS_FAIL_2 = [a for a in ARGS_0]
ARGS_FAIL_2.remove("abc123")
ARGS_FAIL_2.append("obj6")

CLI_KWARGS_0 = {
    'validate_checksum': True,
    'output_dir': 'unittests/outdata/',
    'download': True,
    'output_metadata': 'unittests/outdata/metadata.json',
    'logfile': 'unittests/outdata/log.txt',
    'max_threads': 1,
    'verbosity': 'DEBUG',
    'suppress_ssl_verify': True,
    'authtoken': 'omitted',
    'url': 'https://localhost:5000',
    'object_id': 'abc123',
    'expand': False,
    'silent': False
}

