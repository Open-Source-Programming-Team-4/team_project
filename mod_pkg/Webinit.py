  
#!/usr/bin/python3


def search(searchobject, case):
  idx = "data_idx"
        # "title" / "field" / "host" 검색 설정
  dt = data_search_cs("title", idx, searchobject)
  
  return dt
if __name__=='__main__':
    keyword = input()
    res =  search(keyword)
    print(res['Dday'])
    from ela_search import *
else:
    from mod_pkg.ela_search import *
