#!/bin/bash

echo "============================="
echo "공모전 대외활동 CompeteONE 설치 화면입니다."
echo "============================="

sudo apt-get install python3 python3-pip default-jdk

pip3 install --upgrage pip

wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.13.2-linux-x86_64.tar.gz"
tar xvzf "elasticsearch-7.13.2-linux-x86_64.tar.gz"
mv elasticsearch-7.13.2 bin
rm elasticsearch-7.13.2-linux-x86_64.tar.gz

chmod +x run_comp.sh
echo "설치가 완료되었으므로 실행하여 주시기 바랍니다. 감사합니다."
