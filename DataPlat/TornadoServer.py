#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tornado.web import RequestHandler,Application,url
from tornado.httpserver import HTTPServer
from tornado.options import options,define,parse_command_line
from tornado.ioloop import IOLoop
import os,sys
import time,datetime

#查询模块路径
DataGo_Path='F:/PythonBuild/DataStatistics'
# DataGo_Path='/home/Tornado/DataStatistics' #linux下路径

#环境变量
sys.path.append(DataGo_Path)
from core import DataGo

#变量
reflect_zh_dict={
    'regpeople':'注册人数',
    'people':'总注册人数',
    'pay':'支付人数',
    'record':'游戏活跃（记录大于50条）人数',
    'active':'活跃人数',
    'inputs':'玩家ID',
    'outputs':'玩家ID',
    'win_rank':'玩家ID',
    'lose_rank':'玩家ID',
    'gold':'金币',
}

s_moth_list=[4,6,9,11]

spea_moth_list=[2]

date_dict={
    1:[1,2,3,4,5,6,7],
    2:[8,9,10,11,12,13,14],
    3:[15,16,17,18,19,20,21],
    4:[22,23,24,25,26,27,28],
    5:[29,30,31],
}

define('port',default=9091,help='web服务监听端口',type=int)

class IndexHandler(RequestHandler):
    def prepare(self):
        # self.revenues_dict={'fish': [-6510, 115750, 154500],
        #     'doll': [0, 0, 8010000],
        #     'chess': {'classic': [50, 2000, 0],
        #               'slander': [50, 2000, 0],
        #               'double_slander': [50, 3000, 0]
        #               },
        #     'turntable': [0, 0, 620000],
        #     'total': [8900890]
        #     }

        self.group_regpeople_dict={}
        self.revenues_url = self.reverse_url("revenus")
        self.col_url = self.reverse_url("col")
        self.s_moth = None
        # self.now_time = get_date_time() # 当前日期
        # # self.now_time = '2019-10-21' # 当前日期
        # self.pange_x,self.page_y = get_date_day(self.now_time)
        # self.page_list = list(range(1,self.pange_x+1))
        # self.data_time=date_oper_before(get_date_time())
        # self.revenues_dict=get_info_ditc('revenues',self.data_time)
        # mysql_list,mongo_list,redis_list = get_info_list('people', self.now_time)
        # self.all_people_list = mysql_list+mongo_list+redis_list
        #

        # mysql_list, mongo_list, redis_list = get_info_list('active', self.now_time)
        # all_list= mysql_list+mongo_list+redis_list
        # self.active_list = list(set(all_list))
        # print(self.revenues_dict)
        global now_time,pange_x,page_y,page_list,data_time,all_people_list,revenues_dict
        self.now_time=now_time
        self.pange_x=pange_x
        self.revenues_dict=revenues_dict
        self.page_y=page_y
        self.page_list=page_list
        self.data_time=data_time
        self.all_people_list=all_people_list

    def get(self):
        # print('%s,%s' % (self.pange_x,self.page_y))
        datas={
            'show_dicts':self.revenues_dict,
            'date_time':self.data_time,
            'now_time':self.now_time,
            'all_people_list': self.all_people_list,
            'page_list':self.page_list,
            'page_x': self.pange_x,
            'page_y': self.page_y,
            'group_regpeople_dict':self.group_regpeople_dict,
            'revenues_url':self.revenues_url,
            'col':self.col_url,
            's_moth':self.s_moth
        }
        self.render("index.html",**datas)

    def post(self):
        global reflect_zh_dict
        pots_kind_data=self.get_argument('kinds',None)
        pots_time_data=self.get_argument('date_time',None)
        pots_stime_data=self.get_argument('s_time',None)
        mysql_list,mongo_list,redis_list=get_info_list(pots_kind_data,pots_time_data)
        # print(mysql_list,mongo_list,redis_list)
        finally_list=mysql_list+mongo_list+redis_list
        # finally_list=list(set(finally_list))
        if pots_kind_data == 'active':
            finally_list = list(set(finally_list))
        # print(pots_stime_data)
        # print(finally_list)

        datas={
            'show_dicts':self.revenues_dict,
            'col_list':finally_list,
            'kind':pots_kind_data,
            'reflect_zh_dict':reflect_zh_dict,
            'pots_time_data': pots_time_data,
            'date_time': self.data_time,
            'now_time': self.now_time,
            'page_list': self.page_list,
            'all_people_list': self.all_people_list,
            'page_x': self.pange_x,
            'page_y': self.page_y,
            'group_regpeople_dict': self.group_regpeople_dict,
            'revenues_url': self.revenues_url,
            'col': self.col_url,
            's_moth':self.s_moth,
        }

        self.render('collect.html',**datas)



    def get_template_namespace(self):
        '''函数加入模板运行'''
        namespace = {}
        namespace = super(IndexHandler, self).get_template_namespace()
        uimethods = {
            "date_time": get_date_time(),
            "all_people": people,
            "count_list": count_list,
            "negate": Negate_num,
        }
        namespace.update(uimethods)
        return namespace


