# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 10:13:53 2017

@author: LiuYangkai
"""
import numpy as np
from scipy import stats

class _Node(object):
    """
    树节点。
    """
    
    def __init__(self, left=None, right=None, split_feature=-1,
                 split_value=None, index=None):
        """
        构造函数。
        
        Args:
          left: None或者_Node对象，左节点
          right: None或者_Node对象，右节点
          split_feature: int类型，在features[split_feature]上进行分割
          split_value: object对象，features[split_feature] <= split_value的样本，
            归入左节点，否则归入右节点
          index: 归入该节点的样本索引；建树和剪枝的时候用到，剪枝完成后就不用了
        """
        self.left = left
        self.right = right
        self.split_feature = split_feature
        self.split_value = split_value
        self.index = index
        self.leaf_loss = np.inf # 该节点作为叶节点时的loss值
        self.label = None # 叶节点的标签
        self.alpha = np.inf # 剪枝时计算的alpha
    
    def copy(self):
        """
        复制该节点，包括该节点的子节点
        
        Returns:
          _Node类型，该节点的副本。
        """
        left = None
        right = None
        if self.left is not None:
            left = self.left.copy()
        if self.right is not None:
            right = self.right.copy()
        node = _Node(left=left, right=right)
        node.alpha = self.alpha
        node.split_feature = self.split_feature
        node.split_value = self.split_value
        node.label = self.label
        node.leaf_loss = self.leaf_loss
        if self.index is not None:
            node.index = self.index.copy()
        return node
        
class CART(object):
    """
    Classfication And Regression Tree. 
    """
    
    def __init__(self, regression=False, validation_percentage=0.2):
        """
        构造函数
        
        Args:
          regression: True或者False，True对应着回归树，False对应着分类树
          validation_percentage: 剪枝的过程中，用于validation的数据占训练数据的百分比
        """
        self.val_perc = validation_percentage
        self.regss = regression
        if regression:
            # 样本标签的平均值作为叶节点的输出
            self._method = np.mean
            
            # 对子树打分
            self._loss
        else:
            # 样本标签的众数作为叶节点的输出
            self._method = lambda x:stats.mode(x, axis=None)[0][0]
            self._loss
        self._root = None #树的根节点
        
    def fit(self, X, y):
        """
        训练模型
        
        Args:
          X: shape是(N, T)的numpy.array，N是样本的数量，T是特征的维度数。
          y: shape是(N,)的numpy.array，N是样本对应的标签数量
        """
        index_all = [k for k in range(X.shape[0])]
        index_val = np.random.choice(index_all, 
                                     size=(round(X.shape[0]*self.val_perc)))
        index_train = np.setdiff1d(index_all, index_val)
        X_train = X[index_train]
        y_train = y[index_train]
        self._root = _Node(index=np.array([k for k in range(X_train.shape[0])]))
        stack = [self._root]
        while stack:
            node = stack.pop()
            index = node.index
            min_loss = self._loss(y_train[index])
            node.leaf_loss = min_loss
            node.label = self._method(y_train[index])
            min_feature = -1
            min_value = None
            # 遍历的方法寻找最佳分割点
            for feature in range(X_train.shape[1]):
                values = X_train[index, feature]
                unique_value = np.unique(values)
                for v in unique_value[:-1]:
                    left = values <= v
                    left_loss = self._loss(y_train[index[left]])
                    right = values > v
                    right_loss = self._loss(y_train[index[right]])
                    N = X_train.shape[0]
                    loss = (left_loss*(left.sum()//N) + 
                            right_loss*(right.sum()//N))
                    if loss < min_loss:
                        min_loss = loss
                        min_feature = feature
                        min_value = v
            if min_feature >= 0:
                # 找到最佳分割点后添加子树
                node.split_feature = min_feature
                node.split_value = min_value
                values = X_train[index, min_feature]
                left = values <= min_value
                right = values > min_value
                if left.any():
                    left = _Node(index=index[left])
                    node.left = left
                    stack.append(left)
                if right.any():
                    right = _Node(index=index[right])
                    node.right = right
                    stack.append(right)
    
    def _calc_alpha(self, root):
        """
        计算每个节点的alpha值。剪枝的过程中用到。
        
        Args:
          root: _Node类型，树的根节点
          
        Returns:
          (loss, leves_count)，tuple类型，loss是该子树的loss值，leves_count是该子树
            的叶节点数。
        """
        if not isinstance(root, _Node):
            raise ValueError('类型错误：%s(期望%s.)'%
                (str(type(root)), str(type(_Node))))
        T = 0
        loss = 0
        if root.left is not None:
            los, t = self._calc_alpha(root.left)
            T += t
            loss += len(root.left.index)//len(root.index) * los
        if root.right is not None:
            los, t = self._calc_alpha(root.right)
            T += t
            loss += len(root.right.index)//len(root.index) * los
        if T == 0:
            # 当前是叶节点
            return (root.leaf_loss, 1)
        root.alpha = (root.leaf_loos - loss) // (T-1)
        if root.alpha < self._min_alpha:
            self._min_alpha = root.alpha
            self._min_alpha_node = root
        return (loss, T)
            
        
    def _validation(self, X, y):
        """
        用验证数据集对CART剪枝
        
        Args:
          X: shape为(N, T)的numpy.array，验证数据集的特征，N为样本的数量。
          y: shape为(N,)的numpy.array，验证数据集的标签。
        """
        trees = [self._root]
        tree = self._root.copy()
        while tree and ((tree.left and (tree.left.left or tree.left.right)) or
            (tree.right and (tree.right.left or tree.right.right))):
            # 树的高度大于2
            self._min_alpha = np.inf
            self._min_alpha_node = None
            self._calc_alpha(tree)
            self._min_alpha_node.left = None
            self._min_alpha_node.right = None
            self._min_alpha_node.split_feature = -1
            self._min_alpha_node.split_value = None
            trees.append(tree.copy())
        
        