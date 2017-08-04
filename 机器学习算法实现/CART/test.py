# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 10:22:05 2017

@author: LiuDongjing
"""
import numpy as np
from sklearn.datasets import fetch_mldata
from sklearn.model_selection import train_test_split
from CART import CART
print('在iris数据集上做分类...')
iris = fetch_mldata('iris', data_home='../datasets/iris')
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target)
model = CART(debug=True)
model.fit(X_train, y_train)
pred = model.predict(X_test)
eq = pred == y_test
print('Accuracy: %.2f.'%(np.sum(eq)/eq.shape[0]))

print('在boston数据集上做回归...')
boston = fetch_mldata('housing_scale', data_home='../datasets/boston')
X_train, X_test, y_train, y_test = train_test_split(
    boston.data, boston.target)
model = CART(regression=True, debug=True)
model.fit(X_train, y_train)
pred = model.predict(X_test)
err = np.mean(np.power(y_test-pred, 2))
print('Mean error: %.2f.'%np.sqrt(err))
