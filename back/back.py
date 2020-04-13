from flask import Flask, render_template, jsonify, Response, request
from flask_cors import CORS
# from PIL import Image
import json, os
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)


# from flask import render_template, jsoçnify

@app.route("/train",methods=['POST'])
def train():
    return jsonify({"a":"123","b":"445"})

@app.route("/post", methods=['POST','GET'])
def post_num():
    num = request.get_json()['value']
    # 这里应该是一个返回id_list,img_list的函数，随便示例一下
    img_lst = []
    id_lst= list(range(num))
    for i in range(int(num)):
        x = np.random.random(10)
        fig = plt.figure(1, figsize=(5, 5))
        plt.plot(x)
        sio = BytesIO()
        fig.savefig(sio, format='png')
        img_base64 = base64.b64encode(sio.getvalue()).decode('utf8')
        img_lst.append(img_base64)
    return jsonify({"ids":id_lst,"images":img_lst})


@app.route("/retrain", methods=['POST','GET'])
def retrain():
    ids = request.get_json()['ids']
    labels = request.get_json()['labels']
    print(ids)
    print(labels)
    return jsonify({'msg':'OK'})




@app.route('/test')
def test():
    return jsonify({'msg':'OK'})


if __name__ == '__main__':
    app.run(debug=True)
