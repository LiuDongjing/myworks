# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 09:47:27 2017

@author: LiuYangkai
"""

import numpy as np
from scipy import stats

def distance_norm2(feature1, feature2):
    """
    计算欧氏距离
    
    Args:
      feature1: numpy array，一维数组
      feature2: numpy array，一维数组
      
    Returns:
      feature1和feature2的欧式距离
    """
    return np.sqrt(np.power(feature1-feature2, 2).sum())
    

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
    
    def __init__(self, k=3, method='mode'):
        """
        构造函数。
        
        Args:
          k: 邻居的个数
          method: 可以取'max'或者'mean'；'max'表示在k个邻居中label的众数作为预测值，
            用在分类问题上，'mean'的表示在k个邻居中label的平均数作为预测值，用在回归
            问题上。
        """
        if method == 'mode':
            self.method = lambda x:stats.mode(x, axis=None)[0][0] #计算众数
        else:
            self.method = np.mean
        self.k = k
        #(邻居的索引, 邻居与目标点的距离)
        self._neighbors = [(-1, np.inf) for k in range(self.k)] 
        self._neighbors_dist = np.inf #目标点离邻居的最远距离
        
    def _insert_neighbor(self, index, dist):
        """"
        添加一个邻居。
        
        Args:
          index: 邻居的索引。
          dist: 邻居离目标点的距离
          
        Returns:
          所有邻居中离目标点的最大距离。
        """
        for k in reversed(range(self.k)):
            if dist < self._neighbors[k][1]:
                if k+1 < self.k:
                    self._neighbors[k+1] = self._neighbors[k]
                if k == 0:
                    self._neighbors[k] = (index, dist)
            else:
                if k+1 < self.k:
                    self._neighbors[k+1] = (index, dist)
                break
        return self._neighbors[-1][1]
        
    def fit(self, X, y):
        """
        训练函数，实际上就是构造kd-tree。
        
        Args:
          X: numpy array, shape是(n, p)的二维数组，其中n是样本数量，p是样本的维度。
          y: numpy array, shape是(n,)的数组，n是样本数量
        """
        
        self._x = X.copy()
        self._y = y.copy()
        self._root = _TreeNode()
        stack = []
        data = np.array([n for n in range(y.shape[0])])
        stack.append({'node':self._root, 'data':data})
        while stack:
            frame = stack.pop()
            node = frame['node'] #树节点
            index = frame['data'] #样本的索引
            vals = self._x[index, node.split] #样本在分割维度上的数据
            sort_index = vals.argsort(axis=None) #排序，获得索引
            global_index = index[sort_index] #排序后的样本索引
            middle = global_index.shape[0] // 2
            node.index = global_index[middle]
            split = (node.split + 1) % self._x.shape[1]
            if 0 < middle:
                node.left = _TreeNode(split=split)
                left_index = global_index[:middle]
                stack.append({'node':node.left, 'data':left_index})
            if middle+1 < len(global_index):
                node.right = _TreeNode(split=split)
                right_index = global_index[middle+1:]
                stack.append({'node':node.right, 'data':right_index})
            
    def predict(self, X):
        """
        预测。
        
        Args:
          X: 同fit里的X参数
          
        Returns:
          numpy array，shape是(n,)的一维数组，每个元素对应着样本的预测值
        """
        y = np.zeros((X.shape[0],))
        for k in range(X.shape[0]):
            self._neighbors = [(-1, np.inf) for k in range(self.k)]
            self._neighbors_dist = np.inf
            self._search_tree(self._root, X[k])
            index = [e[0] for e in self._neighbors]
            labels = self._y[index]
            y[k] = self.method(labels)
        return y
        
    def _search_tree(self, node, x):
        """
        搜索kd-tree。
        
        Args:
          node: _TreeNode，当前树节点
          x: numpy array， shape是(p,)，一个样本数据，其中p是样本的维度

        """
        if node == None:
            return
        dist = distance_norm2(self._x[node.index], x)
        self._insert_neighbor(node.index, dist)
        if x[node.split] <= self._x[node.index, node.split]:
            self._search_tree(node.left, x)
        else:
            self._search_tree(node.right, x)
        # 剪枝操作
        if abs(x[node.split] - 
            self._x[node.index, node.split]) > self._neighbors_dist:
            return
        # 剪枝失败
        if x[node.split] <= self._x[node.index, node.split]:
            self._search_tree(node.right, x)
        else:
            self._search_tree(node.left, x)
            