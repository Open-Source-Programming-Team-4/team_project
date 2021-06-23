#!/bin/bash

if [[ $(uname) == "Linux" ]]; then
	directory=$(dirname $(readlink -f $0))
else
	echo "ERROR"
fi

chmod +x app.py
chmod +x mod_pkg/ela_search.py
exec $directory/bin/bin/elasticsearch & 
elasticpid=$!
exec $directory/mod_pkg/ela_search.py &
initpid=$!
exec python3 $directory/app.py &
pythonpid=$!

echo '공모전/대외활동 한 눈에 보기! Compete ONE입니다.'
echo '------------------------------------------------'

echo 'Loading에 약 3분 30초 정도 소요됩니다. 잠시만 기다려 주십시오.'
echo ''
echo '***********************************************************'
echo '실행이 완료되면 Starting the service with ip_addr=127.0.0.1이 표시됩니다.'

while true; do
    current_time=`date +%H%M%S`
    if [["${current_time}" == '000000']]; then
        exec $directory/mod_pkg/ela_search.py & initpid=$!
    fi
    sleep 1
done
