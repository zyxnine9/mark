import h5py
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
import math
from sklearn import preprocessing
from sklearn.model_selection import train_test_split


label_name = {0: 'Activate', 1: 'Rest', 2: 'Noisy', 3: 'Unknown'}
train_has_label = [1, 10, 11, 12, 13, 14, 15, 16]


index = 0


def takeFirst(elem):
    return elem[0]


def load_data_to_train(path):
    global index
    f = h5py.File(path, 'r')
    datas = []
    raw_datas = []
    labels = []
    for title in f:

        for group in f[title]:
            for train in f[title][group]:
                for signal_num in f[title][group][train]:
                    fftdata = f[title][group][train][signal_num]['FFT'][0][0][0]
                    rawdata = f[title][group][train][signal_num]['rawEMG'][0][0][0]
                    # print(train, signal)
                    signal_label = len(f[title][group][train][signal_num].attrs['Label'])
                    # print(signal_label)
                    if signal_label == 8:
                        labels.append([0, index])
                    elif signal_label == 4:
                        labels.append([1, index])
                    elif signal_label == 5:
                        labels.append([2, index])
                    elif signal_label == 6:
                        labels.append([3, index])

                    rawdata = rawdata[:2000]
                    fftdata = fftdata[:2000]
                    raw_datas.append(rawdata)
                    datas.append(fftdata)
                    index += 1
            break

    datas_butter = []
    # raw_datas_butter = []
    for i in range(len(datas)):
        filtedData = signal.medfilt(datas[i])
        b, a = signal.butter(4, 0.3, 'lowpass')
        filtedData = signal.filtfilt(b, a, filtedData)
        datas_butter.append(filtedData)

    labels = np.array(labels)
    datas_butter = np.array(datas_butter)
    raw_datas = np.array(raw_datas)
    datas = np.array(datas)

    X_butter_scaler = preprocessing.StandardScaler().fit(datas_butter)
    X_raw_scaler = preprocessing.StandardScaler().fit(raw_datas)

    datas_butter = X_butter_scaler.transform(datas_butter)
    raw_datas = X_raw_scaler.transform(raw_datas)

    ids = [[i] for i in range(index)]

    datas_butter = np.concatenate((datas_butter, ids), axis=1)
    raw_datas = np.concatenate((raw_datas, ids), axis=1)
    datas = np.concatenate((datas, ids), axis=1)

    datas_butter = datas_butter[:, np.newaxis]
    raw_datas = raw_datas[:, np.newaxis]

    datas_con = np.concatenate((datas_butter, raw_datas), axis=1)

    X_train, X_test, y_train, y_test = train_test_split(datas_con, labels, test_size=0.2, random_state=42)

    return datas, raw_datas, labels, datas_butter, X_train, X_test, y_train, y_test



def read_data_from_h5py(path):
    f = h5py.File(path, 'r')
    for t in train_has_label:
        data = []
        label = []
        train = 'Train' + str(t)
        for s in range(1, len(f['HKSR']['hksr003'][train]) + 1):
            signal = 'Signal' + str(s)
            fftdata = f['HKSR']['hksr003'][train][signal]['FFT'][0][0][0]
            data.append(fftdata)
            # print(train, signal)
            signal_label = len(f['HKSR']['hksr003'][train][signal].attrs['Label'])
            if signal_label == 8:
                label.append(0)
            elif signal_label == 4:
                label.append(1)
            elif signal_label == 5:
                label.append(2)
            elif signal_label == 6:
                label.append(3)
        np.save('data_processed/train_' + str(t) + '_datas.npy', data)
        np.save('data_processed/train_' + str(t) + '_labels.npy', label)


def read_unlabeled_data_from_h5py(path):
    f = h5py.File(path, 'r')
    data = []
    for t in range(1, len(f['HKSR']['hksr003'])+1):
        if t in train_has_label:
            continue

        train = 'Train' + str(t)
        for s in range(1, len(f['HKSR']['hksr003'][train]) + 1):
            signal = 'Signal' + str(s)
            fftdata = f['HKSR']['hksr003'][train][signal]['FFT'][0][0][0]
            data.append(fftdata)

    return np.array(data)


