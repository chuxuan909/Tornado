#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Python2.x除法保留2位小数
# from __future__ import division
# from __future__ import print_function
# from __future__ import unicode_literals

from sqlalchemy import Column,create_engine,Integer,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_
from sqlalchemy import inspect
import argparse,sys
import datetime
import time
import re

#Python2.x的中文支持
# reload(sys)
# sys.setdefaultencoding('utf-8')

from config.conf_database import get_arg # 数据库连接配置
from config.conf_database import test_db # 数据库连接测试
from core import DataManager
from core.DBfunction import DBs
from core.MongoFun import Mongo_DBs
from core.RedisFunction import Redis_DBs

#用户全局变量
#stables_count=511
# engine01 = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' % (get_arg('user'),get_arg('passwd'),get_arg('url'),get_arg('port'),get_arg('dbs')['userdb1']), max_overflow=15, echo=False)
# engine02 = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' % (get_arg('user'),get_arg('passwd'),get_arg('url'),get_arg('port'),get_arg('dbs')['userdb2']), max_overflow=15, echo=False)
# Satisfy_reg_uidset=[]
# Satisfy_login_set=[]

# base=declarative_base()
##获取数据库内所有表的信息#######
# base.metadata.reflect(engine01)
# tables = base.metadata.tables
# print(tables)
##获取数据库内所有表的信息 END####

# def usage():
#     '''
#     输出帮助信息
#     '''
#     print(
# """
# Usage:  sys.args[0]       [option]
#
# [option]：
#
# -h or --help：显示帮助信息
# -l or --login：指定查询那个日期的登录记录      例如: 2019-06-06
# -r or --reg：指定查询那个日期的注册记录      例如: 2019-06-06
# """
#     )
#
# def argv_check():
#     '''
#     判断是否输入了参数
#     '''
#     if len(sys.argv) == 1:
#         usage()
#         sys.exit()
#
# def parser_flag():
#     '''
#     获取用户输入参数的函数
#     :return:
#     '''
#     #帮助信息
#     parser=argparse.ArgumentParser(description="输入登录记录和注册记录的查询日期")
#     #相关选项
#     parser.add_argument("-l","--login",help="指定查询那个日期的登录记录      例如: 2019-06-06")
#     parser.add_argument("-r","--reg",help="指定查询那个日期的注册记录      例如: 2019-06-06")
#     #获取参数
#     # args=parser.parse_args()
#     return parser.parse_args()

