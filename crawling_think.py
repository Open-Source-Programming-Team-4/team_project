#!/usr/bin/python3
#-*- coding: utf-8 -*-


#최대페이지, URL 해결. 1~2669 까지 매번 돌릴 것인지 결정하기.
# 시간이 많이 걸리니까 다른곳에다가 저장해놓고 새로운 것들만 크롤링하는 것도 방법.

#result(dict)의 각 0번들 
#2021 그린스마트 미래학교「가상설계 및 콘텐츠」공모전
#['', '논문/리포트', '기획/아이디어', '디자인', 'UCC/영상', '문학/수기', '건축/건설', '']
#교육부, 전국 17개 시ㆍ도교육청
#D-2
#접수예정
#https://www.thinkcontest.com/Contest/ContestDetail.html?id=31018


import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

# https://www.thinkcontest.com/Contest/ContestDetail.html?id=31076
#id뒤의 숫자가 각 공모전의 번


result = { "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [] }

#마지막 페이지 리턴.
def FindMaxPage_think(url):호
  res=requests.get(url)
  soup=BeautifulSoup(res.content,"html.parser")
  maxpage = soup.select("#main > div > div.body.contest-cate > div > div.paging-wrap > div > a")[8]
  max=maxpage["href"].split('=')

  return max[1]

def Crawling_think(url):
  for num in range(1,400):
	num=str(num)
      	url='https://www.thinkcontest.com/Contest/CateField.html'+'?page=' + num
      	res=requests.get(url)
      	soup=BeautifulSoup(res.content,"html.parser")
      	for n in range(10):
        	result_think["site"].append("씽굿") 
      	title = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-title > a")
      	for sp_list in title:
        	result_think["title"].append(sp_list.text)
      	field = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-cate")
      	for b in field:
        	list_text=b.text
        	split_list=list_text.split()
        	result_think["field"].append(split_list)
      	host = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(2)")
      	for c in host:
        	result_think["host"].append(c.text)
      	dday = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(3) > p")
      	for d in dday:
        	result_think["Dday"].append(d.text)
      	mode = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td:nth-of-type(3) > span > span")
      	for e in mode:
        	result_think["dday-ing"].append(e.text)
      	URL_list = soup.select("#main > div > div.body.contest-cate > div > table > tbody > tr > td.txt-left > div.contest-title > a")
      	aa='https://www.thinkcontest.com'
      	for f in URL_list:
        	result_think["url"].append(aa+f["href"])
  

if __name__ == '__main__':
	url = u'https://www.thinkcontest.com/Contest/CateField.html'
 
  #maximum = int(FindMaxPage_think(url))
	Crawling_think(url)
  

	print(len(result_think["site"]))

  
	for i in range(len(result_think["title"])):
	print(result_think["site"][i])
    	print(result_think["title"][i])
    	print(result_think["field"][i])
    	print(result_think["host"][i])
    	print(result_think["Dday"][i])
    	print(result_think["dday-ing"][i])
    	print(result_think["url"][i])

  	print(len(result_think["Dday"]))
