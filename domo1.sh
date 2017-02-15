event_hour=(00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23)
#event_hour=(21 22 23)
#for i in ${event_hour[@]}
#event_year=(2016 2017)
event_year=(2016)
#event_day=(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31)
event_day=(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31)
#event_month=(01 02 03 04 05 06 07 08 09 10 11 12)
event_month=(05)
#event_log_source=(play_log_nginx)
event_log_source=(fm_log_nginx music_api_ui_log music_hao123_nginx music_heyinliang_api_nginx_log music_leboweb_log_nginx music_log_nginx music_lua_log music_musicmini_nginx_log music_musicmini_nginx_log music_musicpay_nginx_log music_songfile_nginx_log music_yyr_log_nginx ns_qianqian_ttmsg_udw_new nsclick play_log_nginx yinyueyun_nginx)
for i in ${event_year[@]}
do
	for j in ${event_month[@]}
	do
		for k in ${event_day[@]}
		do
			if [ $k -eq 31 ] && [ $j -eq 02 -o $j -eq 04 -o $j -eq 06 -o $j -eq 09 -o $j -eq 11 ];then
				continue
			fi
			for l in ${event_hour[@]}
			do
				for w in ${event_log_source[@]}
				do
					./test1.sh $i $j $k $l $w
					#echo $j $k $l $w
					sleep 1
				done 
			done


 
		done
	done
done

