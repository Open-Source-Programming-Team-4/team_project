#!/usr/bin/python3

from elasticsearch import Elasticsearch
import pprint
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__=='__main__':
	import crawling as crawling
	import crawling_de as crawling_de
	import crawling_think as crawling_think
else:
	import mod_pkg.crawling as crawling
	import mod_pkg.crawling_de as crawling_de
	import mod_pkg.crawling_think as crawling_think

'''
*** elastic search module ***

$ cd elasticsearch-7.6.2
$ ./bin/elasticsearch

*****************************

beautifulsoup4 version : 4.6.0
install sklearn

'''

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
	"ddaying" : [],   	( 진행상황 )
	"url" : []			( 링크 )
}
'''

# 크롤링 데이터 가져오기
detizen_data = crawling_de.crawling_detizen(50)
think_data = crawling_think.Crawling_think()
wevity_data = crawling.Crawling_wevity(20)

# 데이터 저장
def data_store(idx):
	for i in range(len(detizen_data["site"])):
		input_data = {
			"site" : detizen_data["site"][i],
			"title" : detizen_data["title"][i],
			"field" : detizen_data["field"][i],
			"host" : detizen_data["host"][i],
			"Dday" : detizen_data["Dday"][i],
			"ddaying" : detizen_data["ddaying"][i],
			"url" : detizen_data["url"][i]
		}
		res = es.index(index=idx, doc_type="_doc", id=i, body=input_data)

def data_store2(idx):
	for i in range(len(think_data['site'])):
		input_data = {
			'site': think_data['site'][i],
			'title': think_data['title'][i],
			'field': think_data['field'][i],
			'host': think_data['host'][i],
			'Dday': think_data['Dday'][i],
			'ddaying': think_data['ddaying'][i],
			'url': think_data['url'][i]
		}
		res = es.index(index=idx, doc_type="_doc", id=i+len(detizen_data['site']), body=input_data)

def data_store3(idx):
	for i in range(len(wevity_data['site'])):
		input_data = {
			'site': wevity_data['site'][i],
			'title': wevity_data['title'][i],
			'field': wevity_data['field'][i],
			'host' : wevity_data['host'][i],
			'Dday' : wevity_data['Dday'][i],
			'ddaying' : wevity_data['ddaying'][i],
			'url' : wevity_data['url'][i]
		}
		res = es.index(index=idx, doc_type="_doc", id=i+len(detizen_data['site'])+len(think_data['site']), body=input_data)

# 코사인 유사도 분석 tfidf & cosine similarity
def cal_CoSim(input_str, search_str):
	sent = (input_str, search_str)
	tfidf_vectorizer = TfidfVectorizer()
	tfidf_matrix = tfidf_vectorizer.fit_transform(sent)

	cs = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

	return cs

# 저장 된 전체 데이터 검색
def data_search_all(idx):
	data = {"match_all": {}}
	query = {"query": data}
	res = es.search(index=idx, body=query, size=10000)
        
        max_res = 5
        output = {'site': [], 'title': [], 'field': [],
                'host': [], 'Dday': [], 'ddaying': [], 'url': []}
        for i in range(max_res):
            output['site'].append(tmp['site'][i])
            output['title'].append(tmp['title'][i])
            output['field'].append(tmp['field'][i])
            output['host'].append(tmp['host'][i])
            output['Dday'].append(tmp['Dday'][i])
            output['ddaying'].append(tmp['ddaying'][i])
            output['url'].append(tmp['url'][i])
        
        pprint.pprint(output)
	return output

# 검색 기능 - case 변수에 "title" / "field" / "host" 지정
def data_search(case, idx, input_str):
	data = {"match": {case: input_str}}
	query = {"query": data}
	res = es.search(index=idx, body=query, size=10000)
	max_res = 5
	if max_res < res['hits']['total']['value']:
		max_res = 5
	if max_res > res['hits']['total']['value']:
		max_res = res['hits']['total']['value']
	tmp = {'site': [], 'title': [], 'field': [],
		'host': [], 'Dday': [], 'ddaying': [], 'url': []}
	output = {'site': [], 'title': [], 'field': [],
		'host': [], 'Dday': [], 'ddaying': [], 'url': []}
	if res['hits']['total']['value']>0:
		for hit in res['hits']['hits']:
			tmp['site'].append(hit['_source']['site'])
			tmp['title'].append(hit['_source']['title'])
			tmp['field'].append(hit['_source']['field'])
			tmp['host'].append(hit['_source']['host'])
			tmp['Dday'].append(hit['_source']['Dday'])
			tmp['ddaying'].append(hit['_source']['ddaying'])
			tmp['url'].append(hit['_source']['url'])
		
		for i in range(max_res):
			output['site'].append(tmp['site'][i])
			output['title'].append(tmp['title'][i])
			output['field'].append(tmp['field'][i])
			output['host'].append(tmp['host'][i])
			output['Dday'].append(tmp['Dday'][i])
			output['ddaying'].append(tmp['ddaying'][i])
			output['url'].append(tmp['url'][i])
	
	pprint.pprint(output)
	return output

# 통합 검색기능 - 테스트 필요
def data_search_allField(idx,search_word): 
	res = es.search(index = idx,size=10000, body={"query": {"multi_match": {"query": search_word}}})
	max_res = 5
	if max_res < res['hits']['total']['value']:
		max_res = 5
	if max_res > res['hits']['total']['value']:
		max_res = res['hits']['total']['value']
	tmp = {'site': [], 'title': [], 'field': [],
		'host': [], 'Dday': [], 'ddaying': [], 'url': [],
		'score': []}
	output = {'site': [], 'title': [], 'field': [],
		'host': [], 'Dday': [], 'ddaying': [], 'url': []}
	if res['hits']['total']['value']>0:
		for hit in res['hits']['hits']:
			tmp['site'].append(hit['_source']['site'])
			tmp['title'].append(hit['_source']['title'])
			tmp['field'].append(hit['_source']['field'])
			tmp['host'].append(hit['_source']['host'])
			tmp['Dday'].append(hit['_source']['Dday'])
			tmp['ddaying'].append(hit['_source']['ddaying'])
			tmp['url'].append(hit['_source']['url'])
			tmp['score'].append(cal_CoSim(search_word, hit['_source']['title']))
			tmp['score'].append(cal_CoSim(search_word, hit['_source']['field']))
			tmp['score'].append(cal_CoSim(search_word, hit['_source']['host']))

		tmp_list = []
		for i in range(len(tmp['site'])):
			tmp_list.append({'site': tmp['site'][i], 'title': tmp['title'][i],
					'field': tmp['field'][i], 'host': tmp['host'][i],
					'Dday': tmp['Dday'][i], 'ddaying': tmp['ddaying'][i],
					'url': tmp['url'][i], 'score': tmp['score'][i]})
		tmp_list = sorted(tmp_list, key=itemgetter('score'), reverse=True)

		for i in range(len(tmp['site'])):
			tmp['site'][i] = tmp_list[i]['site']
			tmp['title'][i] = tmp_list[i]['title']
			tmp['field'][i] = tmp_list[i]['field']
			tmp['host'][i] = tmp_list[i]['host']
			tmp['Dday'][i] = tmp_list[i]['Dday']
			tmp['ddaying'][i] = tmp_list[i]['ddaying']
			tmp['url'][i] = tmp_list[i]['url']
			tmp['score'][i] = tmp_list[i]['score']
	
		for i in range(max_res):
			output['site'].append(tmp['site'][i])
			output['title'].append(tmp['title'][i])
			output['field'].append(tmp['field'][i])
			output['host'].append(tmp['host'][i])
			output['Dday'].append(tmp['Dday'][i])
			output['ddaying'].append(tmp['ddaying'][i])
			output['url'].append(tmp['url'][i])

	pprint.pprint(output)
	return output
	

# Cosine Similarity
# 검색 기능 - case 변수에 "title" / "field" / "host" 지정
def data_search_cs(case, idx, input_str):
	data = {"match": {case: input_str}}
	query = {"query": data}
	res = es.search(index=idx, body=query, size=10000)
	max_res = 5
	if max_res < res['hits']['total']['value']:
		max_res = 5
	if max_res > res['hits']['total']['value']:
		max_res = res['hits']['total']['value']
	tmp = {'site': [], 'title': [], 'field': [],
		'host': [], 'Dday': [], 'ddaying': [], 'url': [],
		'score': []}
	output = {'site': [], 'title': [], 'field': [],
		'host': [], 'Dday': [], 'ddaying': [], 'url': []}
	if res['hits']['total']['value']>0:
		for hit in res['hits']['hits']:
			tmp['site'].append(hit['_source']['site'])
			tmp['title'].append(hit['_source']['title'])
			tmp['field'].append(hit['_source']['field'])
			tmp['host'].append(hit['_source']['host'])
			tmp['Dday'].append(hit['_source']['Dday'])
			tmp['ddaying'].append(hit['_source']['ddaying'])
			tmp['url'].append(hit['_source']['url'])
			tmp['score'].append(cal_CoSim(input_str, hit['_source'][case]))

		tmp_list = []
		for i in range(len(tmp['site'])):
			tmp_list.append({'site': tmp['site'][i], 'title': tmp['title'][i],
					'field': tmp['field'][i], 'host': tmp['host'][i],
					'Dday': tmp['Dday'][i], 'ddaying': tmp['ddaying'][i],
					'url': tmp['url'][i], 'score': tmp['score'][i]})
		tmp_list = sorted(tmp_list, key=itemgetter('score'), reverse=True)

		for i in range(len(tmp['site'])):
			tmp['site'][i] = tmp_list[i]['site']
			tmp['title'][i] = tmp_list[i]['title']
			tmp['field'][i] = tmp_list[i]['field']
			tmp['host'][i] = tmp_list[i]['host']
			tmp['Dday'][i] = tmp_list[i]['Dday']
			tmp['ddaying'][i] = tmp_list[i]['ddaying']
			tmp['url'][i] = tmp_list[i]['url']
			tmp['score'][i] = tmp_list[i]['score']
	
		for i in range(max_res):
			output['site'].append(tmp['site'][i])
			output['title'].append(tmp['title'][i])
			output['field'].append(tmp['field'][i])
			output['host'].append(tmp['host'][i])
			output['Dday'].append(tmp['Dday'][i])
			output['ddaying'].append(tmp['ddaying'][i])
			output['url'].append(tmp['url'][i])

	pprint.pprint(output)
	return output

# 데이터 저장 함수
def ela_store():
    idx = "data_idx"
    es.indices.delete(index=idx, ignore=[400, 404])

    data_store(idx)
    data_store2(idx)
    data_store3(idx)

''' 데이터 저장 & 검색 테스트 '''
if __name__ == "__main__":
	# index 설정
	idx = "data_idx"
	# "title" / "field" / "host" 검색 설정
	case = "title"
	
	es.indices.delete(index=idx, ignore=[400, 404])

	# 대티즌 데이터 저장
	data_store(idx)

	# 씽굿 데이터 저장
	data_store2(idx)

	# 위비티 데이터 저장
	data_store3(idx)

	# 데이터 전체 검색
#	print("전체 검색 결과")
#	data_search_all(idx)
	# 검색 기능 테스트
#	print("검색 결과")
	data_search(case, idx, "대구")
	# 코사인 유사도 적용 검색 기능 테스트
	print("코사인 유사도 적용 검색 결과")
	data_search_cs(case, idx, "사자")
