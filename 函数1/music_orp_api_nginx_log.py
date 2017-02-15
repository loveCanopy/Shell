#!/usr/bin/python
#coding=utf8
#################
#Author：tongyue
#Description：切分music_api_nginx_log日志

import sys, re
from urllib import unquote

#定义属性类
class conf(object):
    #定义request的位置，从0数起
    num = 11
    # #一共输出的列数
    length= 27
    #正则匹配规则
    p = re.compile('''
    ^(.*?)\ \-\ (.*?)\ \[(.*?)\/(.*?)\/(.*?):(.*?):(.*?):(.*?)\ (.*?)\]\ cost=(.*?)\ \"(.*?)\ (.*?)\ .TTP\/(.*?)\"\ (.*?)\ (.*?)\ \"(.*?)\"\ \"(.*?)\"\ \"(.*?)\"\ (.*?)\ (.*?)\ (.*?)\ (.*?)\ (.*?)\ \"(.*?)\"\ (.*?)\ (.*?)\ (.*)$
    ''', re.VERBOSE)

#定义解析log的类，用于匹配、解析nginx日志
class matchLog(object):

    #定义基本属性,log为原始日志，logPattern为正则格式，i为参数列的位置序列号（从0开始），lenth为总列数
    log = ''
    logPattern = ''
    i = ''
    lengh = ''

    #定义构造方法
    def __init__(self, log, logPattern, i, lengh):
        #原log日志
        self.log = log
        #log的正则匹配对象
        self.logPattern = logPattern
        #参数列字符串的序列号，从0开始
        self.i = i
        #一共输出的列的个数
        self.lengh = lengh

    #定义解析nginx日志的方法
    def analyze(self):
        #用log匹配正则表达式
        logMatch = self.logPattern.match(self.log)
        #如果匹配成功，则输出
        if logMatch:
            logList = list(logMatch.groups())
            #将参数列字符串放置在最后一列
            logList.append(self.log)
            #切分参数列，并互换参数列字符串和参数map字符串
            logList[self.lengh] = self.splitMap(logList[self.i])
            #拼成字符串，以便输出
            logStr = '\t'.join(logList)
            print(logStr)
        #如果匹配未成功，输出空列
        else:
            #map字段为空
            emptyMap = {}
            emptyList = [''] * (self.lengh - 1)
            #将空map字符串插入列表最后一位
            emptyList.append(str(emptyMap))
            emptyList[self.i] = self.log
            emptyStr = '\t'.join(emptyList)
            print(emptyStr)

    def splitMap(self, logStr):
        #只按第一个?切分
        logList = logStr.split('?', 1)
        keyValueList = []
        if len(logList) == 2 and logList[1] != '':
            listLog = logList[1].split('&')
            for i in listLog:
                elementList = i.split('=')
                if len(elementList) != 2:
                    elementList.append('')
                elementList[0]=unquote(elementList[0])
                elementList[1]=unquote(elementList[1])
                keyValueList.append('\003'.join(elementList))
            mapLogStr = '\002'.join(keyValueList)
        else:
            elementList = ["",""]
            keyValueList.append('\003'.join(elementList))
            mapLogStr = '\002'.join(keyValueList)
        return mapLogStr

    #判断变量v是否存在
    def isset(self, v):
        try:
            type(eval(v))
        except:
            return 0
        else:
            return 1


class Main(object):
    def main(self):
        #定义配置类对象
        confTarget = conf()
        # # input comes from STDIN (standard input)
        # line='114.239.175.82 - - [14/Aug/2016:00:03:00 +0800] cost=0.006 "GET /api/v1/tactics?format=jsonp&callback=jQuery172012914442969486117_1471104178992&from=pcweb&product=music&listenType=8&_=1471104179363 HTTP/1.1" 200 196 "http://play.baidu.com/?__m=mboxCtrl.playSong&__a=267378536&__o=/search||songListIcon&fr=ps||www.baidu.com&__s=%E4%BB%BB%E6%84%8F%E4%BE%9D%E6%81%8B" "BAIDUID=0311040BFB26DC3D73E0868350CF5013:FG=1; BIDUPSID=EF79B5F416FF12B8DF0F289E577750B9; PSTM=1442990461; BDUSS=FuQUtDZ2dCOHNETHB5RVNBNmZaWHRINHN2bGZRN2Y2T2FVZ1VOUzIya2NNckJXQVFBQUFBJCQAAAAAAAAAAAEAAABpFul9ztK63M~rxOO2rLasAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAByliFYcpYhWSm; pgv_pvi=1567980544; pgv_si=s5876406272; BDRCVFR[8gzLr2xelNt]=IdAnGome-nsnWnYPi4WUvY; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=20739_1449_18240_17948_18559_12297_19439_20848_20856_20836_20771_20781; fmtip=14; Hm_lvt_d0ad46e4afeacf34cd12de4c9b553aa6=1471104173; Hm_lpvt_d0ad46e4afeacf34cd12de4c9b553aa6=1471104173; tracesrc=ps%7C%7Cwww.baidu.com; u_lo=0; u_id=; u_t=; TOPMSG=1471104174-0" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0" 0.006 - - 192.168.0.77 unix:/home/work/orp/var/hhvm.sock baifen.music.baidu.com "-" orp orp 01803295201291888832081400'
        # # remove leading and trailing whitespace
        # log = line.strip('\n')
        # #去掉前后空格
        # log = log.strip()
        # #定义解析类对象
        # matchLogTarget = matchLog(log, confTarget.p, confTarget.num, confTarget.length)
        # matchLogTarget.analyze()

        for line in sys.stdin:
            # remove leading and trailing whitespace
            log = line.strip('\n')
            #去掉前后空格
            log = log.strip()
        #定义解析类对象
            matchLogTarget = matchLog(log, confTarget.p, confTarget.num, confTarget.length)
            matchLogTarget.analyze()

if __name__ == '__main__':
    main = Main()
    main.main()
