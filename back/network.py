import torch
from torch import nn, optim
import numpy as np
from torch.autograd import Variable
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset, TensorDataset


class CNN1d(nn.Module):
    def __init__(self):
        super(CNN1d, self).__init__()

        self.conv1 = nn.Sequential(nn.Conv1d(2, 4, kernel_size=2, stride=1),
                                   nn.BatchNorm1d(4),
                                   nn.ReLU(),
                                   nn.MaxPool1d(2))

        self.conv2 = nn.Sequential(nn.Conv1d(4, 8, kernel_size=2, stride=1),
                                   nn.BatchNorm1d(8),
                                   nn.ReLU(),
                                   nn.MaxPool1d(2))

        self.conv3 = nn.Sequential(nn.Conv1d(8, 32, kernel_size=2, stride=1),
                                   nn.BatchNorm1d(32),
                                   nn.ReLU(),
                                   nn.MaxPool1d(2))

        self.conv4 = nn.Sequential(nn.Conv1d(32, 64, kernel_size=2, stride=1),
                                   nn.BatchNorm1d(64),
                                   nn.ReLU(),
                                   nn.MaxPool1d(2))

        '''self.l_1 =  nn.Sequential(nn.AdaptiveMaxPool1d(1),                                
                                nn.Linear(1,1),                                
                                nn.ReLU()) 
        self.f_l1 = nn.Sequential(nn.Linear(108,16),                                
                                nn.Dropout(0.5),                                
                                nn.ReLU())
        self.f_l2 = nn.Linear(16,1)'''

        self.f1 = nn.Sequential(nn.Linear(7936, 256),
                                nn.Dropout(0.5),
                                nn.ReLU())
        self.f2 = nn.Sequential(nn.Linear(256, 16),
                                nn.Dropout(0.5),
                                nn.ReLU())
        self.f3 = nn.Linear(16, 4)

    def forward(self, x):
        x = self.conv1(x)
        # x1 = self.l_1(x)
        x = self.conv2(x)
        # x2 = self.l_1(x)
        x = self.conv3(x)
        # x3 = self.l_1(x)
        x = self.conv4(x)
        # x4 = self.l_1(x)

        x = x.view(x.size()[0], -1)
        x = self.f1(x)
        x = self.f2(x)

        return self.f3(x)


def train_and_label_process(X, y):
    X_train, y_train = torch.Tensor(X), torch.Tensor(y)
    train_data = TensorDataset(X_train, y_train)
    return train_data


def train(train_data, X_test, y_test, epoch = 10):
    model = CNN1d()
    model = model.train()
    # model = TextCNN()
    # 选择损失函数
    Loss_target = nn.CrossEntropyLoss()
    Loss_mse = nn.MSELoss()
    # Loss = nn.BCELoss()
    # Loss = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    validation_standard = 0

    for epoch in range(epoch):
        acc = []
        losssum = []
        batch_train = DataLoader(dataset=train_data, batch_size=16, shuffle=True)
        for i, data in enumerate(batch_train):
            x, y = data
            y = y.long()
            y = y[:, 0]
            x = Variable(x)
            x = Variable(x)
            out = model(x)
            loss = Loss_target(out, y)
            # loss = Loss_mse(preloss, targetloss)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # print(torch.argmax(out,-1), y)
            accracy = np.mean((torch.argmax(out, -1) == y).numpy())
            acc.append(accracy)
            losssum.append(int(loss))
        acc = np.array(acc)
        losssum = np.array(losssum)

        _,validation_pre = test(X_test, y_test, model)
        print()
        if validation_pre > validation_standard:
            validation_standard = validation_pre
            print("save_model")
            torch.save(model.state_dict(), 'models/parameter'+str(epoch)+'.pkl')
        print('loss: ', np.mean(losssum), '   accracy: ', np.mean(acc), '   validation:', validation_pre)
    return model


def test(X, y, model):
    X_test, y_test = torch.Tensor(X), torch.Tensor(y)

    model = model.eval()
    with torch.no_grad():
        predict = model(Variable(X_test.cuda()))

    acc = np.mean((torch.argmax(predict.cpu(), -1) == y_test[:, 0]).numpy())
    predict = predict.cpu()
    torch.cuda.empty_cache()
    return predict, acc


def entropy(out, X):
    out = F.softmax(out, dim=1)
    pre_entropy = []
    for i in range(len(out)):
        entropy_signal = 0
        for j in range(4):
            entropy_signal += torch.log(out[i][j])
        pre_entropy.append([float(entropy_signal), float(torch.argmax(out[i], -1)), list(out[i]), float(X[i][0][-1])])

    return pre_entropy


def load_model(model, path):
    model.load_state_dict(torch.load(path))
    return model


def re_train_model(train_data, X_test, y_test, model, epoch=10, validation_standard=0):

    model = model.train()
    # model = TextCNN()
    # 选择损失函数
    Loss_target = nn.CrossEntropyLoss()
    Loss_target = Loss_target.cuda()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(epoch):
        acc = []
        losssum = []
        batch_train = DataLoader(dataset=train_data, batch_size=16, shuffle=True)
        for i, data in enumerate(batch_train):
            x, y = data
            y = y.long()
            y = y[:, 0]
            x = Variable(x)
            x = Variable(x)
            x = x.cuda()
            y = y.cuda()
            out = model(x)
            loss = Loss_target(out, y)
            # loss = Loss_mse(preloss, targetloss)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # print(torch.argmax(out,-1), y)
            accracy = np.mean((torch.argmax(out.cpu(), -1) == y.cpu()).numpy())
            acc.append(accracy)
            losssum.append(int(loss))
        acc = np.array(acc)
        losssum = np.array(losssum)

        _,validation_pre = test(X_test, y_test, model)
        print()
        if validation_pre > validation_standard:
            validation_standard = validation_pre
            print("save_model")
            torch.save(model.state_dict(), 'models/little_parameter.pkl')
        print('loss: ', np.mean(losssum), '   accracy: ', np.mean(acc), '   validation:', validation_pre)
    return model
