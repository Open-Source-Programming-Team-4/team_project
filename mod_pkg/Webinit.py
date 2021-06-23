  
#!/usr/bin/python3
from flask import render_template

def search(searchobject, case):
  idx = "data_idx"
  if case=="all":
    dt=  data_search_allField(idx,searchobject)
  else:        # "title" / "field" / "host" 검색 설정
    dt = data_search_cs(case, idx, searchobject)
  
  return render_template("main.html",rest=dt)
if __name__=='__main__':
    keyword = input()
    res =  search(keyword)
    print(res['Dday'])
    from ela_search import *
else:
    from mod_pkg.ela_search import *
