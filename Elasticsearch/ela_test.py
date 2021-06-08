# Elasticsearch 기본 폼
from elasticsearhch import Elasticsearch

# host, port 설정
es_host = '127.0.0.1'
es_port = 9200

'''
client 생성 >> host 정보 입력
data 검색 >> search() method arguemnt 에 index 이름, query 내용 입력
print 결과 >> query 정보 출력
'''
if __name__ == '__main__':
  client = Elasticsearch(
    hosts = [{host : es_host, port : es_port}]
  )
  index_name = 'idx_name'
  print(client.search(
    index = index_name,
    body = {
      "query" : {
        "match_all" : {}
      }
    }
  ))
