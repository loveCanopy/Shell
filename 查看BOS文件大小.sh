-- 查看BOS文件大小
hadoop fs -ls bos://bigdata2/music/compress/music_log/event_day=2016050*/event_hour=*/event_log_source=* | awk '/bos/{print $3,$6}' | awk '{num+=$1} END {print num}'

-- 查看hadoop文件大小
hadoop fs -ls /music/compress/music_log/event_day=2016050*/event_hour=*/event_log_source=* | awk '/music/{print $5,$7}' | awk '{num+=$1} END {print num}'

hadoop fs -cp /music/compress/music_log/event_day=20160525/event_hour=21/event_log_source=play_log_nginx  
bos://bigdata2/music/compress/music_log/event_day=20160525/event_hour=21/event_log_source=play_log_nginx


查看文件的列数
awk -F '\t' '{print "columns:" NF}' unreleased_song_udw.txt | head
