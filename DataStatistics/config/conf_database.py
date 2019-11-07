#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import create_engine

#mysql连接配置
database_config={
    "passwd":"xxxxxxxxx",  # 数据库密码
    "user":"xxx",                     # 数据库用户
    "url":"xxx.xxx.xxx.xxx",                 # 数据库地址
    "port":3306,                       # 数据库连接端口
    "dbs":{'userdb1':'gHallSvrShardInfo_0','userdb2':'gHallSvrSingleInfo_0',}                  # mysql连接的库名称
}

#mongo连接配置
database_mongo_config ={
    "passwd": "",  # 数据库密码
    "user": "",  # 数据库用户
    "url": "xxx.xxxxxx",  # 数据库地址,测试
    "port": "27017",  # 数据库连接端口
    "db":"GHall",
    "collection":{"col1":"gameCoinDetail","col2":"userPut","col3":"userPutRank"}
}

#redis连接配置
database_redis_config ={
    "passwd": "",  # redis密码
    "user": "",  # redis用户
    "url": "xxx.xxx.xxx.xxx",  # redis地址
    "port": "6379",  # redis连接端口
    "db":2,     # redis使用的库
}

def get_arg(info):
    '''
    获取配置参数
    :param info: key
    :return: 配置参数
    '''
    try:
        return database_config[info]
    except KeyError:
        return None

def get_mongo_arg(info):
    '''
    获取配置参数
    :param info: key
    :return: 配置参数
    '''
    try:
        return database_mongo_config[info]
    except KeyError:
        return None

def get_redis_arg(info):
    '''
    获取配置参数
    :param info: key
    :return: 配置参数
    '''
    try:
        return database_redis_config[info]
    except KeyError:
        return None

def test_db():
    '''
    尝试连接数据库
    :return:
    '''
    for value in get_arg('dbs').values():
        engine = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' % (
        get_arg('user'), get_arg('passwd'), get_arg('url'), get_arg('port'), value), max_overflow=15,
                                 echo=False)
        try:
            dbs_name=engine.execute('show databases')
            if dbs_name:
                print("连接 >>%s:%d<< MySql数据库 [[%s]] 成功" % (get_arg('url'),get_arg('port'),value))
                dbs_name.close()
        except Exception as err:
            print("数据库连接失败... 请检查连接配置和数据库服务器配置")
            print(err)


if __name__ == "__main__":
    print('数据库地址 : %s ' % get_arg('url'))
    print('数据库连接端口 %d' % get_arg('port'))
    for index in get_arg('dbs').keys():
        print('连接的数据库 %s 名称为 : %s' % (index, get_arg('dbs')[index]))
    raw=input("是否测试数据库连接？ [Y/N]\t")
    if raw == "Y" or raw == "y":
        test_db()
    else:
        pass
