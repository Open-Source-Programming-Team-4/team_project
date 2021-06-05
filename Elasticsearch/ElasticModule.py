#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
모듈 사용시 my_pkg 폴더안에 __init__.py와 함께 넣어서 사용
메인 코드에서 import my_pkg.ElasticModule 으로 임포트 해주고 
my_pkg.ElasticModule.delData("test","words",1) 와같이 함수를 사용할 수 있습니다

검색기능이 구현되었습니다. 딕셔너리의 6개의 모든 키값에서 일치하는 단어가 있는지 검색합니다.
해당 검색어를(단어) 포함하는 인덱스의 데이터를 딕셔너리 형태로 반환합니다
딕셔너리 형태는 장영우분께서 크롤링하실 때만든 result와 같습니다

검색기능구현을 위해 데이터 저장방식이 변경되었습니다  
이제 딕셔너리의 각각의 인덱스가 별개의 id를 가진 데이터로 들어갑니다

기본적인 사용 메커니즘
0. 엘라스틱 서치를 실행한다
1. 크롤링을 해서 data(딕셔너리)를 얻는다. 
2. data를 dataInsert함수를 사용해서 엘라스틱 서치에 삽입한다.
3. 검색함수를 사용해서 결과값을 얻는다(1.의 data와 똑같은 형태로 반환됨)
data ={ "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [] }


-----------------------------까먹으신 분들을 위한 엘라스틱 서치 사용법-----------------------------
엘라스틱 서치 실행 방법
cd elasticsearch-7.6.2
./bin/elasticsearch

기본 쿼리문
curl 'localhost:9200/test/_search?size=500&pretty' => 엘라스틱 서치내의 모든 데이터 출력
------------------------------------------------------------------------------------------------
'''


from elasticsearch import Elasticsearch

es_host="127.0.0.1"
es_port="9200"
es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)


#첫번째 인자로 받은 딕셔너리 데이터(data)를 엘라스틱 서치에 저장하는 함수 
#인덱스별로 각각의 딕셔너리 생성, 검색기능을 위해서
#2인자 엘라스틱 서치의 인덱스, 3인자 도큐먼트 타입
def dataInsert(data, idx, docType): 
	for i in range(0,len(data["title"])):
		tempDic = { "title" : data["title"][i] , "field" : data["field"][i] , "host" : data["host"][i] , "Dday": data["Dday"][i] , "dday-ing": data["dday-ing"][i] ,"url": data["url"][i]}
		res = es.index(index=idx, doc_type=docType,id=i, body=tempDic)
		print(res)

#1인자 인덱스, 2인자 도큐먼트 타입 3인자 검색어 
#검색어를 입력해서 나오는 결과들을 딕셔너리 타입으로 반환해주는 함수
def searchData(idx, docType,search_word):
	res ={ "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [] }
	resp = es.search(index = idx, doc_type = docType,size=1000, body={"query": {"multi_match": {"query": search_word}}})

	for doc in resp['hits']['hits']:
		res['title'].append(doc['_source']['title'])
		res['field'].append(doc['_source']['field'])
		res['host'].append(doc['_source']['host'])
		res['Dday'].append(doc['_source']['Dday'])
		res['dday-ing'].append(doc['_source']['dday-ing'])
		res['url'].append(doc['_source']['url'])
	return res

		
#1인자 인덱스, 2인자 도큐먼트 타입 
#해당 인덱스의 데이터를 추출해서 딕셔너리 타입으로 반환해주는 함수 => 저장된데이터 전체출력기능
#딕셔너리의 키값은 장영우분이 크롤링 코드에서 만드신 딕셔너리의 키값을 사용했습니다
#dic{title, field, host, Dday, dday-ing, url}
def extractData(idx,docType):
	res ={ "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [] }

	resp = es.search(index = idx, doc_type = docType, size=1000)
	for doc in resp['hits']['hits']:
		res['title'].append(doc['_source']['title'])
		res['field'].append(doc['_source']['field'])
		res['host'].append(doc['_source']['host'])
		res['Dday'].append(doc['_source']['Dday'])
		res['dday-ing'].append(doc['_source']['dday-ing'])
		res['url'].append(doc['_source']['url'])
	return res

#1인자 인덱스, 2인자 도큐먼트 타입, 3인자 ID 번호 / 특정 데이터를 삭제하는 함수
def delData(idx,docType,idNum):
	res=es.delete(index=idx, doc_type=docType, id=idNum)
	print(res)

#1인자 인덱스 / 해당인덱스의 모든 데이터를 삭제하는 함수
def delAllData(idx):
	res=es.indices.delete(index=idx, ignore=[400, 404])
	print(res)
		


		

	


