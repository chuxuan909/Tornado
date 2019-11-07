#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,DateTime
from sqlalchemy import and_
import datetime
import sys
class DBs(object):
    def __init__(self,table_name,session,data_time,function):
        self.table_name=table_name
        self.session=session
        self.data_time=data_time
        self.base=declarative_base()
        self.function=function
        self.li=[]

    def dofun(self):
        if hasattr(self,self.function):
            func=getattr(self,self.function)
            func()
            return self.li
        else:
            print('DBfunction 模块无此方法')
            sys.exit(101)

    def qure_res(self):
        '''
        指定时间（默认为当天）
        注册人数查询
        :return:
        '''
        class userInfo(self.base):
            __tablename__ = self.table_name
            uid = Column(Integer, primary_key=True, autoincrement=True)
            loginTime = Column(DateTime)
            registerTime = Column(DateTime)
        reg_time_later = self.date_oper(self.data_time)
        reg_objs = self.session.query(userInfo).filter(and_(userInfo.registerTime >= self.data_time,userInfo.registerTime < reg_time_later))
        if reg_objs.count() != 0:
            try:
                for index_obj in reg_objs:
                    self.li.append(index_obj.uid)
                # for index in login_objs:
                #     Satisfy_login_set.append(index.uid)
            except AttributeError:
                print('查询的值不存在')

    def qure_all(self):
        '''
        总注册人数查询
        :return:
        '''
        class userInfo(self.base):
            __tablename__ = self.table_name
            uid = Column(Integer, primary_key=True, autoincrement=True)
            loginTime = Column(DateTime)
            registerTime = Column(DateTime)
        '''
        表记录数统计
        :return:
        '''
        self.li.append(self.session.query(userInfo).count())

    def qure_pay(self):
        '''
        指定时间（默认为当天）
        支付人数查询
        :return:
        '''
        class payInfo(self.base):
            __tablename__ = self.table_name
            uid = Column(Integer, primary_key=True, autoincrement=True)
            flag = Column(Integer)
            registerTime = Column(DateTime)
        reg_time_later = self.date_oper(self.data_time)
        pay_objs= self.session.query(payInfo).filter(and_(payInfo.registerTime >= self.data_time, payInfo.registerTime < reg_time_later,payInfo.flag==1))
        if pay_objs.count() != 0:
            try:
                for index_obj in pay_objs:
                    self.li.append(index_obj.uid)
                # for index in login_objs:
                #     Satisfy_login_set.append(index.uid)
            except AttributeError:
                print('查询的值不存在')

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
            sys.exit(602)
