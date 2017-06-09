# -*- coding: utf-8 -*-
"""
感知器的简易实现。

@author: LiuYangkai
"""
import numpy as np

class Perceptron(object):
    """
    感知器算法类。
    """
    
    def __init__(self, eta=0.05):
        """
        构造函数。
        
        Args:
          eta: 学习速率。
        """
        self.eta = eta

    def fit(self, X, Y):
        """
        训练函数。
        
        Args:
          X: 训练数据集，numpy array，NxD的矩阵(N是数据量，D是特征维数)。
          Y: 标签，numpy array，Nx1的矩阵，取值1或-1.
        """
        X = np.matrix(X)
        Y = np.matrix(Y)
        W = np.matrix(np.zeros([X.shape[1], 1]))
        b = np.matrix(np.zeros([1,1]))
        flag = False
        while not flag:
            flag = True
            for x, y in zip(X, Y):
                if ((y*x*W) + y*b <= 0).any():
                    flag = False
                    W = W + (self.eta*y*x).T
                    b = b + self.eta*y
        self.W = W
        self.b = b

    def predict(self, X):
        """
        预测输入样本的标签。
        
        Args:
          X: 测试样本集，numpy.array，NxD的矩阵
          
        Returns:
          测试样本标签，numpy.array，Nx1的矩阵。
        """
        p = X * self.W + self.b
        p[p<=0] = -1
        p[p>0] = 1
        return p.A
        
    def get_params(self):
        """
        返回训练好的参数。
        
        Returns:
          tuple。即(W, b)
        """
        return (self.W, self.b)