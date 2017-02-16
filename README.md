# Shell
shell代码整理
## 后台执行
```
hadoop fs -cp $file bos://bigdata2/music/compress/music_log/event_day=${year}${month}${day}/event_hour=${hour}/event_log_source=${log_source} &
pids=(${pids[*]} $!)


cnt=0
echo 'Start Background Pids: '${pids[@]}
for pid in ${pids[@]}
do
    echo 'Wait Pid  '$pid
    wait $pid
    if [ $? -eq 0 ]; then
        ((cnt++))
    fi
done

end=`date +"%Y-%m-%d %H:%M:%S"`

if [ $cnt -ne ${#pids[@]} ]; then
        exit 1
else
	echo "[$end] Rsync file success"
fi
```
## 

