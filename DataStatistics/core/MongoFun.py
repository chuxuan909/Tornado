#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymongo
import time,datetime
from config.conf_database import get_mongo_arg
import sys

class Mongo_DBs(object):
    def __init__(self,data_time,GAME_COUNT_NUM):
        self.data_time=data_time
        self.GAME_COUNT_NUM = GAME_COUNT_NUM  # 游戏记录次数
        self.__connect_mongo()

    def __connect_mongo(self):
        self.mongo_client = pymongo.MongoClient("mongodb://%s:%s/" % (get_mongo_arg('url'),get_mongo_arg('port')))
        self.m_db = self.mongo_client[get_mongo_arg('db')]
        self.m_col = self.m_db[get_mongo_arg('collection')['col1']]
        self.m_col2 = self.m_db[get_mongo_arg('collection')['col2']]
        self.m_col3 = self.m_db[get_mongo_arg('collection')['col3']]

    def game_record(self):
        '''
        游戏记录查询
        :return:
        '''
        record_list=[]

        # 获取13位时间戳
        time_later_stamp = self.timestamp(self.date_oper(self.data_time))
        time_now_stamp = self.timestamp(self.data_time)

        myquery = {'time': {'$gte': time_now_stamp, '$lt': time_later_stamp}} # 查询条件
        res = self.m_col.find(myquery)

        for re_index in res:
            rec_dic=re_index
            if record_list.count(rec_dic.get('uid')) <= self.GAME_COUNT_NUM:
                record_list.append(rec_dic.get('uid'))
        return record_list

    def revenue(self):
        '''
        玩家营收记录查询
        :return:
        '''
        if self.data_time >= time.strftime("%Y-%m-%d", time.localtime()):
            before_data = self.date_oper_before()
            return self.m_col2.find({'date':before_data},{'_id' : 0})
        else:
            # print('查询指定日期-> %s' % self.data_time)
            return self.m_col2.find({'date': self.data_time}, {'_id': 0})

    def win_record(self):
        '''赢排名前100'''
        # if self.data_time >= time.strftime("%Y-%m-%d", time.localtime()):
        #     before_data = self.date_oper_before()
        #     return self.m_col2.find({'date': before_data}, {'_id': 0})
        # else:
        #     # print('查询指定日期-> %s' % self.data_time)
        li=[]
        for i in self.m_col3.find({'date': self.data_time}, {'_id': 0}):
            li.append(i)
        if li:
            return li[0]['leftRank']
        else:
            return li

    def lose_record(self):
        '''输排名前100'''
        # if self.data_time >= time.strftime("%Y-%m-%d", time.localtime()):
        #     before_data = self.date_oper_before()
        #     return self.m_col2.find({'date': before_data}, {'_id': 0})
        # else:
        #     # print('查询指定日期-> %s' % self.data_time)
        li = []
        for i in self.m_col3.find({'date': self.data_time}, {'_id': 0}):
            li.append(i)
        if li:
            return li[0]['rightRank']
        else:
            return li

    def timestamp(self,my_time):
        '''时间转为13位数的时间戳'''
        ts = time.strptime('%s 00:00:00.000000' % my_time, "%Y-%m-%d %H:%M:%S.%f")
        return time.mktime(ts)*1000

    def date_oper(self,srt_time):
        '''
        日期处理
        :param srt_time:
        :return: 返回当前日期后一天的日期
        '''
        try:
            now=datetime.datetime.strptime(srt_time,'%Y-%m-%d')
            now_later=now+datetime.timedelta(days=1)
            return  now_later.strftime('%Y-%m-%d')
        except ValueError:
            print("请输入正确的日期格式")
            sys.exit(600)

    def date_oper_before(self,):
        '''
        日期处理
        :param srt_time:
        :return: 返回当前日期前一天的日期
        '''
        srt_time=time.strftime("%Y-%m-%d", time.localtime())
        try:
            now=datetime.datetime.strptime(srt_time,'%Y-%m-%d')
            now_later=now-datetime.timedelta(days=1)
            return  now_later.strftime('%Y-%m-%d')
        except ValueError:
            print("请输入正确的日期格式")
            sys.exit(601)


if __name__ == '__main__':
    test_db=Mongo_DBs('2019-11-01',50)
    clo_list=test_db.win_record()
    re_li=test_db.revenue()

    print(clo_list)
    print(re_li)


