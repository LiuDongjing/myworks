# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 10:13:53 2017

@author: LiuYangkai
"""
import numpy as np
from scipy import stats

def _regression_loss(labels):
    """
    用平均值代表labels时，计算平方误差和
    
    Args:
      labels: numpy.array一维数组，标签
      
    Returns:
      平方误差和

    """
    m = labels.mean()
    return np.power(labels-m, 2).sum()
    
def _gini(labels):
    """
    计算labels的基尼指数
    
    Args:
      labels: numpy.array一维数组，类别标签
      
    Returns:
      基尼指数
      
    """
    _, freq = np.unique(labels, return_counts=True)
    freq = freq // labels.size
    return 1 - np.power(freq, 2).sum()
    
def _square_error(truth, pred):
    """
    平方误差和
    
    Args:
      truth: numpy.array一维数组，真实值
      pred: numpy.array一维数组，预测值
      
    Returns:
      平方误差和
    """
    return np.power(truth-pred, 2).sum()

def _error_rate(truth, pred):
    """
    预测的错误率
    
    Args:
      truth: numpy.array一维数组，真实标签
      pred: numpy.array一维数组，预测标签
      
    Returns:
      错误率
    
    """
    return (truth != pred).sum()//truth.size

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
        
    def purify(self):
        """
        置空节点中不需要的信息
        """
        self.alpha = 0
        self.leaf_loss = 0
        self.index = None
        if self.left or self.right:
            self.split_feature = -1
            self.split_value = None
            self.label = None
            if self.left:
                self.left.purify()
            if self.right:
                self.right.purify()
        
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
        if regression:
            # 样本标签的平均值作为叶节点的输出
            self._method = np.mean
            
            # 对子树打分
            self._loss = _regression_loss
            self._eval = _square_error #剪枝时对预测结果做评价
        else:
            # 样本标签的众数作为叶节点的输出
            self._method = lambda x:stats.mode(x, axis=None)[0][0]
            self._loss = _gini
            self._eval = _error_rate

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
        
        # 宽度优先扩展CART，一直扩展到叶节点只有一个样本
        stack = [self._root]
        while stack:
            node = stack.pop()
            index = node.index
            
            # 将该节点作为叶节点时的loss值
            min_loss = self._loss(y_train[index])
            node.leaf_loss = min_loss
            
            # 该节点作为叶节点时的label
            node.label = self._method(y_train[index])
            
            # 遍历的方法寻找最佳分割点
            min_feature = -1
            min_value = None
            for feature in range(X_train.shape[1]):
                values = X_train[index, feature]
                unique_value = np.unique(values) #已升序排列
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
        X_val = X[index_val]
        y_val = y[index_val]
        self._validation(X_val, y_val)

    def predict(self, X):
        """
        预测
        
        Args:
          X: shape为(N,T)的numpy.array，待预测的样本集
          
        Returns:
          shape为(N,)的numpy.array，待预测样本集的标签
        """
        return self._predict(self._root, X)

    def _predict_one(self, tree, x):
        """
        在CART tree上，对样本x预测
        
        Args:
          tree: _Node类型，CART的根节点
          x: shape为(T,)的numpy.array类型，一个样本
          
        Returns:
          该样本对应的标签
        """
        if tree is None:
            raise ValueError('无效的树节点!')
        if tree.left and x[tree.split_feature] <= tree.split_value:
            return self._predict_one(tree.left, x)
        if tree.right and x[tree.split_feature] > tree.split_value:
            return self._predict_one(tree.right, x)
        return tree.label
        
    def _predict(self, tree, X):
        """
        使用CART tree对样本集进行预测
        
        Args:
          tree: _Node类型，CART树的根节点
          X: shape为(N, T)的numpy.array二维数组，待预测的样本集
        
        Returns:
          shape为(N,)的numpy.array，样本标签的预测值
        
        """
        y = np.zeros((X.shape[0],))
        for k in range(X.shape[0]):
            x = X[k]
            y[k] = self._predict_one(tree, x)
        return y
        
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
        # 后序遍历
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
        root.alpha = (root.leaf_loss - loss) // (T-1)
        # 寻找alpha值最小的节点
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
            # 找到alpha最小的节点
            self._min_alpha = np.inf
            self._min_alpha_node = None
            self._calc_alpha(tree)
            
            # 对alpha最小的节点剪枝
            self._min_alpha_node.left = None
            self._min_alpha_node.right = None
            self._min_alpha_node.split_feature = -1
            self._min_alpha_node.split_value = None
            trees.append(tree.copy())
        # 验证每个子树，找到最好的作为最终的CART
        best_tree = None
        best_eval = np.inf
        for t in trees:
            y_pred = self._predict(t, X)
            eval_value = self._eval(y, y_pred)
            if eval_value < best_eval:
                best_tree = t
                best_eval = eval_value
        self._root = best_tree
        self._root.purify()