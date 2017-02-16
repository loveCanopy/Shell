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
## 比对文件大小
```
num=`hadoop fs -ls bos://bigdata2/music/compress/music_log/event_day=201605${k}/event_hour=*/event_log_source=${i} | awk '/bos/{print $3,$6}' | awk '{num+=$1} END {print num}'`

```
## 比对文件数
```
num=`hadoop fs -count -q bos://bigdata2/music/compress/music_log/event_day=201604${k}/event_hour=*/event_log_source=${i}  | awk '{print $5,$6}' | awk '{num+=$2} END {print num}'`

```
