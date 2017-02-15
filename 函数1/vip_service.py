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
    num = 0
    #一共输出的列数
    length= 15
    #正则匹配规则
    p = re.compile('''
    ^service_id\[(.*?)\]\\tbaidu_id\[(.*?)\]\\tservice_type\[(.*?)\]\\tservice_level\[(.*?)\]\\tstart_time\[(.*?)\]\\tend_time\[(.*?)\]\\tupdate_time\[(.*?)\]\\tprice\[(.*?)\]\\tservice_quota\[(.*?)\]\\tservice_num\[(.*?)\]\\tservice_ident\[(.*?)\]\\txrank\[(.*?)\]\\tdesc\[(.*?)\]\\tfr\[(.*?)\]\\twallet_bill\[(.*?)\]$
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
            # print(self.lengh)
            #拼成字符串，以便输出
            logStr = '\t'.join(logList)
            print(logStr)
        #如果匹配未成功，输出空列
        else:
            #制造空map：mapLogStr
            keyValueList = []
            elementList = ["",""]
            keyValueList.append('\003'.join(elementList))
            mapLogStr = '\002'.join(keyValueList)

            emptyList = [''] * (self.lengh - 2)
            #将空map字符串插入列表最后两位
            emptyList.append(mapLogStr)
            emptyList.append(mapLogStr)
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

    def splitKeyValue(self, logStr):
        #按空格分隔
        logList = logStr.split(' ')
        keyValueList = []
        for logElement in logList:
            logElement = logElement.strip()
            if len(logElement) == 0:
                break
            p = re.compile('''^(.*?)\[(.*?)\]$''', re.VERBOSE)
            logMatch = p.match(logElement)
            if logMatch:
                logList = list(logMatch.groups())
                keyValueList.append('\003'.join(logList))
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
        # input comes from STDIN (standard input)
        for line in sys.stdin:
            # remove leading and trailing whitespace
            log = line.strip('\n')
            #去掉前后空格
            log = log.strip()
        #定义解析类对象
            matchLogTarget = matchLog(log, confTarget.p, confTarget.num, confTarget.length)
            matchLogTarget.analyze()

        # line='service_id[18436152]	baidu_id[57999806]	service_type[cloud]	service_level[gold]	start_time[2016-02-02 17:13:37]	end_time[2017-02-02 17:13:37]	update_time[2016-07-08 11:21:15]	price[48]	service_quota[20000]	service_num[12]	service_ident[1454404417]	xrank[2]	desc[]	fr[zfb]	wallet_bill[199806160708112044]'
        # # # ?cmd_no=16000&f=api&cuid=
        # # # remove leading and trailing whitespace
        # log = line.strip('\n')
        # #去掉前后空格
        # log = log.strip()
        # #定义解析类对象
        # matchLogTarget = matchLog(log, confTarget.p, confTarget.num, confTarget.length)
        # matchLogTarget.analyze()

if __name__ == '__main__':
    main = Main()
    main.main()
