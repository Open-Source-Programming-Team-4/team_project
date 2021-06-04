#!/usr/bin/python3
#-*- coding: utf-8 -*-

##### 분야별에서 전체로 크롤링 10개씩 나옴.
###### 최대페이지를 찾아서 페이지 하나씩 넘겨가면서 10개씩 크롤링해서 저장하면 될듯
###### 분야가 여러개 나오는거 아직 해결 못함.
##### 크롤링한 url을 사이트 뒤에 붙여야함. 
##### 아직 list로 안만듬.


import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

#  - 분야별 -
#  전체는 ~CateField.html 임
#  페이지는 +?page=(숫자) 분야는 &c=(숫자)
#  <예시> 기획/아이디어의 3번째 페이지는 https://www.thinkcontest.com/Contest/CateField.html?page=3&c=2

#	논문/리포트 - 1, 기획/아이디어 - 2, 네이밍/슬로건 - 3, 디자인 - 4,
#	광고/마케팅 - 5, 사진 - 6, UCC/영상 - 7, 예체능 - 8, 문학/수기 - 9,
#	캐릭터/만화 - 10, 과학/공학 - 11, 게임/소프트웨어 - 12, 건축/건설 - 13,
#	대외활동 - 14, 취업/창업 - 15, 경품/이벤트 - 16, 전시/페스티발 - 17, 
#	장학(금)재단 - 18, 봉사활동 - 19, 해외 - 20

#  - 접수 정보 (default : 생략은 전체)
#	스폐셜 공모 - sp, 마감임박 - hurry, 접수중 - ing,
#	접수예정 - soon, 마감 - end 
 	
#	print(type(url))
def FindMaxPage_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  maxpage = soup.select("#main > div > div.body.contest-cate > div > div.paging-wrap > div > a")[8]
  print(type(maxpage))
  print(maxpage)     
  # 이렇게하면은 <a class="next" href="CateField.html?page=2653"><i aria-hidden="true" class="fa fa-caret-right"></i><i aria-hidden="true" class="fa fa-caret-right"></i></a>
  #이렇게 나오고 여기서 2653을 추출하면 그게 마지막 페이지 아마?? 2653 을 리턴해줌. 


# 공모전 이름 
def title_think(url):
  # html에  + ?page=1 ~ ?page=2653 까지 원래 url에다가 붙여서 돌리면 해당 페이지의 제목 나옴.
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  title = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-title > a")
  print(type(title))
  print(title)
  for sp_list in title:
    print(sp_list.text)

#분야 
def field_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  field = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-cate > span")
  print(type(field))
  print(field)
  for list in field:
    print(list.text)

#주최사
def host_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  host = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(2)")
  for list in host:
    print(list.text)
  ## nth-of-type 써야함..

#진행사항
def mode_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  mode = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(3) > span > span")
  for list in mode:
    print(list.text)

#디데이
def Dday_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  dday = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(3) > p")
  for list in dday:
    print(list.text)

def url_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  URL = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-title.special > a")
  for list in URL:
    print(list["href"])
  #or list in URL:
  #  print(list.text)
  


def Crawling_think(url):
  #title_think(url)
  #field_think(url)
  #host_think(url)
  #mode_think(url)
  Dday_think(url)
  url_think(url)



if __name__ == '__main__':
  url = u'https://www.thinkcontest.com/Contest/CateField.html'
  
  #FindMaxPage_think(url)
  Crawling_think(url)
