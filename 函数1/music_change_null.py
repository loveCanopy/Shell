#!/usr/bin/python

#coding:utf8

import sys  

for line in sys.stdin:  
    line = line.strip('\n')  
    arr = line.split('\t')
    i = 0
    while i<len(arr):
        #print(names[i])
        if arr[i] == '' or not arr[i] or arr[i] is None or arr[i]=='null' or arr[i]=='\\N' or arr[i]=='\N':
            arr[i]=''
        i = i+1
    str = '\t'.join(arr)
    print str  
