# !/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os

# 利用Numpy 的函数定义训练并返回多项式回归模型的函数;
# np.polyfit(x,y,deg) 通过多项式拟合, 对x,y进行拟合, 其中deg表示自由度, 返回多项式的系数reg;
# np.polyval(reg, x) 输入x的值, 以及多项式的系数, 返回对应的y值;

def get_model(deg):
    return lambda input_x = xO: np.polyval(np.polyfit(x, y, deg), input_x)

# 根据参数n 、输入的x 、y 返回相对应的损失
def get_cost(deg, input_x, input_y):
    return 0.5*((get_model(deg)(input_x) - input_y) ** 2).sum()


# ---- 1. 识别数据
x, y = [], []
for sample in open(r"../../TestData/prices.txt ", "r"):

    _x, _y = sample.split(",")
    x.append(float(_x))
    y.append(float(_y))

x, y = np.array(x), np.array(y)
x = (x - x.mean()) / x.std()

# ---- 2. 识别数据

xO = np.linspace(-2, 4, 100)

test_set = (1, 2, 3)   # 自由度


for d in test_set:
    print(get_cost(d, x, y))
plt .scatter(x, y, c="g", s=20)
for d in test_set:
    plt.plot(xO, get_model(d)(), label="degree = {}".format(d))

plt.xlim(-2, 4)
plt.ylim(1e5, 8e5)
plt.legend()
plt.show()