class RevenusHandler(RequestHandler):
    def post(self):
        global reflect_zh_dict,all_people_list,page_list,pange_x,page_y
        self.page_y=page_y
        self.pange_x=pange_x
        self.page_list=page_list
        self.s_moth = None
        self.all_people_list = all_people_list
        self.group_regpeople_dict={}
        self.col_url=self.reverse_url('col')
        self.now_time = get_date_time()  # 当前日期
        pots_stime_data = self.get_argument('s_time', None)
        # print(pots_stime_data)
        revenues_dict = get_info_ditc('revenues', pots_stime_data)
        # print(revenues_dict)
        datas={
            'show_dicts':revenues_dict,
            'reflect_zh_dict':reflect_zh_dict,
            'date_time':  pots_stime_data,
            'now_time': self.now_time,
            'col': self.col_url,
            'group_regpeople_dict': self.group_regpeople_dict,
            'all_people_list': self.all_people_list,
            'page_list':self.page_list,
            'page_x': self.pange_x,
            'page_y': self.page_y,
            's_moth':self.s_moth,
        }

        self.render('revenus.html', **datas)

    def get_template_namespace(self):
        '''函数加入模板运行'''
        namespace = {}
        namespace = super(RevenusHandler, self).get_template_namespace()
        uimethods = {
            "date_time": get_date_time(),
            "all_people": people,
            "count_list": count_list,
            "negate": Negate_num,
        }
        namespace.update(uimethods)
        return namespace

class PageHandler(RevenusHandler):
    def prepare(self):
        self.col_url = self.reverse_url("col")
        self.revenues_url = self.reverse_url("revenus")
        self.now_time = get_date_time()
        self.format_time=self.now_time
        self.day_list=[]
        self.data_time = date_oper_before(get_date_time())
        self.revenues_dict = get_info_ditc('revenues', self.data_time)
        mysql_list,mongo_list,redis_list = get_info_list('people', self.now_time)
        self.all_people_list = mysql_list+mongo_list+redis_list

    def get(self,pages,index_x,index_y):
        global date_dict
        group_regpeople_dict={}
        group_active_dict={}
        self.page_list = list(range(1, int(index_x) + 1))
        self.page_list.reverse()
        s_moth=self.get_argument('s_moth',None)
        s_moth_end = '%s-31' % s_moth
        if s_moth and s_moth_end < self.now_time:
            index_x,index_y=get_date_day(s_moth_end)
            self.page_list = list(range(1, int(index_x) + 1))
            self.page_list.reverse()
            self.format_time=s_moth_end
        if pages==index_x:
            for i in date_dict[int(pages)][:int(index_y)+1]:
                self.day_list.append(date_format_fun(self.format_time, i))
                # date_format_fun(self.now_time, i)
        else:
            for i in date_dict[int(pages)]:
                self.day_list.append(date_format_fun(self.format_time, i))
                # date_format_fun(self.now_time, i)
        # print(self.day_list)
        self.day_list.reverse()
        # print(self.day_list)
        for l_index in self.day_list:
            mysql_list,  mongo_list,  redis_list = get_info_list('regpeople', l_index)
            regpeople_list =  mysql_list +  mongo_list +  redis_list
            group_regpeople_dict[l_index]=regpeople_list
            mysql_list, mongo_list, redis_list = get_info_list('active', l_index)
            active_list = mysql_list + mongo_list + redis_list
            active_list = list(set(active_list))
            group_active_dict[l_index]=active_list
        # print(group_regpeople_dict)
        # print('=====')
        # print(group_active_dict)

        datas={
            'show_dicts':self.revenues_dict,
            'date_time':self.data_time,
            'now_time':self.now_time,
            'all_people_list': self.all_people_list,
            'page_list':self.page_list,
            'page_x': int(index_x),
            'page_y': int(index_y),
            'day_list':self.day_list,
            'group_regpeople_dict':group_regpeople_dict,
            'group_active_dict':group_active_dict,
            'revenues_url':self.revenues_url,
            'col': self.col_url,
            's_moth':s_moth,
        }
        self.render("pages.html",**datas)

    def get_template_namespace(self):
        '''函数加入模板运行'''
        namespace = {}
        namespace = super(PageHandler, self).get_template_namespace()
        uimethods = {
            "count_list": count_list,
        }
        namespace.update(uimethods)
        return namespace


