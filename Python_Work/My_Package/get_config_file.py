#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import copy
import collections


def get_test_item(file_path, test_flow):
    test_items = collections.OrderedDict()  # OrderedDict([('T0', 'MOVINV8'), ('T1', 'MOVINV8F'), ('T2', 'MOVINV8R')])
    test_flows = collections.OrderedDict()  # OrderedDict([('GLOBAL', OrderedDict([('CYCLE', '5')])), ......
    test_item_dict_out = collections.OrderedDict()
    test_item_out = []
    with open(file_path, "r") as f_obj:
        lines = [tmp.strip() for tmp in f_obj.readlines()]
        for line in lines:
            if line.startswith("[") or line.startswith("{"):
                test_items = collections.OrderedDict()  # 初始化test_items [('CYCLE', '5')]
                test_flows["".join(line[1:-1])] = []  #
                test_item = "".join(line[1:-1])
            elif line != "":
                line = re.split("=|;", line)
                if line[1] == 'ACCMOVINV8' or line[1] == 'ACCBUTTERFLY':
                    line[1] = line[1][3:]+line[1][:3]
                test_items[line[0]] = (line[1])
                test_flows[test_item] = copy.deepcopy(test_items)
    for value in test_flows[test_flow].values():
        test_item_dict_out[value] = []
        test_item_out.append(value)
    return test_item_dict_out, test_item_out

# 需要输入config文件的路径，以及所需要的test_flow, 返回该flow的测试项目
# 输出如下内容
# OrderedDict([('MOVINV8ACC', []), ('BUTTERFLYACC', []), ('SSN', []), ('VICTIM', [])])
# ['MOVINV8ACC', 'BUTTERFLYACC', 'SSN', 'VICTIM']



