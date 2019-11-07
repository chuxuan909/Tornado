#!/usr/bin/env python
# -*- coding:utf-8 -*-
import platform
import os
import sys

#环境变量
#for linux
if platform.system() == "Windows":
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1]) #当前目录的上一级目录
    # BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    #print (BASE_DIR)
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
    # BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from core import DataGo

if __name__ == "__main__":
    DataGo.Collets(sys.argv)