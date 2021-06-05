#!/usr/bin/python3
#-*- coding: utf-8 -*-


###해야할것  ->  크롤링한 url을 사이트 뒤에 붙여야함, 제일 마지막 페이지 뽑아서 그 페이지까지 크롤링하는것.
##### 분야별에서 전체로 크롤링 10개씩 나옴.
###### 최대페이지를 찾아서 페이지 하나씩 넘겨가면서 10개씩 크롤링해서 저장하면 될듯
 

#result(dict)의 각 0번들 
#2021 그린스마트 미래학교「가상설계 및 콘텐츠」공모전
#['', '논문/리포트', '기획/아이디어', '디자인', 'UCC/영상', '문학/수기', '건축/건설', '']
#교육부, 전국 17개 시ㆍ도교육청
#D-2
#접수예정
#/Contest/ContestDetail.html?id=31018


import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

#이부분 의미없는듯 그냥 전체 다 들고올거면 https://www.thinkcontest.com/Contest/ContestDetail.html?id=31076
#이런식으로 뒤에 /ContestDetail.html?id=숫자  붙이면 됨.

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
result = { "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [] }

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
  for sp_list in title:
    result["title"].append(sp_list.text)
   # print(sp_list.text)

#분야 
def field_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  #field = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-cate > span")
  field = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-cate")
  #main > div > div.body.contest-cate > div > table > tbody > tr:nth-child(1) > td.txt-left > div.contest-cate > span:nth-child(6)
  #main > div > div.body.contest-cate > div > table > tbody > tr:nth-child(1) > td.txt-left > div.contest-cate
  #print(type(field))
  #print(field)
  for list in field:
    list_text=list.text
   # print(type(list_text))
    split_list=list_text.split('\n')
    result["field"].append(split_list)
    #a=split_list.split('\n')
    #print(a)
   # print(type(split_list))
   # print(list.text)

 #print()

#주최사
def host_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  host = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(2)")
  for list in host:
    #print(list.text)
    result["host"].append(list.text)
    
  ## nth-of-type 써야함..

#디데이
def Dday_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  dday = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(3) > p")
  for list in dday:
    result["Dday"].append(list.text)
    #print(list.text)

#진행사항
def dday_ing_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  mode = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(3) > span > span")
  for list in mode:
    result["dday-ing"].append(list.text)
    #print(list.text)



def url_think(url):
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  URL = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-title.special > a")
  for list in URL:
    result["url"].append(list["href"])
    #print(list["href"])
  


def Crawling_think(url):
  title_think(url)
  field_think(url)
  host_think(url)
  Dday_think(url)
  dday_ing_think(url)
  url_think(url)



if __name__ == '__main__':
  url = u'https://www.thinkcontest.com/Contest/CateField.html'
  
  #FindMaxPage_think(url)
  Crawling_think(url)
  for i in range(len(result["title"])):
    print(result["title"][i])
    print(result["field"][i])
    print(result["host"][i])
    print(result["Dday"][i])
    print(result["dday-ing"][i])
    print(result["url"][i])
