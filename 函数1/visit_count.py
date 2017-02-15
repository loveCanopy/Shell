#!/usr/bin/python
#coding=utf8
#2016.07.04 zgy
#本脚本用于计算PCWEB页面访问所属访次，用大于30分钟的访问间隔切分访次
#stdin:event_time	event_baiduid	event_product	event_url
#stdout:event_baiduid	event_product	event_url	visit_pv	visit_flag	event_time
import sys,time

#用于存储是否是首次访问的标记，1为是，0位否
first_flag = 1
#用于存储是否是末次访问的标记，1为是，0为否
last_flag = 0
#用于存储访问所属访次
visit_pv = 1
#用于存储访问状态，默认：0，首次：1，最后一次：2，单次访问：3
visit_flag = 3
#用于存储baiduid
event_baiduid = ''
#用于存储上一次event_baiduid
last_baiduid = ''
#用于存储product
event_product = ''
#用于存储url
event_url = ''
#用于存储访问时间
event_time = ''


# input comes from STDIN (standard input)

line1 = sys.stdin.readline()
line1 = line1.strip('\n')
words1 = line1.split('\t')
event_time = words1[0]
event_baiduid = words1[1]
event_product = words1[2]
event_url = words1[3]

for line in sys.stdin:
  
  # remove leading and trailing whitespace
  line = line.strip('\n')

  # split the line into words
  words = line.split("\t")

  test=words[0]
  #判断上一条访问是否是末次访问,并判断上次访问的状态
  if ( ( time.mktime(time.strptime(words[0] , "%Y-%m-%d %H:%M:%S")) - time.mktime(time.strptime(event_time, "%Y-%m-%d %H:%M:%S")) > 1800 ) or event_baiduid <> words[1] ):
    last_flag = 1
  else:
    last_flag = 0

  if ( last_flag == 1 and first_flag == 1 ):
    visit_flag = 3
  elif ( last_flag == 1 and first_flag == 0 ):
    visit_flag = 2
  elif ( last_flag == 0 and first_flag == 1 ):
    visit_flag = 1
  else:
    visit_flag = 0
    
  #输出上次访问的结果
  print "%s\t%s\t%s\t%d\t%d\t%s" % ( event_baiduid , event_product , event_url , visit_pv , visit_flag , event_time)

  #计算本次访问的first_flag及visit_pv，以上次访问是否是末次访问为依据
  if ( last_flag == 1):
    first_flag = 1
    if ( event_baiduid == words[1] ):
      visit_pv += 1
    else:
      visit_pv = 1
  else:
    first_flag = 0

  #本行数据保存：event_baiduid,event_product,event_url
  event_time = words[0]
  event_baiduid = words[1]
  event_product = words[2]
  event_url = words[3]


#对最后一条记录的访问情况进行判断
if ( first_flag == 1 ):
  visit_flag = 3
else: 
  visit_flag = 2

#输出末次访问的结果
  print "%s\t%s\t%s\t%d\t%d\t%s" % ( event_baiduid , event_product , event_url , visit_pv , visit_flag , event_time)
