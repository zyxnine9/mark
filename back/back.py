#coding:utf-8
from flask import Flask, render_template, jsonify, Response, request
from flask_cors import CORS
# from PIL import Image
import json, os
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import data_process
#from network import *
import lightgbm as lgb
from sklearn.metrics import *
from sklearn.mixture import GaussianMixture
from sklearn.cluster import k_means
import train_features


app = Flask(__name__)
CORS(app)
# path = "../../2020MAR-EMG Labeling Data/labeling.h5"
path = "./emg_data.h5"
validation_standard = 0
pre_entropy = []
deleted_X, deleted_y, deleted_raw, deleted_fft = [], [], [], []

# CNN部分
# datas, raw_datas, labels, datas_butter, X_train, X_test, y_train, y_test = data_process.load_data_to_train(path)
# X_train, X_pool, y_train, y_pool = data_process.train_test_split(X_train, y_train, test_size=0.99, random_state=42)
# print(X_pool.shape, X_train.shape)
# model = CNN1d()
# model = load_model(model, 'models/little_parameter.pkl')
# model = model.cuda()

feature_data, labels = data_process.load_feature_data('datas/features.npy', 'datas/labels.npy')
raw_datas, fft_datas = data_process.load_signal_data(path)

X_train, X_test, y_train, y_test = data_process.train_test_split(feature_data, labels, test_size=0.2, random_state=42)
X_train, X_pool, y_train, y_pool = data_process.train_test_split(X_train, y_train, test_size=0.997, random_state=42)
raw_train, raw_test, raw_labels, _ = data_process.train_test_split(raw_datas, labels, test_size=0.2, random_state=42)
raw_train, raw_pool, _, _ = data_process.train_test_split(raw_train, raw_labels, test_size=0.997, random_state=42)
fft_train, fft_test, _, _ = data_process.train_test_split(fft_datas, labels, test_size=0.2, random_state=42)
fft_train, fft_pool, _, _ = data_process.train_test_split(fft_train, raw_labels, test_size=0.997, random_state=42)

# from flask import render_template, jsoçnify


@app.route("/train",methods=['POST'])
def train():
    # CNN部分
    # global pre_entropy, model
    # model = load_model(model, 'models/little_parameter.pkl')
    # model = model.cuda()
    # _, acc = network.test(X_test, y_test, model)
    # global validation_standard
    # validation_standard = acc
    # print(acc)
    #
    # predict = torch.ones([1, 4])
    # for i in range(0, X_pool.shape[0], 16):
    #     if i + 16 < X_pool.shape[0]:
    #         tmp_predict, _ = network.test(X_pool[i:i + 16], y_pool[i:i + 16], model)
    #     else:
    #         tmp_predict, _ = network.test(X_pool[i:], y_pool[i:], model)
    #     predict = torch.cat((predict, tmp_predict), dim=0)
    # # predict, _ = network.test(X_pool, y_pool, model)
    # pre_entropy = entropy(predict[1:], X_pool)
    # pre_entropy.sort(key=data_process.takeFirst, reverse=True)
    # pre_entropy = pre_entropy[:8]+pre_entropy[-5:]
    # print(len(pre_entropy))
    global pre_entropy
    lgb_clf = lgb.Booster(model_file='models/model.txt')
    y_test_prob = lgb_clf.predict(X_test)
    y_test_pred = np.argmax(y_test_prob, axis=1)
    print(classification_report(y_test, y_test_pred))

    y_pool_prob = lgb_clf.predict(X_test)
    pre_entropy = train_features.entropy(y_pool_prob)

    return jsonify({"a":"123","b":"445"})


@app.route("/post", methods=['POST','GET'])
def post_num():
    num = request.get_json()['value']
    # 这里应该是一个返回id_list,img_list的函数，随便示例一下
    # img_lst = []
    raw_lst = []
    fft_lst = []
    title_lst = []
    id_lst= []
    global pre_entropy
    global X_pool, X_train, y_pool, y_train, deleted_X, deleted_y, deleted_raw, deleted_fft, raw_pool, fft_pool
    print(X_pool.shape)
    deleted_X, deleted_y, deleted_raw, deleted_fft = [], [], [], []
    selected, selected_entropy = data_process.select(pre_entropy, 0, 10)
    deleted_X, deleted_y, deleted_raw, deleted_fft, X_pool, y_pool, raw_pool, fft_pool = data_process.delete_from_pool(X_pool, y_pool, raw_pool, fft_pool, selected)
    print(X_pool.shape)
    for i in range(int(num)):
        # print(selected_entropy[i])
        # x_fft = np.arange(0, len(deleted_fft[i]))
        # x_raw = np.arange(0, len(deleted_raw[i]))
        # # y = filtedData[x]
        # y_fft = deleted_fft[i][x_fft]
        # y_raw = deleted_raw[i][x_raw]
        # fig = plt.figure(1, figsize=(15, 5))
        # plt.subplot(131)
        # plt.cla()
        # plt.ylim(ymax=0.005)
        # plt.title(data_process.label_name[deleted_y[i]])
        # plt.plot(x_fft, y_fft)
        # plt.subplot(132)
        # plt.cla()
        # plt.title(data_process.label_name[deleted_y[i]])
        # plt.plot(x_raw, y_raw)
        # plt.subplot(133)
        # plt.cla()
        # plt.bar([0, 1, 2, 3], selected_entropy[i][-1])
        # sio = BytesIO()
        # fig.savefig(sio, format='png')
        # img_base64 = base64.b64encode(sio.getvalue()).decode('utf8')
        # img_lst.append(img_base64)
        raw_lst.append(deleted_raw[i].tolist())
        fft_lst.append(deleted_fft[i].tolist())
        title_lst.append(data_process.label_name[deleted_y[i]])
        id_lst.append(i)

    return jsonify({"ids":id_lst, "raw_datas": raw_lst, "fft_datas": fft_lst, "title:": title_lst})


@app.route("/retrain", methods=['POST','GET'])
def retrain():
    ids = request.get_json()['ids']
    labels = request.get_json()['labels']
    print(ids)
    print(labels)
    global X_train, y_train, raw_train, fft_train
    print(X_train.shape)
    X_train, y_train, raw_train, fft_train = data_process.add_to_train(deleted_X, deleted_y, deleted_raw, deleted_fft, X_train, y_train, raw_train, fft_train)
    print(X_train.shape)
    train_features.emg_lgb(X_train, X_test, y_train, y_test)
    # global model, validation_standard
    # train_data = train_and_label_process(X_train[:, :, :-1], y_train[:, :-1])
    # model = re_train_model(train_data, X_test, y_test, model, 5, validation_standard)

    return jsonify({'msg':'OK'})


@app.route('/test')
def test():
    return jsonify({'msg':'OK'})


if __name__ == '__main__':
    app.run(debug=True)
