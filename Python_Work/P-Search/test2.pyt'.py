# !/usr/bin/python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

# 构建噪声数据xu,yu
xu = np.random.rand(50) * 4 * np.pi - 2 * np.pi
def f(x):
    return np.sin(x) + 0.5 * x

yu = f(xu)

plt.figure(figsize=(8, 4))
# 用噪声数据xu,yu，得到拟合多项式系数，自由度为5
reg = np.polyfit(xu, yu, 10)

ry = np.polyval(reg, xu)

plt.plot(xu, yu, 'b^', label='f(x)')
plt.plot(xu, ry, 'r.', label='regression')
plt.legend(loc=0)
plt.show()