from flask import Flask, render_template, jsonify, Response, request
from flask_cors import CORS
# from PIL import Image
import json, os
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import data_process
from network import *
import network

app = Flask(__name__)
CORS(app)
path = "../../2020MAR-EMG Labeling Data/labeling.h5"
validation_standard = 0
pre_entropy = []

datas, raw_datas, labels, datas_butter, X_train, X_test, y_train, y_test = data_process.load_data_to_train(path)
X_train, X_pool, y_train, y_pool = data_process.train_test_split(X_train, y_train, test_size=0.5, random_state=42)
print(X_pool.shape)
model = CNN1d()
model = load_model(model, 'models/little_parameter.pkl')
model = model.cuda()


# from flask import render_template, jsoçnify


@app.route("/train",methods=['POST'])
def train():
    global pre_entropy
    print(X_test.shape)

    _, acc = network.test(X_test, y_test, model)
    global validation_standard
    validation_standard = acc
    print(acc)

    predict = torch.ones([1, 4])
    print(X_pool.shape[0])
    for i in range(0, X_pool.shape[0], 16):
        if i + 16 < X_pool.shape[0]:
            tmp_predict, _ = network.test(X_pool[i:i + 16], y_pool[i:i + 16], model)
        else:
            tmp_predict, _ = network.test(X_pool[i:], y_pool[i:], model)
        predict = torch.cat((predict, tmp_predict), dim=0)
    # predict, _ = network.test(X_pool, y_pool, model)
    pre_entropy = entropy(predict[1:], X_pool)
    pre_entropy.sort(key=data_process.takeFirst, reverse=True)
    return jsonify({"a":"123","b":"445"})


@app.route("/post", methods=['POST','GET'])
def post_num():
    num = request.get_json()['value']
    # 这里应该是一个返回id_list,img_list的函数，随便示例一下
    img_lst = []
    id_lst= []
    global pre_entropy
    global X_pool, X_train, y_pool, y_train
    print(datas.shape)
    print(X_pool.shape)
    for i in range(int(num)):
        for signal_num in range(len(datas)):
            if int(pre_entropy[i][-1]) == int(datas[signal_num][-1]):
                print(pre_entropy[i])
                x = np.arange(0, 2000)
                # y = filtedData[x]
                y_fft = datas[signal_num][x]
                y_raw = raw_datas[signal_num][0][x]
                fig = plt.figure(1, figsize=(15, 5))
                plt.subplot(131)
                plt.cla()
                plt.ylim(ymax=0.005)
                plt.title(data_process.label_name[labels[signal_num][0]])
                plt.plot(x, y_fft)
                plt.subplot(132)
                plt.cla()
                plt.title(data_process.label_name[labels[signal_num][0]])
                plt.plot(x, y_raw)
                plt.subplot(133)
                plt.cla()
                plt.bar([0, 1, 2, 3], pre_entropy[i][-2])
                sio = BytesIO()
                fig.savefig(sio, format='png')
                img_base64 = base64.b64encode(sio.getvalue()).decode('utf8')
                img_lst.append(img_base64)
                id_lst.append(datas[signal_num][-1])
                break
        length = X_test.shape[0]
        for signal_num in range(length):

            if int(pre_entropy[i][-1]) == int(X_test[signal_num][0][-1]):
                tmp_data = X_test[signal_num:signal_num+1]
                tmp_label = y_test[signal_num:signal_num+1]
                print(tmp_data.shape)
                print(tmp_label.shape)
                X_train = np.append(X_train, tmp_data, axis=0)
                y_train = np.append(y_train, tmp_label, axis=0)
                y_pool = np.delete(y_test, signal_num, axis=0)
                X_pool = np.delete(X_test, signal_num, axis=0)

                break
    return jsonify({"ids":id_lst,"images":img_lst})


@app.route("/retrain", methods=['POST','GET'])
def retrain():

    ids = request.get_json()['ids']
    labels = request.get_json()['labels']
    print(ids)
    print(labels)
    print(X_train.shape)
    global model, validation_standard
    train_data = train_and_label_process(X_train[:, :, :-1], y_train[:, :-1])
    model = re_train_model(train_data, X_test, y_test, model, 5, validation_standard)

    return jsonify({'msg':'OK'})


@app.route('/test')
def test():
    return "1"


if __name__ == '__main__':
    app.run(debug=True)