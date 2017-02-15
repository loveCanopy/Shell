set -x
for i in `cat result7_check.txt`
do
event_day=`echo $i|awk -F ',' '{print $1}'`
event_hour=`echo $i|awk -F ',' '{print $2}'`
event_log_source=`echo $i|awk -F ',' '{print $3}'`
all=`hadoop fs -ls /music/compress/music_log/event_day=201607$event_day/event_hour=$event_hour/event_log_source=$event_log_source|awk '/music/{print $8}'`
	for file in $all
	do
	echo $file
	filename=`echo $file | awk -F '/' '{print $8}'`
	echo $filename
	hadoop fs -test -e bos://bigdata2/music/compress/music_log/event_day=201607${event_day}/event_hour=${event_hour}/event_log_source=${event_log_source}/$filename
	if [ $? -ne 0 ];then
		#echo "hahahhahaha"
		#echo $file
		hadoop fs -cp $file bos://bigdata2/music/compress/music_log/event_day=201607${event_day}/event_hour=${event_hour}/event_log_source=${event_log_source} &
		pids=(${pids[*]} $!)
	fi
	done
done
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
#25,20,nsclick,7301076839,7447072896
#25,21,nsclick,7428244580,7647546802

