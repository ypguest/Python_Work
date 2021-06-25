# !/usr/bin/python
# -*- coding: utf-8 -*-
# @FileName:read4gd3.py
# @Time:2021/1/7 8:47
# @Author:Jason_Yin

import os
import xml.etree.ElementTree as ET
import pandas as pd
import xlwt

# ---- pd设置 ----
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


def dir_folder(file_path):
    file_paths = []
    for root, dirs, files in os.walk(file_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        for file in files:
            if file == "desktop.ini":
                continue
            else:
                file_paths.append(os.path.join(root, file))

    return file_paths


def xml_reader(file_path):
    with open(file_path) as f:
        file_name = os.path.basename(file_path).split('.')[0][:9]
        tree = ET.parse(f)
        root = tree.getroot()
        WaferId = root.attrib["WaferId"]
        Bindata_dict = {'WaferId': WaferId}

        for children in root:
            Columns = children.attrib['Columns']
            DeviceSizeX = children.attrib['DeviceSizeX']
            DeviceSizeY = children.attrib['DeviceSizeY']
            LotId = children.attrib['LotId']
            MapType = children.attrib['MapType']
            NullBin = children.attrib['NullBin']
            Orientation = children.attrib['Orientation']
            OriginLocation = children.attrib['OriginLocation']
            ProductId = children.attrib['ProductId']
            Rows = children.attrib['Rows']
            SupplierName = children.attrib['SupplierName']
            WaferSize = children.attrib['WaferSize']
            for Bin in children.iter("{http://www.semi.org}Bin"):
                BinCode = Bin.attrib['BinCode']
                BinCount = Bin.attrib['BinCount']
                BinDescription = Bin.attrib['BinDescription']
                BinQuality = Bin.attrib['BinQuality']
                Bindata_dict.update({BinCode: BinCount})
            for Data in children.iter("{http://www.semi.org}Data"):
                DataCode = Data.attrib['CreateDate']
                Bindata_dict.update({'Data': DataCode})
            print(Bindata_dict)
    return Bindata_dict


if __name__ == '__main__':
    rawpaths = r"""\\arctis\qcxpub\QRE\00_Production_Public\4GDDR4_25nm\17_Quality_control\6.Wafer Plan Vs Mapping\500pcs Raw Data"""
    paths = dir_folder(rawpaths)
    df = pd.DataFrame()
    for path in paths:
        data = xml_reader(path)
        df = df.append(data, ignore_index=True)
    # df = df.set_index("WaferId")
    # df = df.fillna(0)
    # df.to_excel('data.xls')





