#!/usr/bin/python3
#-*- coding: utf-8 -*-

'''
result(dict)의 각 0번들 
씽굿
2021 그린스마트 미래학교「가상설계 및 콘텐츠」공모전
['논문/리포트', '기획/아이디어', '디자인', 'UCC/영상', '문학/수기', '건축/건설']
교육부, 전국 17개 시ㆍ도교육청
D-2
접수예정
https://www.thinkcontest.com/Contest/ContestDetail.html?id=31018
'''

import re
import requests
from bs4 import BeautifulSoup

# https://www.thinkcontest.com/Contest/ContestDetail.html?id=31076
#id뒤의 숫자가 각 공모전의 번호


result_think = { "site" : [] , "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [] }

def Crawling_think():
 for num in range(1,161):
  num = str(num)
  url='https://www.thinkcontest.com/Contest/CateField.html?page=' + num
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  for n in range(10):
   result_think["site"].append("씽굿") 

#공모명  
  title = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-title > a")
  for sp_list in title:
   result_think["title"].append(sp_list.text)

#분야
  field = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-cate")
  for b in field:
   list_text=b.text
   split_list=list_text.split()
   sp=','.join(split_list)
   result_think["field"].append(sp)

#주최
  host = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(2)")
  for c in host:
   result_think["host"].append(c.text)

#진행사항
  dday = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(3)")
  for d in dday:
   d_list = d.text
   d_split=d_list.split()
   if (d_split[0]=="마감"):
    result_think["dday-ing"].append(d_split[0])
    result_think["Dday"].append("-")
   else:
    result_think["dday-ing"].append(d_split[0])
    result_think["Dday"].append(d_split[1])

#URL
  URL_list = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-title > a")
  aa='https://www.thinkcontest.com'
  for f in URL_list:
   result_think["url"].append(aa+f["href"])
  
 return result_think
  
if __name__ == '__main__':
	
	Crawling_think()
  
	for i in range(len(result_think["title"])):
         print(result_think["site"][i])
         print(result_think["title"][i])
         print(result_think["field"][i])
         print(result_think["host"][i])
         print(result_think["Dday"][i])
         print(result_think["dday-ing"][i])
         print(result_think["url"][i])
