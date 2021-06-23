#!/bin/bash

echo "============================="
echo "공모전 대외활동 CompeteONE 설치 화면입니다."
echo "BeautifulSoup는 버전 문제가 발생할 수 있으니 4.6.0 버전 수동 설치를 권장합니다."
echo "============================="

sudo apt-get install python3 python3-pip default-jdk

pip3 install --upgrade pip
pip3 install flask
pip3 install -U scikit-learn

wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.13.2-linux-x86_64.tar.gz"
tar xvzf "elasticsearch-7.13.2-linux-x86_64.tar.gz"
mv elasticsearch-7.13.2 bin
rm elasticsearch-7.13.2-linux-x86_64.tar.gz

chmod +x run_comp.sh
echo "설치가 완료되었으므로 실행하여 주시기 바랍니다. 감사합니다."
