# 공모전 & 대외활동 사이트 모음


### 구성도
![OSP구성도](https://user-images.githubusercontent.com/79684170/119575711-6b029a00-bdf2-11eb-8212-6e1f12d5cf56.png)


### 기능
prototype function
- [System] - Shell Script
- [Main page] - HTML, Flask
- [Crawler] - Python : Beautifulsoup4 
- [Search] - Python : Elasticsearch

### License
Free Software


깃허브 사용법
=============

#### 1.	Beautifulsoup 4.6.0, Elasticsearch, flask를 설치한다. 
#### 2.	터미널 창에서 새로운 디렉토리를 생성한다.
   >	~$ mkdir new  ( new : 생성할 디렉토리 이름)
#### 3.	생성한 디렉토리로 이동한다
   >	~$ cd new   (new : 생성한 디렉토리 이름)
#### 4.	git clone을 이용하여 복사본을 만든다.
   >	~/new$ git clone https://github.com/Open-Source-Programming-Team-4/team_project.git
#### 5.   생성된 team_project 파일로 이동한다.
   >  ~/new$ cd team_project/
#### 6.   새터미널 창을 열어 Elasticsearch 디렉토리로 이동 후 실행한다.
   > ~$ cd elasticsearch-7.6.2/
   > 
   > ~/elasticsearch-7.6.2$ ./bin/elasticsearch
#### 7.   첫번째 터미널 창으로 돌아와서 app.py를 실행한다.
   > ~/new/team_project$ ./app.py
#### 8.   인터넷 브라우저 창을 키고 주소창에 http://127.0.0.1:5000/을 입력해 접속한다.
