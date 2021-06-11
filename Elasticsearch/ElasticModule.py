#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
모듈 사용시 my_pkg 폴더안에 __init__.py와 함께 넣어서 사용
메인 코드에서 import my_pkg.ElasticModule 으로 임포트 해주고 
my_pkg.ElasticModule.delData("test","words",1) 와같이 함수를 사용할 수 있습니다

검색기능이 구현되었습니다. 딕셔너리의 6개의 모든 키값에서 일치하는 단어가 있는지 검색합니다.
해당 검색어를(단어) 포함하는 인덱스의 데이터를 딕셔너리 형태로 반환합니다
딕셔너리 형태는 장영우분께서 크롤링하실 때만든 result를 참고했습니다

기본적인 사용 메커니즘 
0. 엘라스틱 서치를 실행한다
1. 크롤링을 해서 data(딕셔너리)를 얻는다. 
2. data를 dataInsert함수를 사용해서 엘라스틱 서치에 삽입한다.
3. 검색함수를 사용해서 결과값을 얻는다(1.의 data와 똑같은 형태로 반환되나 
코사인 유사도 분석의 경우는 결과값 확인을위해 cosSimScore라는 키값이 추가된 형태로 반환된다)

반환되는 데이터 형태 
data = { "site" : [], "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : []}
data(코사인 유사도 분석시) = { "site" : [], "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [],"cosSimScore" : []}

-----------------------------까먹으신 분들을 위한 엘라스틱 서치 사용법-----------------------------
엘라스틱 서치 실행 방법
cd elasticsearch-7.6.2
./bin/elasticsearch

기본 쿼리문
curl 'localhost:9200/test/_search?size=500&pretty' => 엘라스틱 서치내의 모든 데이터 출력
------------------------------------------------------------------------------------------------
'''
from elasticsearch import Elasticsearch

from konlpy.tag import Okt 
from numpy import dot 
from numpy.linalg import norm 
import numpy as np 
from operator import itemgetter

#----------------------------------------------------코사인 유사도 분석 부분----------------------------------------------------
# 코사인 유사도를 구하는 함수 
def cos_sim(a, b): 
	return dot(a, b)/(norm(a)*norm(b)) 

# 기준이 되는 키워드와 벡터 키워드 리스트를 받아서 키워드별 빈도를 구하는 함수 
def make_matrix(feats, list_data): 
	freq_list = [] 
	for feat in feats: 
		freq = 0 
		for word in list_data: 
			if feat == word: 
				freq += 1 
		freq_list.append(freq) 
	return freq_list

def scoreCoSim(searchWord,objectWord):
	okt = Okt() 
	v1 = okt.nouns(searchWord) 
	v2 = okt.nouns(objectWord) 
	# 단어들을 중복제거를 위해, set에 데이터를 쌓는다 
	v3 = v1 + v2 
	feats = set(v3) 
	v1_arr = np.array(make_matrix(feats, v1)) 
	v2_arr = np.array(make_matrix(feats, v2)) 

	cs1 = cos_sim(v1_arr, v2_arr) 
	return cs1

#----------------------------------------------------------------------------------------------------------------------------

es_host="127.0.0.1"
es_port="9200"
es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)


#첫번째 인자로 받은 딕셔너리 데이터(data)를 엘라스틱 서치에 저장하는 함수 
#인덱스별로 각각의 딕셔너리 생성, 검색기능을 위해서
#2인자 엘라스틱 서치의 인덱스, 3인자 도큐먼트 타입

def dataInsert(data, idx, docType): 
	for i in range(0,len(data["title"])):
		tempDic = { "site" : data["site"][i], "title" : data["title"][i] , "field" : data["field"][i] , "host" : data["host"][i] , "Dday": data["Dday"][i] , "dday-ing": data["dday-ing"][i] ,"url": data["url"][i]}
		res = es.index(index=idx, doc_type=docType,id=i, body=tempDic)
		print(res)

#1인자 인덱스, 2인자 도큐먼트 타입 3인자 검색어 
#검색어를 입력해서 나오는 결과들을 딕셔너리 타입으로 반환해주는 함수
#결과를 스코어링해서 내림차순 정렬함 TF,ID, 점수는 Filed Length 값을 조합한 식으로 도출

def searchData(idx, docType,search_word): 
	res ={ "site" : [], "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [] }

	resp = es.search(index = idx, doc_type = docType,size=1000, body={"query": {"multi_match": {"query": search_word}}})

	for doc in resp['hits']['hits']:
		res['site'].append(doc['_source']['site'])	
		res['title'].append(doc['_source']['title'])
		res['field'].append(doc['_source']['field'])
		res['host'].append(doc['_source']['host'])
		res['Dday'].append(doc['_source']['Dday'])
		res['dday-ing'].append(doc['_source']['dday-ing'])
		res['url'].append(doc['_source']['url'])
	return res

		

#1인자 인덱스, 2인자 도큐먼트 타입 
#해당 인덱스의 데이터를 추출해서 딕셔너리 타입으로 반환해주는 함수
#딕셔너리의 키값은 장영우분이 크롤링 코드에서 만드신 딕셔너리의 키값을 사용했습니다
#dic{site, title, field, host, Dday, dday-ing, url}

def extractData(idx,docType):
	res ={ "site" : [], "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : []}

	resp = es.search(index = idx, doc_type = docType, size=1000)
	for doc in resp['hits']['hits']:
		res['site'].append(doc['_source']['site'])
		res['title'].append(doc['_source']['title'])
		res['field'].append(doc['_source']['field'])
		res['host'].append(doc['_source']['host'])
		res['Dday'].append(doc['_source']['Dday'])
		res['dday-ing'].append(doc['_source']['dday-ing'])
		res['url'].append(doc['_source']['url'])
	return res

#1인자 인덱스, 2인자 도큐먼트타입, 3인자 검색어, 4인자 반환데이터 최대길이
#코사인 유사도 분석을 통해서 유사도가 높은순으로 내림차순 결과값을 출력하는 함수
#검색어(searchWord)와 공모전의 제목(title) 사이의 유사도 분석을 합니다

#사용예시 : data = my_pkg.ElasticModule.cosSimSearch("test","words","홍보 콘텐츠 영상 캐릭터 공모전", 15)
# data에 검색어에 대한 유사도점수를 매겨 상위 15개 결과를 반환한다.(test인덱스의 words도큐먼트내의 데이터에서 검색을 수행)
def cosSimSearch(idx,docType,searchWord, maxLen):

	#res 초기데이터 쿼리용 , res2 정렬용 딕셔너리 리스트, res3 최종반환용 딕셔너리(res에서 최대 길이조절)
	res ={ "site" : [], "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [],"cosSimScore" : []}
	res3 ={ "site" : [], "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [],"cosSimScore" : []}
	res2 = []
	resp = es.search(index = idx, doc_type = docType, size=1000)
	for doc in resp['hits']['hits']:
		res['site'].append(doc['_source']['site'])
		res['title'].append(doc['_source']['title'])
		res['field'].append(doc['_source']['field'])
		res['host'].append(doc['_source']['host'])
		res['Dday'].append(doc['_source']['Dday'])
		res['dday-ing'].append(doc['_source']['dday-ing'])
		res['url'].append(doc['_source']['url'])
		
		res['cosSimScore'].append( scoreCoSim(searchWord,doc['_source']['title']) )
	
	
					
	for i in range(len(res["title"])) : #정렬을 위해서 딕셔너리 리스트 잠시 변환
		res2.append({ "site" : res["site"][i], "title" : res["title"][i] , "field" : res["field"][i] , "host" : res["host"][i] , "Dday" : res["Dday"][i] , "dday-ing" : res["dday-ing"][i] ,"url" : res["url"][i],"cosSimScore" : res["cosSimScore"][i]})

	res2 = sorted(res2, key=itemgetter('cosSimScore'), reverse=True) #딕셔너리 정렬 
	for i in range(len(res["title"])) : #딕셔너리 반환에 알맞은 형태로 다시 변환
		res["site"][i] = res2[i]["site"]
		res["title"][i] = res2[i]["title"]
		res["field"][i] = res2[i]["field"]
		res["host"][i] = res2[i]["host"]
		res["Dday"][i] = res2[i]["Dday"]
		res["dday-ing"][i] = res2[i]["dday-ing"]
		res["url"][i] = res2[i]["url"]
		res["cosSimScore"][i] = res2[i]["cosSimScore"]
		

	if maxLen>len(res["title"]): #인자로 넣어준 최대길이가 딕셔너리 전체의 길이보다 길다면 이를 제한함
		maxLen=len(res["title"])

	#del(res["cosSimScore"]) 결과에서 cosSimScore키를 제거하고싶다면 주석해제
	
	'''#디버그용 코드
	for i in range(maxLen) :
		print(res["site"][i])
		print(res["title"][i])
		print(res["field"][i])
		print(res["host"][i])
		print(res["Dday"][i])
		print(res["dday-ing"][i])
		print(res["url"][i])
		print(res["cosSimScore"][i])
		print("----------------------------------------")
	print(str(maxLen)+"개의 공모전 정보를 탐색했습니다.")
	'''
	for i in range(maxLen) : #결과값에 최대길이을 적용
		res3['site'].append(res["site"][i])
		res3['title'].append(res["title"][i])
		res3['field'].append(res["field"][i])
		res3['host'].append(res["host"][i])
		res3['Dday'].append(res["Dday"][i])
		res3['dday-ing'].append(res["dday-ing"][i])
		res3['url'].append(res["url"][i])
		res3['cosSimScore'].append(res["cosSimScore"][i])
	return res3

#1인자 인덱스, 2인자 도큐먼트 타입, 3인자 ID 번호 / 특정 데이터를 삭제하는 함수
def delData(idx,docType,idNum):
	res=es.delete(index=idx, doc_type=docType, id=idNum)
	print(res)

#1인자 인덱스 / 해당인덱스의 모든 데이터를 삭제하는 함수
def delAllData(idx):
	res=es.indices.delete(index=idx, ignore=[400, 404])
	print(res)
		


		

	


