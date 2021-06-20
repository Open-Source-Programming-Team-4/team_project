#!/usr/bin/python3
from ela_search import *


def search(searchobject):
  idx = "data_idx"
        # "title" / "field" / "host" 검색 설정
  case = "title"
  dt = data_search_cs(case, idx, searchobject)
  return dt
if __name__=='__main__':
    dt = input()
    search(dt)
