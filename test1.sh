set -x
year=$1
month=$2
day=$3
hour=$4
log_source=$5
dir_name="/music/compress/music_log/event_day=${year}${month}${day}/event_hour=${hour}/event_log_source=${log_source}"
#首先查看是否有该目录
hadoop fs -test -e $dir_name
if [ $? -eq 0 ];then
	hadoop fs -mkdir -p bos://bigdata2/music/compress/music_log/event_day=${year}${month}${day}/event_hour=${hour}/event_log_source=${log_source}
	all=`hadoop fs -ls ${dir_name}|awk '/music/{print $8}'`
	for file in $all
	do 
	echo $file
	hadoop fs -test -e $file
	if [ $? -eq 0 ];then
		hadoop fs -cp $file bos://bigdata2/music/compress/music_log/event_day=${year}${month}${day}/event_hour=${hour}/event_log_source=${log_source} &
		pids=(${pids[*]} $!)
	fi
	done
else
#源hadoop上不存在该目录，直接退出当前脚本
	exit
fi
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


