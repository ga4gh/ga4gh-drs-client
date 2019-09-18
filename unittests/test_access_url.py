import json
from ga4gh.drs.definitions.access_url import AccessUrl
from ga4gh.drs.definitions.object import DRSObject
from unittests.cli_kwargs import CLI_KWARGS_0

data = [
    {
        "headers": [
            "Authorization: Bearer abc123"
        ],
        "url": "https://localhost:5000/"
    }
]

new_headers = [
    [
        "Authorization: Bearer xyz789"
    ],
    [
        "Authorization: Bearer def456"
    ]
]

new_urls = [
    "https://localhost:5000/ga4gh/drs/v1/objects/abc123",
    "https://localhost:5000/ga4gh/drs/v1/objects/xyzdefghi"
]

drs_json = open("unittests/testdata/json/drs_object_0.json", "r").read()
drs_dict = json.loads(drs_json)
drs_obj = DRSObject(drs_dict)
access_method = drs_obj.access_methods[0]

def assert_all_headers(access_url, headers_l):
    for i in range(0, len(access_url.get_headers())):
        assert access_url.get_headers()[i] == headers_l[i]

def test_access_url():
    
    for json in data:
        access_url = AccessUrl(json, access_method)
        assert access_url.get_url() == json["url"]
        assert_all_headers(access_url, json["headers"])
        
def test_set_header():

    access_url = AccessUrl(data[0], access_method)
    for new_header in new_headers:
        access_url.set_headers(new_header)
        assert_all_headers(access_url, new_header)

def test_set_url():

    access_url = AccessUrl(data[0], access_method)
    for new_url in new_urls:
        access_url.set_url(new_url)
        assert access_url.get_url() == new_url

def test_issue_request():
    
    access_url = AccessUrl(data[0], access_method)
    for new_url in new_urls[:1]:
        access_url.set_headers([])
        access_url.set_url(new_url)
        response = access_url.issue_request()
        assert response.status_code == 200
        


