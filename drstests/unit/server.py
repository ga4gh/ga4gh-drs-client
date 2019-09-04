import json
from flask import Flask, Response, request

app = Flask(__name__)

data_dir = "drstests/data/"
objects_dict = {
    "abc123": "drs_object_0.json",
    "def456": "drs_object_1.json",
    "ghi789": "drs_object_2.json"
}

@app.route("/ga4gh/drs/v1/objects/<object_id>")
def get_object(object_id):

    data = json.dumps({
        "msg": "object with id: " + object_id + " not found"
    })

    if object_id in objects_dict.keys():
        data = open(data_dir + objects_dict[object_id]).read()
    
    return Response(data, mimetype="application/json")
    