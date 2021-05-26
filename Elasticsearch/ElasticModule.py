#!/usr/bin/python
#-*- coding: utf-8 -*-

#모듈 사용시 my_pkg 폴더안에 __init__.py와 함께 넣어서 사용
#메인 코드에서 import my_pkg.ElasticModule 으로 임포트 해주고 
#my_pkg.ElasticModule.delData("test","words",1) 와같이 함수를 사용할 수 있습니다

from elasticsearch import Elasticsearch

es_host="127.0.0.1"
es_port="9200"
es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)


#첫번째 인자로 받은 딕셔너리 데이터(data)를 엘라스틱 서치에 저장하는 함수
#2인자 엘라스틱 서치의 인덱스, 3인자 도큐먼트 타입, 4인자 ID
def dataInsert(data, idx, docType, idNum): 

	res = es.index(index=idx, doc_type=docType,id=idNum, body=data)
	print(res)


#1인자 인덱스, 2인자 도큐먼트 타입 / 해당 데이터를 검색해서 출력하는 함수
def searchData(idx,docType):
        res = es.search(index = idx, doc_type = docType)
        print(res)

#1인자 인덱스, 2인자 도큐먼트 타입 / 해당 데이터를 추출해서 딕셔너리 타입으로 반환해주는 함수 
#딕셔너리의 키값은 장영우분이 크롤링 코드에서 만드신 딕셔너리의 키값을 사용했습니다.(title,field,host) 아직까진 해당 형태의 딕셔너리만이 추출가능합니다.
def extractData(idx,docType):
	res = {}
	result = []
	resp = es.search(index = idx, doc_type = docType)
	for doc in resp['hits']['hits']:
		res['title'] = doc['_source']['title']
		res['field'] = doc['_source']['field']
		res['host'] = doc['_source']['host']
		result.append(res)
	return res

#1인자 인덱스, 2인자 도큐먼트 타입, 3인자 ID 번호 / 해당 데이터를 삭제하는 함수
def delData(idx,docType,idNum):
	res=es.delete(index=idx, doc_type=docType, id=idNum)
	print(res)


		

	


