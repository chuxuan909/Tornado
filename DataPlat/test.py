#!/usr/bin/env python
# -*- coding:utf-8 -*-

date_dict={
    1:[1,2,3,4,5,6,7],
    2:[8,9,10,11,12,13,14],
    3:[15,16,17,18,19,20,21],
    4:[22,23,24,25,26,27,28],
    5:[29,30,31],
}


def get_date_day(date_time_string):
    global date_dict
    date_index = int(date_time_string.split('-')[2])
    for key in date_dict:
        try:
            return key,date_dict[key].index(date_index)
        except:
            continue

date_time='2019-11-06'

x,y=get_date_day(date_time)
print(x,y)

def date_format_fun(date_format,date_list_num):
    if date_list_num <= 9:
        print('%s-%s-0%s' % (date_format.split('-')[0], date_format.split('-')[1], date_list_num))
    else:
        print('%s-%s-%s' % (date_format.split('-')[0], date_format.split('-')[1], date_list_num))

for i in range(1,x+1):
    if i==x:
        for index in range(len(date_dict[i][:y])+1):
            date_format_fun(date_time,date_dict[i][index])
            # if date_dict[i][index] <= 9:
            #     print('%s-%s-0%s' % (date_time.split('-')[0],date_time.split('-')[1],date_dict[i][index]))
            # else:
            #     print('%s-%s-%s' % (date_time.split('-')[0], date_time.split('-')[1], date_dict[i][index]))
    else:
        for index in range(len(date_dict[i])):
            date_format_fun(date_time, date_dict[i][index])
            # if date_dict[i][index] <= 9:
            #     print('%s-%s-0%s' % (date_time.split('-')[0],date_time.split('-')[1],date_dict[i][index]))
            # else:
            #     print('%s-%s-%s' % (date_time.split('-')[0], date_time.split('-')[1], date_dict[i][index]))



