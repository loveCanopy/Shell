set -x
#event_day=(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31)
#event_day=(03 13 22 25 27 20 26)
event_day=(20 28 09 10 13 17)
event_hour=(00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23)
#event_log_source=(music_leboweb_log_nginx music_yyr_log_nginx nsclick play_log_nginx yinyueyun_nginx)
event_log_source=(music_yyr_log_nginx music_log_nginx nsclick play_log_nginx yinyueyun_nginx)
for j in ${event_log_source[@]}
do
	for i in ${event_day[@]}
	do
		for k in ${event_hour[@]}
		do
		num=`hadoop fs -ls bos://bigdata2/music/compress/music_log/event_day=201607${i}/event_hour=${k}/event_log_source=${j} | awk '/bos/{print $3,$6}' | awk '{num+=$1} END {print num}'`
		num1=`hadoop fs -ls /music/compress/music_log/event_day=201607${i}/event_hour=${k}/event_log_source=${j} | awk '/music/{print $5,$7}' | awk '{num+=$1} END {print num}'`
		if [ $num -ne $num1 ];then
			echo $i,$k,$j,$num,$num1 >> /home/work/temp/yujie/20161222_1/result7_check.txt
		fi
		done
	done
done