class Collets(object):
    def __init__(self,argv_list):

        self.engine01 = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' % (get_arg('user'),get_arg('passwd'),get_arg('url'),get_arg('port'),get_arg('dbs')['userdb1']), max_overflow=15, echo=False)
        self.engine02 = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' % (get_arg('user'),get_arg('passwd'),get_arg('url'),get_arg('port'),get_arg('dbs')['userdb2']), max_overflow=15, echo=False)
        self.argvs=argv_list
        self.data_time=time.strftime("%Y-%m-%d", time.localtime())
        self.GAME_COUNT_NUM = 50 # 游戏记录次数
        self.mongo_list=[]
        self.mongo_dict={}
        self.mysql_list=[]
        self.redis_list=[]
        self.pattern = re.compile(r'^userInfo_[0-9]{3}')
        self.__data_check()
        self.__parse_argv()

    def __data_check(self):
        '''
        检测是否自定义了日期
        :return:
        '''
        if len(self.argvs) >= 3:
            self.validate(self.argvs[2])
            self.data_time=self.argvs[2]


    def __parse_argv(self):
        '''
        模块不同功能
        :return:
        '''
        if len(self.argvs) >1:
            if hasattr(self,self.argvs[1]):
                func = getattr(self,self.argvs[1])
                func()
            else:
                print('找不到对应的模块功能')
                self.help_msg()
        else:
            print('请输入功能参数')
            self.help_msg()

    def help_msg(self):
        '''帮助信息'''
        msg = '''
        dbtest                         测试数据库连接
        people                         查询注册总人数
        regpeople  <yyyy-mm-dd>        查询某日注册总的用户数，默认为当日
        pay        <yyyy-mm-dd>        查询某日支付用户数，默认为当日
        record     <yyyy-mm-dd>        查询某日游戏记录较多的用户数，默认为当日
        active     <yyyy-mm-dd>        查询某日活跃的用户数，默认为当日
        inputs     <yyyy-mm-dd>        查询某日投入前100的玩家数，默认为当日（即时查询）
        outputs    <yyyy-mm-dd>        查询某日产出前100的玩家数，默认为当日（即时查询）
        revenues   <yyyy-mm-dd>        查询某日游戏的营收（默认为昨日，超过昨天日期默认为昨日）
        win_rank   <yyyy-mm-dd>        查询某日赢前100的玩家
        lose_rank  <yyyy-mm-dd>        查询某日输前100的玩家
        '''
        print(msg)

    def dbtest(self):
        '''
        测试数据库连接
        :return:
        '''
        test_db()

    # def date_oper(self,srt_time):
    #     '''
    #     日期处理
    #     :param srt_time:
    #     :return: 返回当前日期后一天的日期
    #     '''
    #     try:
    #         now=datetime.datetime.strptime(srt_time,'%Y-%m-%d')
    #         now_later=now+datetime.timedelta(days=1)
    #         return  now_later.strftime('%Y-%m-%d')
    #     except ValueError:
    #         print("请输入正确的日期格式")
    #         sys.exit(600)

    def regpeople(self):
        '''
        默认查询当日注册总人数
        :return:
        '''
        self.Satisfy_db(self.engine01,self.query_db,re.compile(r'^userInfo_[0-9]{3}'),'qure_res')
        # self.Satisfy_db(self.engine02)
        self.reg_out_put()

    def people(self):
        '''
        查询总注册人数
        :return:
        '''
        self.Satisfy_db(self.engine01,self.query_db,re.compile(r'^userInfo_[0-9]{3}'),'qure_all')
        self.all_people_out()

    def pay(self):
        '''
        查询支付情况
        :return:
        '''
        self.Satisfy_db(self.engine02,self.query_db,re.compile(r'^payInfo_[0-9]{3}'),'qure_pay')
        self.pay_out_put()

    def record(self):
        '''
        查询游戏记录
        :return:
        '''
        mongo_fun = Mongo_DBs(self.data_time,self.GAME_COUNT_NUM)
        self.count_list(mongo_fun.game_record())
        self.record_out_put()

    def active(self):
        '''
        查询活跃用户数
        :return:
        '''
        self.pay()
        self.record()
        self.active_out_put()

    def inputs(self):
        '''
        查询玩家产出前100
        :return:
        '''
        redis_fun=Redis_DBs(self.data_time,'redis_input')
        self.redis_list = redis_fun.dofun()
        self.player_out_put('input')

    def outputs(self):
        '''
        查询玩家投入前100
        :return:
        '''
        redis_fun=Redis_DBs(self.data_time,'redis_output')
        self.redis_list = redis_fun.dofun()
        self.player_out_put()

    def revenues(self):
        '''玩家游戏营收情况'''
        mongo_fun=Mongo_DBs(self.data_time,self.GAME_COUNT_NUM)
        self.mongo_list = mongo_fun.revenue()
        DataManager.num_dict_initialize() # 初始化字典
        self.mongo_dict = DataManager.openr_games(self.mongo_list)
        # print(self.mongo_dict)
        # self.player_revenues_output()

    def win_rank(self):
        '''每日赢前100的玩家'''
        # mongo_fun = Mongo_DBs(self.data_time, self.GAME_COUNT_NUM)
        mongo_fun = Mongo_DBs(self.data_time, self.GAME_COUNT_NUM)
        self.mongo_list=mongo_fun.win_record()
        print(self.mongo_list)
        self.rank_out('win')

    def lose_rank(self):
        '''每日输前100的玩家'''
        # mongo_fun = Mongo_DBs(self.data_time, self.GAME_COUNT_NUM)
        mongo_fun = Mongo_DBs(self.data_time, self.GAME_COUNT_NUM)
        self.mongo_list=mongo_fun.lose_record()
        self.rank_out()

    def Satisfy_db(self,engine,fun,pattern,db_fun):
        '''
        库内列表遍历函数
        :param engine:
        :return:
        '''
        db_funs = db_fun
        SessionCls = sessionmaker(bind=engine)
        session = SessionCls()

        inspector = inspect(engine)

        print('%s引擎查询中，请稍候...' % engine)
        for table_name in inspector.get_table_names():
            # 使用re做表名的判断过滤，然后再查询
            if pattern.match(table_name):
                fun(table_name,session,db_funs)
        session.close()

    # def querys_db(self,table_name,session):
    #     '''
    #     查询功能方法，已被query_db方法替换
    #     :param table_name:
    #     :param session:
    #     :return:
    #     '''
    #     ##日期处理##
    #     reg_time_later=self.date_oper(self.data_time)
    #     # login_time_later=date_oper(login_time)
    #     base = declarative_base()
    #     # Satisfy_login_set=[]
    #     class userInfo(base):
    #         __tablename__ = table_name
    #         uid = Column(Integer, primary_key=True, autoincrement=True)
    #         loginTime = Column(DateTime)
    #         registerTime = Column(DateTime)
    #     reg_objs=session.query(userInfo).filter(and_(userInfo.registerTime>= self.data_time ,userInfo.registerTime < reg_time_later )) #注册人数
    #     # login_objs=session.query(userInfo).filter(and_(userInfo.loginTime>= login_time ,userInfo.loginTime < login_time_later))
    #     try:
    #         for index_obj in reg_objs:
    #             self.mysql_list.append(index_obj.uid)
    #         # for index in login_objs:
    #         #     Satisfy_login_set.append(index.uid)
    #     except AttributeError:
    #         print('查询的值不存在')

    def validate(self,date_text):
        '''
        检测日期格式是否正确
        :param date_text:
        :return:
        '''
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            print("日期格式不正确，格式应该为 YYYY-MM-DD 例如：2019-10-22")
            sys.exit(700)

    def reg_out_put(self):
        '''注册人数结果输出'''
        print('%s 注册人数为: %d' % (self.data_time, len(self.mysql_list)))

    def all_people_out(self):
        '''注册总人数输出'''
        all_num=0
        for index in self.mysql_list:
            all_num=all_num+index
        print('总计注册人数为: %d' % all_num)

    def pay_out_put(self):
        '''支付信息输出'''
        print('%s 支付人数为: %d' % (self.data_time, len(self.mysql_list)))
        print('支付用户uid列表: ',self.mysql_list)

    def record_out_put(self):
        '''游戏记录输出'''
        print('%s 游戏记录超过%d条的玩家数量为: %d' % (self.data_time,self.GAME_COUNT_NUM,len(self.mongo_list)))
        print('玩家uid列表：',self.mongo_list)

    def active_out_put(self):
        '''活跃玩家输出'''
        self.mysql_list.extend(self.mongo_list)
        active_set = set(self.mysql_list)
        print('%s 活跃的玩家数量为: %d' % (self.data_time,len(active_set)))
        print('活跃玩家uid列表：', list(active_set))

    def player_out_put(self,io='产出'):
        '''
        投入产出前100的输出
        '''
        informations = io
        if io=='input':
            informations = '投入'
        print('玩家 %s 前100排行如下：' % informations)
        print(self.redis_list)

    def player_revenues_output(self):

        DataManager.record_output(self.mongo_dict)

    def rank_out(self,flag='lose'):
        if flag == 'win':
            print('%s 赢的前100名玩家' % self.data_time)
            for i in self.mongo_list:
                print('%s %s' % (i['uid'],i['revenue']))
        else:
            print('%s 输的前100名玩家' % self.data_time)
            for i in self.mongo_list:
                print('%s %s' % (i['uid'],i['revenue']))

    def query_db(self,table_name,session,fun):
        '''
        调用DBfunction查询模块查询表内信息
        '''
        q_db=DBs(table_name,session,self.data_time,fun)
        res_list=q_db.dofun()
        if len(res_list) != 0:
            self.mysql_list.extend(res_list)

    def count_list(self,some_list):
        '''
        统计列表重复元素个数
        :return:
        '''
        myset = set(some_list)
        for item in myset:
            if some_list.count(item) >= 50:
                self.mongo_list.append(item)

    def data_return(self):
        '''
        模块的"API"
        外部程序import此模块时，返回输出记录给外部程序
        调用范例见：test.py 文件内的代码
        :return:
        '''
        return self.mysql_list,self.mongo_list,self.redis_list

    def dict_data_return(self):
        '''
        模块的"API"
        外部程序import此模块时，返回输出记录给外部程序
        调用范例见：test.py 文件内的代码
        :return:
        '''
        # print('此时mongo dict字典为')
        # for i in self.mongo_list:
        #     print(i)
        return self.mongo_dict

