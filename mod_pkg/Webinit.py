#!/usr/bin/python3


def search(searchobject):
  idx = "data_idx"
        # "title" / "field" / "host" 검색 설정
  case = "title"
  dt = data_search_cs(case, idx, searchobject)
  
  return dt
if __name__=='__main__':
    keyword = input()
    res =  search(keyword)
    print(res['Dday'])
    from ela_search import *
else:
    from mod_pkg.ela_search import *
