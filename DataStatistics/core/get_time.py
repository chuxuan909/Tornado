import http.client
import time
import os
def get_webservertime(host):
    conn=http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r=conn.getresponse()
    #r.getheaders() #获取所有的http头
    ts=  r.getheader('date') #获取http头date部分
    #将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
   # print(ltime)
    ttime=time.localtime(time.mktime(ltime)+8*60*60)
  #  print(ttime)
    day=ttime.tm_mday
    if ttime.tm_mday < 10:
        day = '0%s' % ttime.tm_mday
    dat="%s-%s-%s" % (ttime.tm_year,ttime.tm_mon,day)
#    tm="date -s %02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
#    print (dat)
    return dat
    #os.system(dat)
#    os.system(tm)
get_webservertime('www.baidu.com')
