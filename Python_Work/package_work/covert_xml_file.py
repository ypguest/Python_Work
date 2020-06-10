#!/usr/bin/python
# -*- coding: utf-8 -*-
"""解决UMTEST及SMTEST缺少后缀，导致文件无法打开的问题"""
import os
import re
from dir_folder import dir_folder


def cover_xml_file(file_path):
    xml_Regex = re.compile(r'\d{8}\.XML', re.I)
    file_paths = dir_folder(file_path)
    for file_path in file_paths:
        (filepath, tempfilename) = os.path.split(file_path)
        if re.match(xml_Regex, tempfilename):
            with open(file_path, "r+") as f_obj:
                lines = f_obj.readlines()
                if lines[2].strip() == "<SMTEST>":
                    if lines[-1].strip() == "</MCH>":
                        f_obj.write("\n")
                        f_obj.write("  </TESTRUN>\n")
                        f_obj.write("</SMTEST>")
                    if lines[-1].strip() == "</ENTRY>":
                        f_obj.write("\n")
                        f_obj.write("  </TESTRUN>\n")
                        f_obj.write("</SMTEST>")
                    if lines[-1].strip() == "</TESTRUN>":
                        f_obj.write("\n")
                        f_obj.write("</SMTEST>>")
                    f_obj.close()
                if lines[2].strip() == "<UMTEST>":
                    if lines[-1].strip() == "</MCH>":
                        f_obj.write("\n")
                        f_obj.write("  </TESTRUN>\n")
                        f_obj.write("</UMTEST>")
                    if lines[-1].strip() == "</ENTRY>":
                        f_obj.write("\n")
                        f_obj.write("  </TESTRUN>\n")
                        f_obj.write("</UMTEST>")
                    if lines[-1].strip() == "</TESTRUN>":
                        f_obj.write("\n")
                        f_obj.write("</UMTEST>>")
                    f_obj.close()


if __name__ == '__main__':
    file_paths1 = r"C:\Users\yinpeng\Desktop\Module_Test_Result\rawdata"
    cover_xml_file(file_paths1)
