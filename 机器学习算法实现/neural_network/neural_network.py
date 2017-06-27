# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:38:48 2017

@author: LiuYangkai
"""
import sys
import numpy as np

class Activation(object):
    """
    激活函数的基类
    """
    
    def forward(self, data):
        """
        计算f(data)
        """
        self.data = data
        return data
        
    def backward(self):
        """
        计算f'(data)
        """
        return np.matrix(np.zeros(self.data.shape))
        
class ReLU(Activation):
    """
    ReLU激活函数
    """
    
    def forward(self, data):
        """
        """
        self.data = data
        cp = data.copy()
        cp[cp < 0] = 0
        return cp
        
    def backward(self):
        """
        """
        cp = self.data.copy()
        cp[cp < 0] = 0
        cp[cp > 0] = 1
        return cp

class Layer(object):
    """
    神经网络的一层，包含了weight和激活函数。
    """
    
    def __init__(self, shape, activation='relu', eta=0.1, alpha=0,
                 epsilon=0, random_init=True):
        """
        构造函数。
        
        Args:
          shape: (in, out), 有两个值的元组，in指定了上一层神经元个数，out指定了
            本层神经元个数。
          activation: 激活函数，默认是ReLU(目前只支持ReLU)。
          eta: 学习速率。
          alpha: momentum中的alpha参数，取值在(0, 1)之间；置为0表示不使用alpha。
          epsilon: weight decay中的epsilon参数，取值在(0, 1)之间；置为0表示不使用
            weight decay。
          random_init: 是否用随机数初始化权重。
        """
        if random_init:
            self.weight = np.matrix(np.random.rand(*shape))
        else:
            self.weight = np.matrix(np.zeros(shape))
        self.activation = ReLU()
        self.alpha = alpha
        self.epsilon = epsilon
        if alpha > 0:
            self.prev_delta_weight = np.matrix(np.zeros(shape));
        
    def forward(self, Y):
        """
        前向传播。
        
        Args:
          Y: 前一层网络的输出，也就是本层网络的输入。是个二维矩阵，一行代表一个样本，列
            数对应着上一层神经元的个数。
          
        Returns:
          本层网络的输出，是个二维矩阵，一行是一个样本，列数对应着本层网络的神经元个数。
        """
        net = Y * self.weight
        y_out = self.activation.forward(net)
        self.Y = Y
        return y_out
        
    def backward(self, delta):
        """
        反向传播。
        
        Args:
          delta: 下一层网络backward得到的sensitivity。是个二维矩阵，行数对应着样本
            数，列数对应着本层神经元的个数。
        
        Returns:
          上一层网络的delta，也就是sensitivity。二维矩阵，行数对应着样本数，列数对应
          着上层网络的神经元个数。
        """
        dot = np.multiply(delta, self.activation.backward())
        prev_delta = dot * self.weight.T
        self.delta_weight = self.Y.T * dot;
        return prev_delta
        
    def update(self):
        """
        更新权重。
        """
        self.weight -= self.eta * self.delta_weight
        if self.alpha > 0:
            self.weight -= self.alpha * self.prev_delta_weight
            self.prev_delta_weight = self.delta_weight
        if self.epsilon > 0:
            self.weight = (1 - self.epsilon) * self.weight
            
class Loss(object):
    """
    神经网络的loss层
    """
    def __init__(self, truth=None):
        """
        构造函数。
        
        Args:
          truth: 真实标签。后面作为公开的属性可直接修改。
        """
        self.truth = truth
    
    def forward(self, data):
        """
        前向传播。
        
        Args:
          data: 预测值。
        """
        pass
    
    def backward(self):
        """
        反向传播。
        """
        pass
    
class SoftmaxLoss(Loss):
    """
    softmax loss。
    """
    def fordward(self, data):
        c = np.repeat(np.max(data, 1), data.shape[1], 1)
        data -= c
        data = np.exp(data)
        s = np.repeat(np.sum(data, 1), data.shape[1], 1)
        p = data / s
        self.p = p
        logp = np.log(p)
        return -np.sum(np.multiply(self.truth, logp), 1)
        
    def backward(self):
        return self.p - self.truth
        
class Network(object):
    """
    神经网络算法。
    """
    
    def __init__(self, dims, loss='softmax'):
        """
        构造函数。
        
        Args:
          dims: list，从前往后指定了每一层网络的神经元个数。dims[0]是输入特征的维度数，
            dims[-1]是输出值的维度数。
          loss: loss函数，默认是softmax(目前只支持softmax)。
        """
        layers = []
        for k in range(1, len(dims)):
            layers.append(Layer((dims[k-1], dims[k])))
        self.layers = layers
        self.loss = SoftmaxLoss()
        
    def forward(self, X, y):
        """
        前向传播。
        
        Args:
          X: (n, dim)的array，n是样本的数量，dim是特征的数量。
          y: (n, odim)的数组，n是样本数量，odim是标签的数量。
          
        Returns:
          loss的平均值。
        """
        X = np.matrix(X)
        y = np.matrix(y)
        if len(y.shape) < 2:
            # 当标签只有一维时，array转matrix后shape会反过来
            y = y.T
        self.loss.truth = y
        
        # 前向传播
        feed = X
        for e in self.layers:
            feed = e.forward(feed)
        loss = self.loss.fordward(feed)
        return np.mean(loss)
        
    def backward(self):
        """
        反向传播。
        """
        delta = self.loss.backward()
        for e in reversed(self.layers):
            delta = e.backward(delta)

    def fit(self, X, y):
        """
        拟合数据。
        
        Args:
          X: (n, dim)的array，n是样本的数量，dim是特征的数量。
          y: (n, odim)的数组，n是样本数量，odim是标签的数量。
        """
        # 前向传播
        mean_loss = self.forward(X, y)
        print('平均loss:%f'%mean_loss)
        
        # 反向传播
        self.backward()
            
        # update参数
        for e in self.layers:
            e.update()
            
    def predict(self, X):
        """
        预测样本的标签。
        
        Args:
          X: [n, dim]的array，n是样本的数量，dim是特征数量。
          
        Returns:
          [n, odim]的array，n是样本的数量，odim是标签的数量。
        """
        X = np.matrix(X)
        feed = X
        for e in self.layers:
            feed = e.forward(feed)
        return feed.A
        
def check_algorithm(epsilon=1e-4):
    """
    检验神经网络算法是否正确实现。
    
    Args:
      epsilon: 检验算法中用到的微小增量。
    """
    if epsilon > 1e-4:
        epsilon = 1e-4
    x = np.random.rand(1, 4)
    y = np.array([[1, 0, 0]])
    net = Network([4, 8, 3])
    net.forward(x, y)
    net.backward()
    k = 0
    for layer in net.layers:
        k += 1
        for i in range(layer.weight.shape[0]):
            for j in range(layer.weight.shape[1]):
                layer.weight[i, j] += epsilon
                loss_plus = net.forward(x, y)
                layer.weight[i, j] -= 2*epsilon
                loss_minus = net.forward(x, y)
                delta = layer.delta_weight[i, j]
                delta_calc = (loss_plus - loss_minus)/(2*epsilon)
                if abs(delta - delta_calc) < 1e-4:
                    print('Layer%d_W%d%d: %f(delta), %f(delta_calc), pass.'%
                        (k, i, j, delta, delta_calc))
                else:
                    print('Layer%d_W%d%d: %f(delta), %f(delta_calc), fail.'%
                        (k, i, j, delta, delta_calc), file=sys.stderr)
                    
# 
if __name__ == '__main__':
    check_algorithm()