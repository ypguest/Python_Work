import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico', 'themes/']

# TARGET
target = Executable(
    script="main.py",     # 目标引用脚本
    base="Win32GUI",      # GUI程序需要隐藏控制台
    icon="icon.ico"       # 生成exe的的图标
)

# SETUP CX FREEZE
setup(
    name="PyDracula",
    version="1.0",
    description="Modern GUI for Python applications",
    author="jason.yin",
    options={'build_exe': {'include_files': files}},
    executables=[target]
)

# 在命令行输入python setup.py build进行打包, 打包后的文件放在build目录下
