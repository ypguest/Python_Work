#!/usr/bin/python
# -*- coding: utf-8 -*-
"""获得XML数据文件"""
from mygui.package_work.dir_folder import *
from mygui.package_work.get_flow import *
from mygui.package_work.xml_reader_smtest import *
from mygui.package_work.xml_writer_total import *
import shutil
import os
import re


def get_test_item(file_path_get, test_flow):
    test_items = collections.OrderedDict()  # OrderedDict([('T0', 'MOVINV8'), ('T1', 'MOVINV8F'), ('T2', 'MOVINV8R')])
    test_flows = collections.OrderedDict()  # OrderedDict([('GLOBAL', OrderedDict([('CYCLE', '5')])), ......
    test_item_dict_out = collections.OrderedDict()
    test_item_out = []
    with open(file_path_get, "r") as f_obj:
        lines = [tmp.strip() for tmp in f_obj.readlines()]
        for line in lines:
            if line.startswith("[") or line.startswith("{"):
                test_items = collections.OrderedDict()  # 初始化test_items [('CYCLE', '5')]
                test_flows["".join(line[1:-1])] = []  #
                test_item = "".join(line[1:-1])
            elif line != "":
                line = re.split("=|;", line)
                if line[1] == 'ACCMOVINV8' or line[1] == 'ACCBUTTERFLY':
                    line[1] = line[1][3:] + line[1][:3]
                test_items[line[0]] = (line[1])
                test_flows[test_item] = copy.deepcopy(test_items)
    for value in test_flows[test_flow].values():
        test_item_dict_out[value] = []
        test_item_out.append(value)
    return test_item_dict_out, test_item_out


def xml_dir_smtest(file_path_xml):
    test_results_xml = {}
    xml_Regex = re.compile(r'\d{8}\.XML', re.I)
    file_paths = dir_folder(file_path_xml)
    for file in file_paths:
        (filepath, tempfilename) = os.path.split(file)
        (filename, extension) = os.path.splitext(tempfilename)
        if re.match(xml_Regex, tempfilename):  # 获取包含测试结果的xml文件
            test_flow = get_flow(file)  # 获取test flow
            # 将test_flow为"STANDARD"的文件移走
            if test_flow == "STANDARD":
                shutil.move(file, r"C:\Users\yinpeng\Desktop\Module_Test_Result\STANDARD")
            fileregex = os.path.join(filepath, "umtest.INI")
            # 读取每个测试log的测试项目名称
            if os.path.exists(fileregex):  # 返回所有匹配的文件路径列表
                test_item_dict_out, test_item_out = get_test_item(''.join(fileregex), test_flow)
                test_results_xml = xml_reader_smtest(file, test_item_dict_out)
                test_item_out = ['SN', 'TEST_TIME', 'PRO_V', 'TEST_FLOW', 'PN', 'SILK', 'FLAG'] + test_item_out
                writer_each_file(filepath, filename, test_item_out, test_results_xml)
                writer_sum_file(test_results_xml, test_item_out, test_flow)
    return test_results_xml


if __name__ == "__main__":
    file_path = r"C:\Users\yinpeng\Desktop\Module_Test_Result\rawdata"
    test_results = xml_dir_smtest(file_path)
