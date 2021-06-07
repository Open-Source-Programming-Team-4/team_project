#!/usr/bin/python3

from elasticsearch import Elasticsearch
import crawling

'''
*** elastic search module ***

$ cd elasticsearch-7.6.2
$ ./bin/elasticsearch

Note : import crawling module "crawling.py" in current directory
'''

# Elasticsearch 설정
es_host = '127.0.0.1'
es_port = 9200
es = Elasticsearch(hosts = [{"host" : es_host, "port" : es_port}])

'''
data_set = {
	"title" : [],
	"field" : [],
	"host" : [],
	"Dday" : [],
	"dday-ing" : [],
	"url" : []
}
'''

# wevity 모든 분야 / 접수 중 데이터 전체 가져오기
wevity_data_ing = crawling.CrawlingByField_wevity(2, "end")

# 데이터 저장
def data_store(idx):
	''' 접수 중 데이터 저장 '''
	for i in range(len(wevity_data_ing["title"])):
		input_data = {
			"title" : wevity_data_ing["title"][i],
			"field" : wevity_data_ing["field"][i],
			"host" : wevity_data_ing["host"][i],
			"Dday" : wevity_data_ing["Dday"][i],
			"dday-ing" : wevity_data_ing["dday-ing"][i],
			"url" : wevity_data_ing["url"][i]
		}
		res = es.index(index=idx, doc_type="_doc", id=i+1, body=input_data)
		print(res)

# 저장 된 전체 데이터 검색
def data_search_all():
	query = {
		"query":{
			"match_all":{}
		}
	}
	res = es.search(index="ing", body=query, size=10000)
	print("전체 검색 결과")
	for hit in res["hits"]["hits"]:
		print(hit["_source"])

# 제목으로 검색
'''
title로 검색을 할 때, input 값과 일치하는 값을 결과로 리턴
현재 input 값과 일치하는 값 뿐만 아니라, input 값의 단어 중 하나만 포함해도 검색 결과가 리턴되는 오류가 있음
'''
def data_search(idx, input_str):
	query = {
		"query":{
			"multi_match":{
				"query":input_str
			}
		}
	}
	res = es.search(index=idx, body=query, size=10000)
	print("검색 결과")
	for hit in res["hits"]["hits"]:
		print(hit["_source"])

''' 데이터 저장 & 검색 테스트 '''
if __name__ == "__main__" :
	idx = "test_idx"

	data_store(idx)
#	data_search_all()
	data_search(idx, "2020 부산국제광고제 청소년 크리에이티브 공모전")