def get_date_time():
    return time.strftime("%Y-%m-%d", time.localtime())

def people(conm_list):
    '''
    注册人数统计
    列表元素相加
    '''
    all_num = 0
    for index in conm_list:
        all_num = all_num + index
    return all_num

def count_list(conm_list):
    '''指定日期的支付、注册人数
    列表长度
    '''
    return len(conm_list)


def ope_date(data_time):
    if int(data_time.split('-')[1]) in s_moth_list and data_time.split('-')[2] == '31':
        return '%s-%s-30' % (data_time.split('-')[0],data_time.split('-')[1])
    elif int(data_time.split('-')[1]) in spea_moth_list and data_time.split('-')[2] == '30':
        return '%s-%s-28' % (data_time.split('-')[0], data_time.split('-')[1])
    elif int(data_time.split('-')[1]) in spea_moth_list and data_time.split('-')[2] == '31':
        return '%s-%s-28' % (data_time.split('-')[0], data_time.split('-')[1])
    elif int(data_time.split('-')[1]) in spea_moth_list and data_time.split('-')[2] == '29':
        return '%s-%s-28' % (data_time.split('-')[0], data_time.split('-')[1])
    else:
        return data_time

def get_info_list(col_function,data_time):
    # if col_function == 'active':
    #     pass
    # else:
    #     col_obj = DataGo.Collets([None, col_function, data_time])
    #     return col_obj.data_return()
    #
    data_time = ope_date(data_time)
    print('data_time is ',data_time)
    col_obj = DataGo.Collets([None, col_function, data_time])
    return col_obj.data_return()

def get_info_ditc(col_function,data_time):
    col_obj = DataGo.Collets([None,col_function,data_time])
    return col_obj.dict_data_return()

def date_oper_before(srt_time):
    '''
    日期处理
    :param srt_time:
    :return: 返回当前日期前一天的日期
    '''
    try:
        now=datetime.datetime.strptime(srt_time,'%Y-%m-%d')
        now_later=now-datetime.timedelta(days=1)
        return  now_later.strftime('%Y-%m-%d')
    except ValueError:
        print("请输入正确的日期格式")
        sys.exit(601)

def Negate_num(num):
    return -num

def get_date_day(date_time_string):
    global date_dict
    date_index = int(date_time_string.split('-')[2])
    for key in date_dict:
        try:
            return key,date_dict[key].index(date_index)
        except:
            continue

def date_format_fun(date_format,date_list_num):
    if date_list_num <= 9:
        print('%s-%s-0%s' % (date_format.split('-')[0], date_format.split('-')[1], date_list_num))
        return '%s-%s-0%s' % (date_format.split('-')[0], date_format.split('-')[1], date_list_num)
    else:
        print('%s-%s-%s' % (date_format.split('-')[0], date_format.split('-')[1], date_list_num))
        return '%s-%s-%s' % (date_format.split('-')[0], date_format.split('-')[1], date_list_num)



if __name__=='__main__':

    now_time = get_date_time()
    # now_time = '2019-11-30'
    pange_x, page_y = get_date_day(now_time)
    page_list = list(range(1, pange_x + 1))
    page_list.reverse()
    print(page_list)
    data_time = date_oper_before(get_date_time())
    revenues_dict = get_info_ditc('revenues', data_time)
    mysql_list, mongo_list, redis_list = get_info_list('people', now_time)
    all_people_list = mysql_list + mongo_list + redis_list

    app = Application([
        (r'/',IndexHandler),
        url(r'/col',IndexHandler,name='col'),
        url(r'/Reven',RevenusHandler,name='revenus'),
        (r'/pages/(?P<pages>[0-9]{2})/(?P<index_x>[0-9])(?P<index_y>[0-9])', PageHandler),
        (r'/pages/(?P<pages>[0-9])/(?P<index_x>[0-9])(?P<index_y>[0-9])', PageHandler),
    ],
    # 项目配置信息
    # 网页模板
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    # 静态文件
    static_path=os.path.join(os.path.dirname(__file__), "static"),

    debug=False,
    )
    parse_command_line()
    server=HTTPServer(app)
    server.listen(options.port)
    IOLoop.current().start()

