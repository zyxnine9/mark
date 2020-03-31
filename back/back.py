from flask import Flask, render_template, jsonify, Response, request
from flask_cors import CORS
# from PIL import Image
import json, os
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from data_process import *
from network import *

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
    id_lst= []
    for i in range(int(num)):
        signal_num = np.random.randint(0, 2000)
        x = np.arange(0, 2000)
        # y = filtedData[x]
        y_fft = datas[signal_num][x]
        y_raw = raw_datas[signal_num][0][x]
        plt.cla()
        fig = plt.figure(1, figsize=(10, 5))

        plt.subplot(121)
        plt.ylim(ymax=0.005)
        plt.title(label_name[labels[signal_num][0]])
        plt.plot(x, y_fft)
        plt.subplot(122)

        plt.title(label_name[labels[signal_num][0]])
        plt.plot(x, y_raw)
        sio = BytesIO()
        fig.savefig(sio, format='png')
        img_base64 = base64.b64encode(sio.getvalue()).decode('utf8')
        img_lst.append(img_base64)
        id_lst.append(datas[signal_num][-1])
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
    return "1"


if __name__ == '__main__':
    datas, raw_datas, labels, datas_butter, X_train, X_test, y_train, y_test = load_data_to_train(path)
    app.run(debug=True)