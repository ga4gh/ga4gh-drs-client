import json
from unittests.cli_kwargs import *
from ga4gh.drs.definitions.object import DRSObject, ContentsObject

cli_kwargs = CLI_KWARGS_0
drs_json_path = "unittests/testdata/json/drs_object_{i}.json"
drs_func = lambda i: json.load(open(drs_json_path.format(i=str(i)), "r"))
drs_objs = [DRSObject(drs_func(i), cli_kwargs) for i in range(0, 3)]


def test_drs_object():

    for i in range(0, len(drs_objs)):
        drs_json = drs_func(i)
        drs_obj = drs_objs[i]

        assert drs_obj.id == drs_json["id"]

        if drs_obj.is_bundle:
            assert len(drs_obj.contents) > 0
        else:
            assert len(drs_obj.contents) == 0

def test_contents_object():
    pass
