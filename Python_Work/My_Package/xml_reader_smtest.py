#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import collections
import copy
import datetime

# test_item_dict = collections.OrderedDict()
# file_path = r"C:\Users\yinpeng\Desktop\Module_Test_Result\rawdata\30-5A-3A-0E-81-8B\UMT002I\19102801.XML"
# test_item_dict = collections.OrderedDict([('RA2', []), ('BUTTERFLY', []), ('MOVINV8', []), ('VICTIM', [])])
# 测试item ([('T7', 'MOVINV8ACC'), ('T0', 'BUTTERFLYACC'), ('T1', 'SSN'), ('T4', 'VICTIM')])


def xml_reader_smtest(file_path, test_item_dict):
    fail_logs = []
    test_results = {}  # 最终测试结果文件
    with open(file_path, "rt") as f:
        tree = ET.parse(f)  # 载入数据
        root = tree.getroot()  # 获取根节点
        if root.tag.upper() == "SMTEST":    # 判断文件是否为SMTEST
            for smtest in root.findall("TESTRUN"):
                test_time = smtest.get('START')  # 访问START元素属性,获得测试时间
                test_time_format = datetime.datetime.strptime(test_time, '%a %b %d %H:%M:%S %Y')
                test_time = test_time_format.strftime('%Y/%m/%d %H:%M:%S')
                test_ver = smtest.find("VERSION").text  # 获取test_version
                flow = smtest.find("FLOW").text
                for mch in smtest.findall("MCH"):
                    for controller in mch.findall("./SOCKET/CONTROLLER"):
                        for channel in controller.findall("CHANNEL"):
                            for dim in channel.findall("DIMM"):
                                pn = dim.find("ID").text
                                sn = dim.find("SN").text
                                silk = dim.find("SILK").text
                                test_results[sn] = [sn, test_time, test_ver, flow, pn, silk, copy.deepcopy(test_item_dict)]
    # {'0827DE05': ['0827DE05', 'Sun Oct 27 22:31:57 2019', '0.0.2RD', 'D4R1','SCQ32GP12H1F1C-26V A', '1A1_DIMM',
    # OrderedDict([("MOVINV8ACC", ""), ("BUTTERFLYACC", ""), ("SSN", ""), ("VICTIM", "")])
        elif root.tag.upper() == "UMTEST":
            for umtest in root.findall("TESTRUN"):
                test_time = umtest.get('START')  # 访问START元素属性,获得测试时间

                test_ver = umtest.find("VERSION").text  # 获取test_version
                flow = umtest.find("FLOW").text
                for mch in umtest.findall("MCH"):
                    for controller in mch.findall("CONTROLLER"):
                        for channel in controller.findall("CHANNEL"):
                            for dim in channel.findall("DIMM"):
                                try:
                                    pn = dim.find("ID").text
                                except AttributeError:
                                    pn = "99999999"
                                try:
                                    sn = dim.find("SN").text
                                except AttributeError:
                                    sn = "99999999"
                                silk = dim.find("SILK").text
                                test_results[sn] = [sn, test_time, test_ver, flow, pn, silk, copy.deepcopy(test_item_dict)]
        for entry in root.findall(".//ENTRY"):  # fail sample information collect
            for algorithm in entry.findall("ALGORITHM"):
                fail_patter = algorithm.find("ALGO_NAME").text.upper()
            try:
                dimm_sn = entry.find("DIMM_SN").text
            except AttributeError:
                dimm_sn = "99999999"
            rank = entry.find("RANK").text
            bs = entry.find("BS").text
            bg = entry.find("BG").text
            ras = entry.find("RAS").text
            cas = entry.find("CAS").text
            try:
                dq = entry.find("ECC_DQ").text
            except AttributeError:
                dq = entry.find("DQ").text
            fail_log = [dimm_sn, fail_patter, rank, bg, bs, ras, cas, dq]
    # 将测试的最终结果转换为list
    # ['08E2EC05', 'BUTTERFLYACC', '0', '0', '0', 'FC08', '0330', '24']
            if fail_log not in fail_logs:
                fail_logs.append(fail_log)
    # 除去重复的fail log
        for keys, values in test_results.items():
            for value in values:
                if type(value) is collections.OrderedDict:
                    # 从test_results中筛出测试项目([('MOVINV8ACC', ''), ('BUTTERFLYACC', ''), ...)]
                    for key in value.keys():
                        # key为测试项目名称
                        for fail_log in fail_logs:
                            if keys == fail_log[0] and key == fail_log[1] and fail_log[2:] not in test_results[keys][len(values) - 1][key]:
                                test_results[keys][len(values) - 1][key].append(fail_log[2:])
    return test_results
