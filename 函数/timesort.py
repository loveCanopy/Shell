#!/usr/bin/python
#coding=utf8

import sys


#用于记录上一条记录的用户名
lastusername = ''
#用于记录上一条记录的行为
lastactiontype = ''
#用于记录上一条记录的关键词
lastkeyword = ''
#用于对应检索和检索点击
num = 0

# input comes from STDIN (standard input)
for line in sys.stdin:
  
  # remove leading and trailing whitespace
  line = line.strip('\n')

  # split the line into words
  words = line.split("\t")

  #用户名
  username = words[0]

  #时刻
  timecut = words[1]

  #行为类型
  actiontype = words[2]

  #关键词
  keyword = words[3]

  if actiontype == "search" :

    #若为检索行为记录，则输出
    print "%s\t%s\t%s\t%s" % ( username, timecut, actiontype, keyword )

    lastactiontype = actiontype
    lastusername = username
    lastkeyword = keyword

  else:

    #输出同一个用户search后的第一个点击行为记录
    if lastactiontype == "search" and lastusername == username :

      print "%s\t%s\t%s\t%s" % ( username, timecut, actiontype, lastkeyword )

      lastactiontype = actiontype
      lastusername = username
      lastkeyword = ''

    else :

      lastactiontype = actiontype
      lastusername = username
      lastkeyword = ''
