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
        entropy_signal += np.log(out[i][j])
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