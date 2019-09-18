import json
from unittests.cli_kwargs import *
from ga4gh.drs.config.global_state import GLOBALSTATE 
from ga4gh.drs.definitions.object import DRSObject
from ga4gh.drs.definitions.access_method import AccessMethod
from ga4gh.drs.util.logger import Logger

GLOBALSTATE.set_prop("cli", CLI_KWARGS_0)
GLOBALSTATE.set_prop("logger", Logger("drs.client.unittests"))
drs_obj_json = json.load(open("unittests/testdata/json/drs_object_0.json", "r"))
drs_obj = DRSObject(drs_obj_json)

def test_access_method():

    for i in range(0, len(drs_obj.access_methods)):
        acc_meth_obj = drs_obj.access_methods[i]
        acc_meth_json = drs_obj_json["access_methods"][i]

        if acc_meth_obj.access_id:
            assert acc_meth_obj.access_id == acc_meth_json["access_id"]
        
        if acc_meth_obj.access_url:
            assert acc_meth_obj.access_url.get_url() == \
                   acc_meth_json["access_url"]["url"]
        
        if acc_meth_obj.region:
            assert acc_meth_obj.region == acc_meth_json["region"]
        
        assert acc_meth_obj.type == acc_meth_json["type"]
