#!/usr/bin/python3

from elasticsearch import Elasticsearch
import pprint
import numpy as np
from numpy.linalg import norm
from numpy import dot
from konlpy.tag import Okt
from operator import itemgetter

'''
*** elastic search module ***

$ cd elasticsearch-7.6.2
$ ./bin/elasticsearch

Note : import crawling module "crawling.py" in current directory
'''


''' 데이터 저장 & 검색 테스트 '''
if __name__ == "__main__":
        import crawling
        import crawling_de
        import crawling_think
        # index 설정
        idx = "data_idx"
        # "title" / "field" / "host" 검색 설정
        case = "title"

        # 대티즌 데이터 저장
        data_store(idx)

        # 씽굿 데이터 저장
        data_store2(idx)

        # 데이터 전체 검색
        print("전체 검색 결과")
        data_search_all(idx)
        # 검색 기능 테스트
        print("검색 결과")
        data_search(case, idx, "제 39회 서울특별시 건축상 작품모집 공고")
        # 코사인 유사도 적용 검색 기능 테스트
        print("코사인 유사도 적용 검색 결과")
        data_search_cs(case, idx, "제 39회 서울특별시 건축상 작품모집 공고")
else:
        import mod_pkg.crawling as crawling
        import mod_pkg.crawling_de as crawling_de
        import mod_pkg.crawling_think as crawling_think


# Elasticsearch 설정
es_host = '127.0.0.1'
es_port = 9200
es = Elasticsearch(hosts = [{"host" : es_host, "port" : es_port}])

'''
data_set = {
	"site" : [],		( 사이트 )
	"title" : [],		( 제목 )
	"field" : [],		( 분야 )
	"host" : [],		( 주최사 )
	"Dday" : [],		( 남은 기간 )
	"dday-ing" : [],	( 진행상황 )
	"url" : []		( 링크 )
}
'''

# wevity 모든 분야 / 접수 중 데이터 전체 가져오기
#wevity_data_ing = crawling.CrawlingByField_wevity(2, "end")

# 대티즌 크롤링 데이터 가져오기
detizen_data = crawling_de.crawling_detizen(10)

# 씽굿 크롤링 데이터 가져오기
think_data = crawling_think.Crawling_think()

def data_store2(idx):
	for i in range(len(think_data['site'])):
		input_data = {
			'site': think_data['site'][i],
			'title': think_data['title'][i],
			'field': think_data['field'][i],
			'host': think_data['host'][i],
			'Dday': think_data['Dday'][i],
			'dday-ing': think_data['dday-ing'][i],
			'url': think_data['url'][i]
		}
		res = es.index(index=idx, doc_type="_doc", id=i+1, body=input_data)
#		print(res)

# 데이터 저장
def data_store(idx):
	for i in range(len(detizen_data["site"])):
		input_data = {
			"site" : detizen_data["site"][i],
			"title" : detizen_data["title"][i],
			"field" : detizen_data["field"][i],
			"host" : detizen_data["host"][i],
			"Dday" : detizen_data["Dday"][i],
			"dday-ing" : detizen_data["dday-ing"][i],
			"url" : detizen_data["url"][i]
		}
		res = es.index(index=idx, doc_type="_doc", id=i+1, body=input_data)
#		print(res)

# 형태소 분석 & Cosine Similarity
def cos_sim(a, b):
	return dot(a, b)/(norm(a)*norm(b))

def make_matrix(feats, list_data):
	freq_list = []
	for feat in feats:
		freq = 0
		for word in list_data:
			if feat == word:
				freq += 1
		freq_list.append(freq)
	return freq_list

def KoNLPy_data(input_str, search_str):
	okt = Okt()
	text1 = okt.nouns(input_str)
	text2 = okt.nouns(search_str)
	
	text3 = text1 + text2
	feats = set(text3)

	text1_arr = np.array(make_matrix(feats, text1))
	text2_arr = np.array(make_matrix(feats, text2))
	
	cs = cos_sim(text1_arr, text2_arr)

#	print(cs)
	return cs

# 저장 된 전체 데이터 검색
def data_search_all(idx):
	data = {"match_all": {}}
	query = {"query": data}
	res = es.search(index=idx, body=query, size=10000)
	print("전체 검색 결과")
	pprint.pprint(res)
#	for hit in res["hits"]["hits"]:
#		print(hit["_source"])
	
	return res

# 검색 기능 - case 변수에 "title" / "field" / "host" 지정
def data_search(case, idx, input_str):
	data = {"match": {case: input_str}}
	query = {"query": data}
	res = es.search(index=idx, body=query, size=10000)
