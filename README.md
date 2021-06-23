# 공모전 & 대외활동 사이트 모음


### 구성도

![OSP구성도](https://user-images.githubusercontent.com/70523625/123081296-c8712180-d458-11eb-9860-bb1e7e8af6b3.png)

### 개요
    기본적인 아이디어와 구상은 다음과 같다. 
    인터넷 상에는 여러개의 공모전사이트가 있고 각 사이트마다 전혀 다른 공모전에 대한 정보가 올라오거나 중복된 정보가 존재할 수 있다. 
    이런 실태에서 각 공모전사이트에 흩어진 공모전 정보를 모으고 특정기준에 따라 분류를 하여 정보를 제공하는것이 기본적인 아이디어이다. 
    정보를 수집 할 공모전 사이트로는 위비티(wevity) , 씽굿(thinkgood) , 데티즌(detizen)으로 총 3개의 공모전에서 정보를 수집하였고, 
    위의 사이트에서 얻은 공모전의 정보들은 다음과 같다. 
    ( 해당 공모전을 게시한 사이트 이름 , 공모전 이름 , 공모전 분야 , 주최사 이름 , Dday 정보 , 공모전 진행상황 , 해당 사이트 주소 ) 
    
    정보를 수집 시 필요한 기술은 크롤링으로 python의 beautifulsoup 모듈을 사용한다.  
    정보를 수집한 뒤 웹페이지를 통해서 이용자에게 정보를 전달한다. 이때 정보는 각 공모전 사이트로 분류되고 공모전의 정보를 타이핑한 키워드를 통하여 검색할 수 있다. 
    크롤링한 정보를 저장할 때에는 elastic search와 python을 연동하여 데이터베이스겸 서버의 역할을 하고 
    이런 서비스를 이용자에게 제공할 공간은 웹페이지로 python의 flask 웹 프레임워크를 이용해 제작한다. 
    이를 통해 이용자가 얻을 수 있는 이익은 여러 사이트에서 공모전을 비교하여 수고를 덜어주고 키워드를 통해 검색이 가능하여 공모전 탐색이 수월해 질 것으로 예상한다.


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
#### 5. team_project 디렉토리로 이동한다.
   >  ~$ cd team_project
#### 6. install.sh 파일의 권한을 변경한다.
   >  ~$ chmod 755 install.sh
#### 6. ./install.sh 파일을 실행한다. (BeautifulSoup 4.6.0을 제외한 필요한 패키지 자동 설치)
   >  ~$ ./install.sh
   >  설치가 정상적으로 이루어지지 않는 경우 Elasticsearch와 flask를 수동 설치한다.
#### 7. BeautifulSoup 4.6.0을 설치한다.
#### 8. ./run_comp.sh파일을 실행한다.
   >  ~$ ./run_comp.sh
   >  권한은 자동으로 변경되어 있습니다.
   >  실행이 되지 않는 경우 flask run 명령어를 이용하거나 ./app.py를 입력하여 주십시오.
#### 9.  인터넷 브라우저 창을 키고 주소창에 http://127.0.0.1:5000/을 입력해 접속한다.

#### ElasticSearch가 자동으로 실행되지 않는 경우

#### 1.  생성된 team_project 파일의 mod_pkg 파일로 이동한다.
   >  ~/new$ cd team_project/mod_pkg/
#### 2.  권한을 변경하고 ela_search.py 실행하고 team_project 파일로 이동한다.
   > ~/new/team_project/mod_pkg$ chmod 755 *.py
   > 
   > ~/new/team_project/mod_pkg$ ./ela_search.py
   > 
   > ~new/team_project/mod_pkg$ cd ..
#### 3.  새터미널 창을 열어 Elasticsearch 디렉토리로 이동 후 실행한다.
   > ~$ cd elasticsearch-7.6.2/
   > 
   > ~/elasticsearch-7.6.2$ ./bin/elasticsearch
#### 4.  첫번째 터미널 창으로 돌아와서 app.py를 실행한다.
   > ~/new/team_project$ ./app.py

