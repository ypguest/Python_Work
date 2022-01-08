# !/usr/bin/python
# -*- coding: utf-8 -*-
# @FileName:B-model.py
# @Time:2021/10/2 15:25
# @Author:Jason_Yin

from scipy.stats import binom
import seaborn as sns

def fun_b():
    data_binom = binom.rvs(n=10, p=0.5, size=10000)
    ax = sns.displot(data_binom,
                      kde=False,
                      color='green',
                      hist_kws={"linewidth": 15, 'alpha': 1})
    ax.set(xlabel='Binomial Distribution', ylabel='Frequency')

if __name__ == '__main__':
    fun_b()