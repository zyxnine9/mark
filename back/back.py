#coding:utf-8
from flask import Flask, render_template, jsonify, Response, request
from flask import send_from_directory
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
import scipy.io as scio
from scipy.fftpack import fft
import csv
import pandas as pd
import math


app = Flask(__name__)
CORS(app)

server = False

# 线上路径
if server:
    path = "../../2020MAR-EMG Labeling Data/labeling.h5"
    origin_path = "./datasets/"
else:
    origin_path = "../../2020MAR-EMG Labeling Data/"
    path = "./emg_data.h5"

path_choosed = None
data = None

# validation_standard = 0
# pre_entropy = []
# deleted_X, deleted_y, deleted_raw, deleted_fft = [], [], [], []

info_signal = []
det_signal = []

# name = 'NAAC_s18081064wct_Train15_HandOpen'
# number = 0
# channel = 1

# CNN部分
# datas, raw_datas, labels, datas_butter, X_train, X_test, y_train, y_test = data_process.load_data_to_train(path)
# X_train, X_pool, y_train, y_pool = data_process.train_test_split(X_train, y_train, test_size=0.99, random_state=42)
# print(X_pool.shape, X_train.shape)
# model = CNN1d()
# model = load_model(model, 'models/little_parameter.pkl')
# model = model.cuda()

# feature_data, labels = data_process.load_feature_data('datas/features.npy', 'datas/labels.npy')
# raw_datas, fft_datas = data_process.load_signal_data(path)
#
# X_train, X_test, y_train, y_test = data_process.train_test_split(feature_data, labels, test_size=0.2, random_state=42)
# X_train, X_pool, y_train, y_pool = data_process.train_test_split(X_train, y_train, test_size=0.997, random_state=42)
# raw_train, raw_test, raw_labels, _ = data_process.train_test_split(raw_datas, labels, test_size=0.2, random_state=42)
# raw_train, raw_pool, _, _ = data_process.train_test_split(raw_train, raw_labels, test_size=0.997, random_state=42)
# fft_train, fft_test, _, _ = data_process.train_test_split(fft_datas, labels, test_size=0.2, random_state=42)
# fft_train, fft_pool, _, _ = data_process.train_test_split(fft_train, raw_labels, test_size=0.997, random_state=42)

# from flask import render_template, jsoçnify