def psfeatureTime(data, p1, p2):
    # 均值
    df_mean = data[p1:p2].mean()
    # 方差
    df_var = data[p1:p2].var()
    # 标准差
    df_std = data[p1:p2].std()
    # 均方根
    df_rms = math.sqrt(pow(df_mean, 2) + pow(df_std, 2))
    # 偏度
    df_skew = data[p1:p2].skew()
    # 峭度
    df_kurt = data[p1:p2].kurt()
    sum = 0
    for i in range(p1, p2):
        sum += math.sqrt(abs(data[i]))
        # 波形因子
    df_boxing = df_rms / (abs(data[p1:p2]).mean())
    # 峰值因子
    df_fengzhi = (max(data[p1:p2])) / df_rms
    # 脉冲因子
    df_maichong = (max(data[p1:p2])) / (abs(data[p1:p2]).mean())
    # 裕度因子
    df_yudu = (max(data[p1:p2])) / pow((sum / (p2 - p1)), 2)

    DeadZone = 10e-7
    data_size = p2 - p1
    df_ssc = 0
    df_mavs = 0
    df_wl = 0

    if data_size == 0:
        df_ssc = 0
    else:
        for j in range(p1 + 2, p2):
            difference1 = data[j - 1] - data[j - 2]
            difference2 = data[j - 1] - data[j]
            Sign = difference1 * difference2
            df_mavs = df_mavs + difference1
            df_wl = df_wl + abs(difference1)
            if Sign > 0:
                if abs(difference1) > DeadZone or abs(difference2) > DeadZone:
                    df_ssc = df_ssc + 1
        df_ssc = df_ssc / data_size
        df_mavs = df_mavs / data_size
        df_wl = df_wl / data_size

    featuretime_list = [df_mean, df_rms, df_skew, df_kurt, df_boxing, df_fengzhi, df_maichong, df_yudu, df_ssc, df_mavs,
                        df_wl]
    return featuretime_list


def load_data_prepare(use_medfilt = True, use_butter = True):
    datas = []
    datas_ori = []
    labels = []
    ids = []
    global index
    for number in train_has_label:
        data = np.load('../data_processed/train_' + str(number) + '_datas.npy', allow_pickle=True)
        label = np.load('../data_processed/train_' + str(number) + '_labels.npy', allow_pickle=True)
        for i in range(len(data)):
            datas_ori.append(data[i][:2000])
            labels.append(label[i])
            ids.append('train_' + str(number) + '_signal_' + str(i))
            if use_medfilt:
                filtedData = signal.medfilt(data[i])
            if not use_butter:
                filtedData = data[i]
            b, a = signal.butter(4, 0.3, 'lowpass')
            filtedData = signal.filtfilt(b, a, filtedData) * 2
            datas.append(filtedData[:2000])

    return datas, datas_ori, labels, ids


def data_scaler(datas):
    X_scaler = preprocessing.StandardScaler().fit(datas)
    datas = X_scaler.transform(datas)

    return datas, X_scaler


def add_id_label(datas, labels):
    global index
    data = []
    for i in range(len(datas)):
        labels[i] = np.append(labels[i], index)
        data.append(np.append(datas[i], index))
        index += 1

    return data, labels


def add_id(datas):
    global index
    data = []
    for i in range(len(datas)):
        data.append(np.append(datas[i], index))
        index += 1

    return np.array(data)


def data_to_train_test(datas, labels):
    datas = np.array(datas)
    labels = np.array(labels)
    X_train, X_test, y_train, y_test = train_test_split(datas, labels, test_size=0.2, random_state=42)
    X_train = X_train[:, np.newaxis]
    X_test = X_test[:, np.newaxis]
    return X_train, X_test, y_train, y_test


def show_signal(datas, labels, signal_num):
    x = np.arange(0, len(datas[signal_num]))
    # y = filtedData[x]
    y_raw = datas[signal_num][x]
    print()
    plt.ylim(ymax=0.005)
    plt.title(label_name[labels[signal_num][0]])
    plt.plot(x, y_raw)
    # plt.plot(x,y)

    plt.show()


if __name__ == '__main__':
    datas, raw_datas, labels, datas_butter, X_train, X_test, y_train, y_test = load_data_to_train(path)
    print(X_train.shape)






