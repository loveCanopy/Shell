#!/usr/bin/python
#coding=utf8
#本脚本用于检索优化
import sys

#用于存储上一行当前搜索词
lastwd = ''

#用于统计当前组合数量
num = 0

# input comes from STDIN (standard input)
for line in sys.stdin:
  
  # remove leading and trailing whitespace
  line = line.strip('\n')

  # split the line into words
  words = line.split("\t")

  #pv
  pv = words[0]

  #uv
  uv = words[1]

  #组合pv
  com_pv = words[2]

  #当前搜索词
  wd = words[3]
  
  #历史搜索词
  oq = words[4]
  
  #来源
  tag = words[5]
  
  if num < 20:
    print "%s\t%s\t%s\t%s\t%s" % ( pv, uv, wd, oq, tag)
  
  if wd == lastwd or lastwd == '':
    num += 1
  else :
    num = 0
	
  lastwd = wd