# @app.route("/train",methods=['POST'])
def train(name, number, channel):
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
    # global pre_entropy
    lgb_clf = lgb.Booster(model_file='models/model.txt')
    # y_test_prob = lgb_clf.predict(X_test)
    # y_test_pred = np.argmax(y_test_prob, axis=1)
    # print(classification_report(y_test, y_test_pred))
    #
    # y_pool_prob = lgb_clf.predict(X_test)
    # pre_entropy = train_features.entropy(y_pool_prob)

    global info_signal, det_signal
    info_signal = []
    det_signal = []

    print(name)
    signal = data[name][0][number]
    count = {0: 0, 1: 0}
    for length in {2000, 4000, 6000}:
        for i in range(0, signal.shape[0], length // 4):
            if i + length > signal.shape[0]:
                break
            tmp_feature = np.array(train_features.feature_extract(signal[i:i + length, channel]))
            tmp_feature = tmp_feature[np.newaxis, :]
            y_test_prob = lgb_clf.predict(tmp_feature)
            y_test_pred = np.argmax(y_test_prob, axis=1)
            y_test_pred = int(y_test_pred)

            if y_test_pred == 0 or y_test_pred == 1:
                count[y_test_pred] += 1
                det_signal.append(signal[i:i + length, channel])
                info_signal.append([i, i + length, y_test_prob[0][0], y_test_pred])
    print(count)
    print("success")
    # return jsonify({"a":"123","b":"445"})


@app.route("/post", methods=['POST','GET'])
def post_num():
    # change by zyx 
    # 测试接口
    name = request.get_json()['groupName']
    number = request.get_json()['chosenSignalNumber']
    channel = request.get_json()['chosenSignalChannel']
    print(channel)
    print(number)
    f = csv.reader(open('groups.csv', 'r', encoding='utf-8'))
    grouplist = []
    raw_lst = []
    fft_lst = []
    title_lst = []
    id_lst = []
    for i in f:
        if len(i) == 0:
            continue
        grouplist.append(i[0])
    print(grouplist)
    begin_index = 0
    end_index = len(open('labels_csv.csv').readlines())-1 if os.path.exists('labels_csv.csv') else 0
    if path_choosed+name+str(number)+str(channel) in grouplist: # 判断之前是否detect过
        file = pd.read_csv('./labels_csv.csv')
        f = pd.DataFrame(file)
        print(f.head())
        flag = False
        for i, info in enumerate(f.itertuples()):

            if getattr(info, 'group_name') == name and getattr(info, 'number') == number and getattr(info, 'channel') == channel and getattr(info, 'file_name') == path_choosed:

                if math.isnan(getattr(info, 'label')) and flag is False:
                    begin_index = i
                    flag = True
            else:
                if flag:
                    end_index = i
                    break
        print(begin_index, end_index)
        for i in range(begin_index, end_index):

            tmp_signal = data[name][0][number][int(f.loc[i, "start_time"]):int(f.loc[i, "end_time"]), channel]

            raw_lst.append(tmp_signal.tolist())
            fft_signal = fft(tmp_signal)
            P2 = abs(fft_signal / len(fft_signal))
            P1 = P2[1:len(P2) // 2 + 1]
            P1[2:-1] = 2 * P1[2:-1]
            # img_lst.append(img_base64)
            fft_lst.append(P1.tolist())
            result = "from_csv"
            title_lst.append(name + '_0_' + str(number) + '_channel' + str(channel) + '_start' + str(
                int(f.loc[i, "start_time"])) + '_end' + str(f.loc[i, "end_time"]) + result)
            id_lst.append(str(i))

    else:
        with open('groups.csv', 'a+', newline='')as f:
            writer = csv.writer(f)
            tmp = path_choosed+name+str(number)+str(channel)
            print(tmp)
            writer.writerow([tmp])
            f.close()
        train(name, number, channel)
        keep = train_features.py_cpu_nms(np.array(info_signal), 0.2)
        begin_index = len(open('labels_csv.csv').readlines())-1 if os.path.exists('labels_csv.csv') else 0
        if os.path.exists('labels_csv.csv'):
            file = pd.read_csv('./labels_csv.csv')
            df = pd.DataFrame(file)
        else:
            df = pd.DataFrame(columns=['file_name','group_name', 'number', 'channel', 'start_time', 'end_time', 'label'])

        for i in keep:

            df = df.append({"file_name":path_choosed, "group_name": name, "number":number, "channel":channel, "start_time":info_signal[i][0], "end_time":info_signal[i][1]}, ignore_index=True)

        print(df.head())
        df.to_csv('./labels_csv.csv', index=False)

        for num, i in enumerate(keep):
            fft_signal = fft(det_signal[i])
            P2 = abs(fft_signal / len(fft_signal))
            P1 = P2[1:len(P2) // 2 + 1]
            P1[2:-1] = 2 * P1[2:-1]
            # img_lst.append(img_base64)
            raw_lst.append(det_signal[i].tolist())
            fft_lst.append(P1.tolist())
            result = "_rest" if info_signal[i][3] else "_activate"
            title_lst.append(name + '_0_' + str(number) + '_channel' + str(channel) + '_start' + str(
                info_signal[i][0]) + '_end' + str(info_signal[i][1]) + result)
            id_lst.append(str(num+begin_index))



    # 这里应该是一个返回id_list,img_list的函数，随便示例一下
    # img_lst = []

    # global pre_entropy
    # global X_pool, X_train, y_pool, y_train, deleted_X, deleted_y, deleted_raw, deleted_fft, raw_pool, fft_pool
    # print(X_pool.shape)
    # deleted_X, deleted_y, deleted_raw, deleted_fft = [], [], [], []
    # selected, selected_entropy = data_process.select(pre_entropy, 0, 10)
    # deleted_X, deleted_y, deleted_raw, deleted_fft, X_pool, y_pool, raw_pool, fft_pool = data_process.delete_from_pool(X_pool, y_pool, raw_pool, fft_pool, selected)
    # print(X_pool.shape)

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

    return jsonify({"ids":id_lst[:10], "raw_datas": raw_lst[:10], "fft_datas": fft_lst[:10], "title": title_lst[:10]})


@app.route("/retrain", methods=['POST','GET'])
def retrain():
    ids = request.get_json()['ids']
    labels = request.get_json()['labels']
    print(ids)
    print(labels)
    file = pd.read_csv('./labels_csv.csv')
    f = pd.DataFrame(file)

    print("retrain:")
    print(f.head())

    for i, id in enumerate(ids):
        f.loc[int(id), "label"] = labels[i]
    print(f.head())
    f.to_csv('./labels_csv.csv', index=False)
    # global X_train, y_train, raw_train, fft_train
    # print(X_train.shape)
    # X_train, y_train, raw_train, fft_train = data_process.add_to_train(deleted_X, deleted_y, deleted_raw, deleted_fft, X_train, y_train, raw_train, fft_train)
    # print(X_train.shape)
    # train_features.emg_lgb(X_train, X_test, y_train, y_test)
    # global model, validation_standard
    # train_data = train_and_label_process(X_train[:, :, :-1], y_train[:, :-1])
    # model = re_train_model(train_data, X_test, y_test, model, 5, validation_standard)

    return jsonify({'msg':'OK'})


@app.route('/files', methods=['GET'])
def test():
    print("this is files")
    if server:
        files = os.listdir('./datasets') #线上路径
    else:
        files = os.listdir('../../2020MAR-EMG Labeling Data') # 线下调试路径
    return jsonify({'files':files})


@app.route('/postfile',methods=['POST'])
def post_file():
    print("this is postfile")
    file_ = request.files.get('dataset')
    print(type(file_))
    name = file_.filename
    file_.save("./datasets/{}".format(name))
    return jsonify({'msg':'OK'})


@app.route('/group',methods=['POST'])
def group():
    print(request.get_json()['dataset_name'])
    global data, path_choosed
    path_choosed = request.get_json()['dataset_name']
    data = scio.loadmat(origin_path+path_choosed)

    return jsonify({'group_name':list(data.keys())})


@app.route('/download')
def download():
    return send_from_directory(directory="./", filename="labels_csv.csv", as_attachment=True)


@app.route('/number', methods=['GET'])
def number():
    group_name = request.args.get('groupName')
    print("number", len(data[group_name][0]))
    return jsonify({"signalNumber":len(data[group_name][0])-1})


if __name__ == '__main__':
    app.run(debug=True)
