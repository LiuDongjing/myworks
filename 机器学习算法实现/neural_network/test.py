import numpy as np
from datetime import datetime
from sklearn.datasets import fetch_mldata
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn import preprocessing
from neural_network import Network

lb = preprocessing.LabelBinarizer()
lb.fit([k for k in range(10)])

mnist = fetch_mldata('MNIST original', data_home='../datasets/MNIST')
min_max_scaler = preprocessing.MinMaxScaler()
data = min_max_scaler.fit_transform(mnist.data.astype('float64'))
X_train, X_test, y_train, y_test = train_test_split(
    data, mnist.target)
print('test:', X_test.shape)
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train)
print('train:', X_train.shape)
print('validation:', X_val.shape)
print('label shape', y_val.shape)
img = np.random.choice(range(X_train.shape[0]))
img = X_train[img].reshape((28, 28))
plt.imshow(img, interpolation='nearest')
plt.show()

y_train = lb.transform(y_train)
net = Network([784, 300, 10])
batch_size = 2000
max_acc = 0
for epoc in range(100):
    time_start = datetime.now()
    for left in range(0, X_train.shape[0], batch_size):
        right = min(left+batch_size, X_train.shape[0])
        X = X_train[left:right, :]
        y = y_train[left:right, :]
        net.fit(X, y)
        y_pred = net.predict(X_val)
        y_pred = y_pred.argmax(1).reshape((-1,))
        eql = y_pred == y_val
        acc = np.sum(eql)/eql.shape[0]
        max_acc = max(max_acc, acc)
        print('validation accuracy: %f(now), %f(max)' % (acc, max_acc))
    print('epoc: %d, time: %fs.'%(epoc, (datetime.now()-time_start).seconds))