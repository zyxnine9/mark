import pandas as pd
import numpy as np
import time
import lightgbm as lgb
from sklearn.metrics import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


def entropy(out):
    pre_entropy = []
    for i in range(len(out)):
        entropy_signal = 0
        for j in range(4):
          entropy_signal += -np.log(out[i][j])*out[i][j]
        pre_entropy.append([entropy_signal, np.argmax(out[i]), out[i]])

    return pre_entropy


def emg_lgb(X_train, X_test, y_train, y_test):
    train_data=lgb.Dataset(X_train,label=y_train)
    validation_data=lgb.Dataset(X_test,label=y_test)
    params={
      'learning_rate':0.1,
      'lambda_l1':0.1,
      'lambda_l2':0.2,
      'max_depth':5,
      'objective':'multiclass',
      'num_class':4,
    }
    lgb_clf=lgb.train(params,train_data,valid_sets=[validation_data])
    y_train_pred = np.argmax(lgb_clf.predict(X_train),axis = 1)
    print('train:')
    print(classification_report(y_train,y_train_pred))
    print('test_score:')
    y_test_prob = lgb_clf.predict(X_test)
    y_test_pred = np.argmax(y_test_prob,axis = 1)
    print(classification_report(y_test,y_test_pred))
    lgb_clf.save_model('models/model.txt')
    return y_test_pred, y_test_prob


def feature_extract(data):
    df_mean=data.mean()
    df_var=data.var()
    df_std=data.std()
    df_rms=np.sqrt(pow(df_mean,2) + pow(df_std,2))
    fengfengzhi = max(data)-min(data)
    df_skew=pd.Series(data).skew()
    df_kurt=pd.Series(data).kurt()
    sum=0
    for i in range(len(data)):
        sum+=np.sqrt(abs(data[i]))
    df_boxing=df_rms / (abs(data).mean())
    df_fengzhi=(max(data)) / df_rms
    df_maichong=(max(data)) / (abs(data).mean())
    df_yudu=max(data)/ pow(sum/(len(data)),2)
    df_qiaodu  =(np.sum([x**4 for x in data])/len(data)) / pow(df_rms,4)
    feature_list = [round(df_rms,3),round(fengfengzhi,3),round(df_fengzhi,3),round(df_boxing,3),round(df_maichong,3),round(df_yudu,3),round(df_qiaodu,3)]
    return feature_list


def py_cpu_nms(dets, thresh):
    """Pure Python NMS baseline."""
    # x1、y1、x2、y2、以及score赋值
    x1 = dets[:, 0]

    x2 = dets[:, 1]

    scores = dets[:, 2]
    # 每一个检测框的面积
    areas = (x2 - x1 + 1)
    # 按照score置信度降序排序
    order = scores.argsort()[::-1]
    keep = []
    # 保留的结果框集合
    while order.size > 0:
        i = order[0]
        # print(i)
        keep.append(i)
        # 保留该类剩余box中得分最高的一个
        # 得到相交区域,左上及右下
        xx1 = np.maximum(x1[i], x1[order[1:]])

        xx2 = np.minimum(x2[i], x2[order[1:]])

        # 计算相交的面积,不重叠时面积为0
        w = np.maximum(0.0, xx2 - xx1 + 1)
        inter = w
        # 计算IoU：重叠面积 /（面积1+面积2-重叠面积）
        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        # print(ovr)
        # 保留IoU小于阈值的box
        inds = np.where(ovr <= thresh)[0]
        # print(inds)
        order = order[inds + 1]
        # 因为ovr数组的长度比order数组少一个,所以这里要将所有下标后移一位
    return keep