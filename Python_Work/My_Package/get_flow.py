#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET


def get_flow(file_path):
    with open(file_path, "r") as f:
        tree = ET.parse(f)  # 载入数据
        root = tree.getroot()  # 获取根节点
        for smtest in root.findall("TESTRUN"):
            flow = smtest.find("FLOW").text
    return flow
