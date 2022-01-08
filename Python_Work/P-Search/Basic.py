# !/usr/bin/python
# -*- coding: utf-8 -*-

# 导入需要用到的库
import nurnpy as np
# 定义朴素贝叶斯模型的基类， 方便以后的拓展
class NaiveBayes:
    """
    初始化结构
    self._x, self._y：记录训练集的变量
    self._data ： 核心数组，存储实际使用的条件概率的相关信息
    self._func ： 模型核心一一决策函数，能够根据输入的x 、y输出对应的后验概率
    self._n_possibilities ：记录各个维度特征取值个数的数组： ［Sv
    S2, ..., S0]
    11 · self.labelled
    k
    记录按类别分开后的输入数据的数组
    12
    self._label_zip ：记录类别相关信息的数组， 视具体算法，定义会有所不同
    13
    self._cat_counter ： 核心数组，记录第工类数据的个数（ cat
    是category
    的缩写）
    14
    self.con
    counter ： 核心数组， 用于记录数据条件概率的原始极大似然估计
    15
    self._con_counter[d][c][p] = p(X仰＝ p
    ly = c) (con 是conditional 的缩写）
    16
    self.label
    dic ： 核心字典， 用于记录数值化类别时的转换关系
    17
    sel
    f.feat
    dics ：核心字典， 用于记录数值化各维度特征（ feat ） 时的转换关系