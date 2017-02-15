set -x
event_log_source=(fm_log_nginx music_api_ui_log music_hao123_nginx music_heyinliang_api_nginx_log music_leboweb_log_nginx music_log_nginx music_lua_log music_musicmini_nginx_log music_musicmini_nginx_log music_musicpay_nginx_log music_songfile_nginx_log music_yyr_log_nginx ns_qianqian_ttmsg_udw_new nsclick play_log_nginx yinyueyun_nginx music_api_nginx_log ns_qianqian_ttmsg_udw ns_qianqian_ttpack_udw ns_qianqian_ttmsg_ttpack_new)
event_day=(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31)
#event_day=(20 21 22 23 24 25 26 27 28 29 30)
for i in ${event_log_source[@]}
do
	for k in ${event_day[@]}
	do
	num=`hadoop fs -count -q bos://bigdata2/music/compress/music_log/event_day=201607${k}/event_hour=*/event_log_source=${i}  | awk '{print $5,$6}' | awk '{num+=$2} END {print num}'`
	num1=`hadoop fs -count -q /music/compress/music_log/event_day=201607${k}/event_hour=*/event_log_source=${i} | awk '{print $5,$6}' | awk '{num+=$2} END {print num}'`
	echo $i,$k,$num,$num1  >> /home/work/temp/yujie/20161222_1/result7_count.txt
	done
done
