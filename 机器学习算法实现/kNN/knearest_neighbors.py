# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 09:47:27 2017

@author: LiuYangkai
"""
import numpy as np

class _TreeNode(object):
    """
    kd-tree的节点。
    """
    
    def __init__(self, split=0, index=-1):
        """
        构造函数。
        
        Args:
          split: 分裂的维度的索引。
          index: 该节点存储的数据，也就是样本的索引，-1表示未指向任何样本。
        """
        self.split = split
        self.index = index
        self.left = None #左子树
        self.right = None #右子树

class KNearestNeighbors(object):
    """
    kNN算法
    """
    
    def __init__(self, k=3, method='max'):
        """
        构造函数。
        
        Args:
          k: 邻居的个数
          method: 可以取'max'或者'mean'；'max'表示在k个邻居中label的众数作为预测值，
            用在分类问题上，'mean'的表示在k个邻居中label的平均数作为预测值，用在回归
            问题上。
        """
        if method == 'max':
            self.method = np.max
        else:
            self.method = np.mean
        self.k = k
        
    def fit(self, X, y):
        """
        训练函数，实际上就是构造kd-tree。
        
        Args:
          X: numpy array, shape是(n, p)的二维数组，其中n是样本数量，p是样本的维度。
          y: numpy array, shape是(n,)的数组，n是样本数量
        """
        
        self._x = np.matrix(X)
        self._y = np.matirx(y)
        self._root = _TreeNode()
        remain = [True for n in range(y.shape[0])]
        split = 0
        while not np.any(remain):
            vals = self._x[remain, split]
            remain_index = np.argsort(remain, axis=None)
            #用于将局部数据集的索引映射到全局数据集索引
            remain_index = remain_index[::-1] 
            median = -1
            if vals.shape[0]%2 != 0:
                t = vals.argsort(axis=0)
                median = t[(vals.shape[0]+1)/2,0]
                median = remain_index[median]
            
            split = (split + 1) % X.shape[1]