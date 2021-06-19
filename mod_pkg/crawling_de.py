#!/usr/bin/python3
#-*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup

def split_txt(fileds) :
    return list(map(str.strip , fileds.replace("#","").replace("/",",").split(",")))
    
def crawling_detizen ( pageNum ) :
    URL = "http://www.detizen.com/contest/?PC="
    whole_source = "" # 페이지 순회하며 필요한 정보만 저장할 문자열

    #해당 테이블을 포함하는 html들을 whole_sourse 문자열에 저장
    for page_number in range(1, pageNum):
	    URLS = URL + str(page_number)
	    response = requests.get(URLS)
	    whole_source = whole_source + response.text

    soup = BeautifulSoup(whole_source, 'html.parser')
    items = soup.select("#Contents > #Main .basic-list.page-list > li")
    result = { "site" : [] , "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [] }
    
    for item in items :
        result["site"].append("detizen")
        result["title"].append(item.select_one("div.main-info > h4 > a:nth-of-type(1)").text)
        result["host"].append(split_txt(item.select_one("p:nth-of-type(1) > span").text))   
        item.select_one("p:nth-of-type(1) > span").decompose()
        result["Dday"].append(item.select_one("div.main-info > p > span").text)
        result["dday-ing"].append("-")
        result["field"].append(split_txt(item.select_one("p:nth-of-type(1)").text))
        result["url"].append(URL[:-4] + item.select_one("div.main-info > h4 > a:nth-of-type(1)")["href"])
        
    return result

if __name__ == "__main__" :
    result = crawling_detizen(10)
    data_num = len(result["site"])
    for i in range(data_num) :
        print("-------------------------------------------")
        print(" 사이트 : " + result["site"][i])
        print(" 제목 : " + result["title"][i])
        print(" 주최사 : " + str(result["host"][i]))
        print(" 분야 : " + str(result["field"][i]))
        print(" D-day : " + result["Dday"][i])
        print(" 진행상황 : " + result["dday-ing"][i])
        print(" URL : " + result["url"][i])
    print("크롤링한 공모전의 수는 " +str(data_num) + "개입니다.")
    
