#!/usr/bin/python
#coding=utf8
####################
#Author：yaoli
#Desciption：切分nginx日志
####################

import sys, re
from urllib import unquote

#定义属性类
class conf(object):
    #各正则字段
    ip = r"?P<ip>[\d.]*"
    remote_user = r"?P<remote_user>.*?"
    date = r"?P<date>\d+"
    month = r"?P<month>[A-Za-z]+"
    year = r"?P<year>\d+"
    hour = r"?P<hour>\d+"
    minute = r"?P<minute>\d+"
    second = r"?P<second>\d+"
    time_zone = r"?P<time_zone>.*?"
    method = r"?P<method>.*?"
    request = r"?P<request>.*?"
    http_p_ver = r"?P<http_p_ver>.*?"
    status = r"?P<status>.*?"
    bbs = r"?P<bbs>.*?"
    connect = r"?P<connect>.*?"
    request_time = r"?P<request_time>.*?"
    refer = r"?P<refer>.*?"
    cookie = r"?P<cookie>.*?"
    userAgent=r"?P<userAgent>.*"
    #定义request的位置，从0数起
    num = 10
    # #一共输出的列数
    length= 19
    other=r"?P<other>.*"
    #正则匹配规则
	#^(\d+\.\d+\.\d+\.\d+) - (.*?) \[(\d+)\/([A-Za-z]+)\/(\d+):(\d+):(\d+):(\d+) (.*?)\] \"(.*?) (.*?) .TTP\/(.*?)\" (.*?) (.*?) (.*?) (.*?)\"(.*?)\"(.*?) \"(.*)\"$

    p = re.compile(r'''
    ^(%s)\ -\ (%s)\ \[(%s)\/(%s)\/(%s):(%s):(%s):(%s)\ (%s)\]\ \"(%s)\ (%s)\ .TTP\/(%s)\"\ (%s)\ (%s)\ (%s)\ (%s)\"(%s)\"(%s)\ \"(%s)\"$
    ''' %( ip, remote_user, date, month, year, hour, minute, second, time_zone, method, request, http_p_ver, status, bbs, connect, request_time, refer, cookie, userAgent ), re.VERBOSE)

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
            print logStr
        #如果匹配未成功，输出空列
        else:
            #map字段为空
            emptyMap = {}
            emptyList = [''] * (self.lengh - 1)
            #将空map字符串插入列表最后一位
            emptyList.append(str(emptyMap))
            emptyList[self.i] = self.log
            emptyStr = '\t'.join(emptyList)
            print emptyStr
            

    #def splitMap(self, logStr):
    #    logList = logStr.split('?')
    #    keyValueList = []
    #    listLog = logList[1].split('&')
    #    for i in listLog:
    #        elementList = i.split('=')
    #        keyValueList.append('\003'.join(elementList))
    #    mapLogStr = '\002'.join(keyValueList)
    #    return mapLogStr

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
        # input comes from STDIN (standard input)
        for line in sys.stdin:
            # remove leading and trailing whitespace
            log = line.strip('\n')
            #定义解析类对象
            matchLogTarget = matchLog(log, confTarget.p, confTarget.num, confTarget.length)
            matchLogTarget.analyze()

if __name__ == '__main__':
    main = Main()
    main.main()
