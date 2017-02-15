#! /bin/sh
set -x
if [ x"$3" = x ]; then
	path="ftp://10.208.77.23//home/mp3/udw-log/check/"
else
	path=$3
fi
file=$1.$2."complete"

while true
do
    date=`date +"%Y-%m-%d %H:%M:%S"`
    wget $path$file
    if [[ $? -eq 0 ]]
    then
        exit 0
    else
	echo [$date]": 文件不存在，5min后重试"
        sleep 300
    fi
done
