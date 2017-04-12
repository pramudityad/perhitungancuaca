#!/bin/bash

#cari semua PID
pid=`ps aux | grep 'main.py' | awk '{print $2}'`

#jika PID tidak ditemukan maka print empty, jika isi maka di kill
if [ -z $pid ]
then
	echo "empty"
else
	sudo kill -9 $pid
	printf '%s\tStop Application\n' "$(date +'%T %A %d %B %Y')" >>restartlog
fi

#start semua program
printf '%s\tStart Application\n' "$(date +'%T %A %d %B %Y')" >>restartlog
python /home/TA/perhitungancuaca/apps/main.py

