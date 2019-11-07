#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 外部调用此模块来获得查询数据
from core import DataGo

test_obj=DataGo.Collets([None,'regpeople','2019-08-07'])
print(test_obj.data_return())