#	print("검색 결과")
#	pprint.pprint(res)

	tmp = {'site': [], 'title': [], 'field': [],
		'host': [], 'Dday': [], 'dday-ing': [], 'url': []}
	for hit in res['hits']['hits']:
		tmp['site'].append(hit['_source']['site'])
		tmp['title'].append(hit['_source']['title'])
		tmp['field'].append(hit['_source']['field'])
		tmp['host'].append(hit['_source']['host'])
		tmp['Dday'].append(hit['_source']['Dday'])
		tmp['dday-ing'].append(hit['_source']['dday-ing'])
		tmp['url'].append(hit['_source']['url'])
	
	# 최대 5개 결과까지 출력
	output = {'site': [], 'title': [], 'field': [],
		'host': [], 'Dday': [], 'dday-ing': [], 'url': []}
	for i in range(5):
		output['site'].append(tmp['site'][i])
		output['title'].append(tmp['title'][i])
		output['field'].append(tmp['field'][i])
		output['host'].append(tmp['host'][i])
		output['Dday'].append(tmp['Dday'][i])
		output['dday-ing'].append(tmp['dday-ing'][i])
		output['url'].append(tmp['url'][i])
	
	pprint.pprint(output)
	return output

# Cosine Similarity
# 검색 기능 - case 변수에 "title" / "field" / "host" 지정
def data_search_cs(case, idx, input_str):
	data = {"match": {case: input_str}}
	query = {"query": data}
	res = es.search(index=idx, body=query, size=10000)
#	print("검색결과")
#	pprint.pprint(res)

	tmp = {'site': [], 'title': [], 'field': [],
		'host': [], 'Dday': [], 'dday-ing': [], 'url': [],
		'score': []}
	for hit in res['hits']['hits']:
		tmp['site'].append(hit['_source']['site'])
		tmp['title'].append(hit['_source']['title'])
		tmp['field'].append(hit['_source']['field'])
		tmp['host'].append(hit['_source']['host'])
		tmp['Dday'].append(hit['_source']['Dday'])
		tmp['dday-ing'].append(hit['_source']['dday-ing'])
		tmp['url'].append(hit['_source']['url'])
		tmp['score'].append(KoNLPy_data(input_str, hit['_source'][case]))

	tmp_list = []
	for i in range(len(tmp['site'])):
		tmp_list.append({'site': tmp['site'][i], 'title': tmp['title'][i],
				'field': tmp['field'][i], 'host': tmp['host'][i],
				'Dday': tmp['Dday'][i], 'dday-ing': tmp['dday-ing'][i],
				'url': tmp['url'][i], 'score': tmp['score'][i]})
	tmp_list = sorted(tmp_list, key=itemgetter('score'), reverse=True)

	for i in range(len(tmp['site'])):
		tmp['site'][i] = tmp_list[i]['site']
		tmp['title'][i] = tmp_list[i]['title']
		tmp['field'][i] = tmp_list[i]['field']
		tmp['host'][i] = tmp_list[i]['host']
		tmp['Dday'][i] = tmp_list[i]['Dday']
		tmp['dday-ing'][i] = tmp_list[i]['dday-ing']
		tmp['url'][i] = tmp_list[i]['url']
		tmp['score'][i] = tmp_list[i]['score']
	
	# 최대 5개 결과까지 출력
	output = {'site': [], 'title': [], 'field': [],
		'host': [], 'Dday': [], 'dday-ing': [], 'url': []}
	for i in range(5):
		output['site'].append(tmp['site'][i])
		output['title'].append(tmp['title'][i])
		output['field'].append(tmp['field'][i])
		output['host'].append(tmp['host'][i])
		output['Dday'].append(tmp['Dday'][i])
		output['dday-ing'].append(tmp['dday-ing'][i])
		output['url'].append(tmp['url'][i])

	pprint.pprint(output)
	return output

''' 데이터 저장 & 검색 테스트 '''
if __name__ == "__main__":
        import crawling
        import crawling_de
        import crawling_think
        # index 설정
        idx = "data_idx"
        # "title" / "field" / "host" 검색 설정
        case = "title"
        
        # 대티즌 데이터 저장
        data_store(idx)

        # 씽굿 데이터 저장
        data_store2(idx)

        # 데이터 전체 검색
        print("전체 검색 결과")
        data_search_all(idx)
        # 검색 기능 테스트
        print("검색 결과")
        data_search(case, idx, "제 39회 서울특별시 건축상 작품모집 공고")
        # 코사인 유사도 적용 검색 기능 테스트
        print("코사인 유사도 적용 검색 결과")
        data_search_cs(case, idx, "제 39회 서울특별시 건축상 작품모집 공고")
else:
        import mod_pkg.crawling
        import mod_pkg.crawling_de
        import mod_pkg.crawling_think