####################测试代码区###########################################
####################测试代码区END#########################################

if __name__ == '__main__':
    print('请在Coll模块中调用此模块的一切功能')
    sys.exit(101)
    # argv_check()
    # args = parser_flag()
    #
    # Satisfy_db(engine01, args.reg, args.login)
    # Satisfy_db(engine02, args.reg, args.login)
    # mysql_list = set(mysql_list)
    # # print(mysql_list)
    # print('%s 总计注册了%d人' % (args.reg,len(mysql_list)))
    #
    # Satisfy_login_set = set(Satisfy_login_set)
    # print('%s 总计登录了%d人' % (args.login,len(Satisfy_login_set)))
    #
    # #2个集合取交集，得到规定时间内即注册又登录的用户
    # Inter_set=mysql_list.intersection(Satisfy_login_set)
    # print("在%s登录，并在%s注册过的人有：%d人" % (args.login,args.reg,len(Inter_set)))
    #
    # print("在%s登录，并在%s注册的留存率：%0.2f%%" % (args.login,args.reg,(len(Inter_set)/len(mysql_list)*100)))

# li=[{'uid':2222,'uid date':'2019-10-19','gameId':3,'type':'fish','level':2,'input':99,'output':60,'revenue':-10},{'uid':22333,'uid date':'2019-10-19','gameId':2,'type':'fish','level':1,'input':10,'output':60,'revenue':50}]