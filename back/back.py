from flask import Flask, render_template, jsonify, Response, request
from flask_cors import CORS
from PIL import Image
import json, os

app = Flask(__name__)
CORS(app)


@app.route("/image/<imageid>")
def index(imageid):
    image = open("./{}".format(imageid),"rb").read()
    resp = Response(image, mimetype="image/png")
    return resp
# from flask import render_template, jsoçnify

@app.route("/get")
def json():
    return jsonify({"a":"123","b":"445"})

@app.route("/post", methods=['POST'])
def post_test():
    data = request.get_data()
    print(data)
    return jsonify({"images":["test.png","fly.png"]})


@app.route('/test')
def test():
    return "1"


if __name__ == '__main__':
    app.run()