#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
import sys
from config.conf_database import get_redis_arg

class Redis_DBs(object):
    def __init__(self,data_time,function):
        self.put_zkey='userPut_%s' % data_time
        # self.output_zkey = 'userOutput_%s' % data_time
        self.function=function
        self.__connect()
        self.li=[]

    def dofun(self):
        if hasattr(self,self.function):
            func=getattr(self,self.function)
            func()
            return self.li
        else:
            print('DBfunction 模块无此方法')
            sys.exit(101)

    def __connect(self):
        '''
        连接redis
        :return:
        '''
        self.pool=redis.ConnectionPool(host=get_redis_arg('url'),port=get_redis_arg('port'),db=get_redis_arg('db'))
        self.connect=redis.Redis(connection_pool=self.pool)

    def redis_input(self):
        '''
        查询redis
        :return:
        '''
        self.li=self.connect.zrange(self.put_zkey,0,99,withscores=True)

    def redis_output(self):
        '''
        查询redis
        :return:
        '''
        self.li = self.connect.zrevrange(self.put_zkey,0,99,withscores=True)

if __name__ == '__main__':
    tb_test=Redis_DBs('2019-11-01','redis_input')
    test_li=tb_test.dofun()
    print(test_li)