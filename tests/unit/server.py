import json
from flask import Flask, Response, request

app = Flask(__name__)

@app.route("/")
def hello_world():

    return Response(json.dumps({"hello": "world"}), mimetype="application/json")
    