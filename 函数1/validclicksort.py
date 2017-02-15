#!/usr/bin/python
#coding=utf8
#本脚本用于计算按检索结果有效点击率
import sys

#用于记录上一条记录的用户名
lastusername = ''
#用于记录上一条记录的搜索词
lastsearchkey = ''
#用于记录当前模板
validtemplate = ''
#用于对应同一搜索词出现次数
num = 0
#用于对应是否输出有效pv
validtag = 0
#用于对应是否输出搜索pv
searchtag = 0

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

  #模板
  template = words[3]
  
  #当前搜索词
  searchkey = words[4]
  
  if (username == lastusername and searchkey == lastsearchkey):
	num += 1
  else:
	num = 0
	validtag = 0
	searchtag = 0
  
  #输出搜索行为，对同一搜索词只输出一条
  if (actiontype == 'search' and searchtag == 0):
	print "%s\t%s\t%s" % ( username, actiontype, template )
	searchtag = 1
	validtemplate = template
  
  #输出有效搜索行为，同一搜索词只输出一条，判断规则为：已有有效搜搜行为同时记录条数>2
  if (validtag == 0 and searchtag == 1 and num > 1):
	print "%s\tvalidsearch\t%s" % ( username, validtemplate )
	validtag = 1
	
  lastusername = username
  lastsearchkey = searchkey