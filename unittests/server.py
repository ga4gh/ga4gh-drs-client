import json
from flask import Flask, Response, request, redirect, send_file

app = Flask(__name__)

data_dir = "unittests/testdata/"
json_dir = data_dir + "json/"
bam_dir =  "testdata/bam/"
objects_dict = {
    "abc123": "drs_object_0.json",
    "def456": "drs_object_1.json",
    "bundle0": "drs_object_2.json",
    "bundle1": "drs_object_3.json",
    "ghi789": "drs_object_4.json",
    "obj5": "drs_object_5.json",
    "obj6": "drs_object_6.json"
}
bam_dict = {
    "abc123": "unittest.bam.bai",
    "def456": "unittest.bam",
    "ghi789": "unittest.bam",
    "obj5": "unittest.bam.bai",
    "obj6": "unittest.bam.bai"
}
access_dict = {
    "obj5": {
        "rest-api": {
            "valid": True,
            "obj": {
                "url": "https://localhost:5000/download/obj5",
                "headers": []
            }
        }
    },
    "obj6": {
        "rest-api": {
            "valid": False
        }
    }
}

@app.route("/")
def hello():
    return Response("hello world")

@app.route("/ga4gh/drs/v1/objects/<object_id>")
def get_object(object_id):

    status = 404
    data = json.dumps({
        "msg": "object with id: " + object_id + " not found"
    })

    if object_id in objects_dict.keys():
        status = 200
        data = open(json_dir + objects_dict[object_id]).read()
    
    return Response(data, mimetype="application/json", status=status)

@app.route("/ga4gh/drs/v1/objects/<object_id>/access/<access_id>")
def get_access_url(object_id, access_id):

    subdict = access_dict[object_id][access_id]
    is_valid = subdict["valid"]
    data = "not valid json"
    if is_valid:
        data = json.dumps(subdict["obj"])
    return Response(data, mimetype="application/json", status=200)

@app.route("/download/<object_id>")
def download(object_id):

    status = 404
    data = "Not Found"
    response = data

    if object_id in bam_dict.keys():
        status = 200
        path = bam_dir + bam_dict[object_id]
        response = send_file(path)

    return response

if __name__ == "__main__":
    app.run(ssl_context="adhoc")