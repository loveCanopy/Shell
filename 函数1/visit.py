#!/usr/bin/python
#coding=utf8
#2016.06.29 zgy
#本脚本用于计算PCWEB用户访次+访问时长，用大于30分钟的访问间隔切分访次
import sys,time

#test=time.strptime(time, "%Y-%b-%d %H:%M:%S")

#用于对应时间序列游标
low = 0
#用于存储有效访问次数
visit_pv = 1
#用于存储有效访问时间
visit_time = 0
#用于存储一次访问就离开的用户
visit_one_pv = 0
#用于存储baiduid
event_baiduid = ''
#用于存储时间序列的list
time_series=[]
#用于存储上一次event_baiduid
last_baiduid = ''
#用于存储product
event_product= ''

# input comes from STDIN (standard input)
for line in sys.stdin:
  
  # remove leading and trailing whitespace
  line = line.strip('\n')

  # split the line into words
  words = line.split("\t")

  #存储baiduid
  event_baiduid = words[1]

  #存储product
  event_product = words[2]

  if (last_baiduid<>event_baiduid and last_baiduid<>''):
    #---输出上一个baiduid的结果
    if (len(time_series) > 1):
      #--计算访次和时间
      for i in range(len(time_series)-1): 
        if (time_series[i+1] - time_series[i] > 1800):
          #判断一次性访问，用于计算跳出率
          if (low == i):
            visit_one_pv += 1
          #计算访次及访问时间
          visit_pv += 1
          visit_time += time_series[i] - time_series[low]
          low = i+1
      #--计算单词访问
      if (time_series[-1] - time_series[-2] > 1800):
        visit_one_pv += 1
    else:
      visit_one_pv += 1
    visit_time += time_series[-1] - time_series[low]
    print "%d\t%d\t%d\t%s\t%s" % ( visit_pv , visit_one_pv , visit_time , last_baiduid , event_product)
  
    #---重置，清空
    low = 0
    visit_pv = 1
    visit_time = 0
    visit_one_pv = 0
    time_series=[]    

  #转换成时间戳形式入list
  time_series.append(time.mktime(time.strptime(words[0], "%Y-%m-%d %H:%M:%S")))
  last_baiduid=event_baiduid

#---输出最后一个baiduid的结果
if (len(time_series) > 1):
  for i in range(len(time_series)-1):
    if (time_series[i+1] - time_series[i] > 1800):
      #判断一次性访问，用于计算跳出率
      if (low == i):
        visit_one_pv += 1
      #计算访次及访问时间
      visit_pv += 1
      visit_time += time_series[i] - time_series[low]
      low = i+1
  if (time_series[-1] - time_series[-2] > 1800):
    visit_one_pv += 1
else:
  visit_one_pv += 1
visit_time += time_series[-1] - time_series[low]
print "%d\t%d\t%d\t%s\t%s" % ( visit_pv , visit_one_pv , visit_time , event_baiduid , event_product )
