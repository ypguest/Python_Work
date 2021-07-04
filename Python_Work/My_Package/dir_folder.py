#!/usr/bin/python
# -*- coding: utf-8 -*-
"""遍历文件夹内的所有文件，并输出列表"""

import os


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


if __name__ == "__main__":
    dir_path = r'C:\Users\yinpeng\Desktop\Module_Test_Result\rawdata'
    dir_paths = dir_folder(dir_path)
    print(dir_paths)
