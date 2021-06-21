#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup


#---------------------------------------------------------- crawling fuction ----------------------------------------------------------


def Crawling_wevity( P_num ) :


    URL = "https://www.wevity.com/?c=find&s=1&gub=1&gp="

    whole_source = "" # 페이지 순회하며 필요한 정보만 저장할 문자열

    #해당 테이블을 포함하는 html들을 whole_sourse 문자열에 저장
    for page_number in range(1, P_num+1):
	    URLS = URL + str(page_number)
	    response = requests.get(URLS)
	    whole_source = whole_source + response.text
        
    # 출력값 - 이름 , 분야 , 주최자 정보를 list로 가지는 dict
    result = { "site" : [] , "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [] }

    #통합된 html에서 공모전 이름 , 분야 , 주최자 정보 추출 
    soup = BeautifulSoup(whole_source, 'html.parser')
    items = soup.select(".ms-list > .list > li")
    
    count = 0
    for item in items :
        count = count + 1
        if count == 1 or count % 37 == 1 :
            continue
        result["site"].append("wevity")
        if item.select(".tit > a > span") != [] :
            for i in item.select(".tit > a > span") : i.decompose()
        result["title"].append(item.select_one(".tit > a").text)
        result["field"].append(item.select_one(".tit > .sub-tit").text[5:])
        result["host"].append(item.select_one(".organ").text)
        result["dday-ing"].append(item.select_one(".day > span").text)
        item.select_one(".day > span").decompose()
        result["Dday"].append(item.select_one(".day").text.strip())
        result["url"].append("https://www.wevity.com/" + item.select_one(".tit > a")["href"])
        


    return result
    


#---------------------------------------------------------- test ----------------------------------------------------------



if __name__ == "__main__" :
    # 여기서 테스트 해보세요 
    data = Crawling_wevity(20)
    #data = CrawlingByField_wevity(whatfield=28, mode="soon")
    #data = CrawlingByField_wevity(whatfield=21)
    #data = CrawlingByField_wevity()
    
    for i in range(len(data["title"])) :
        print(data["title"][i])
        print(data["field"][i])
        print(data["host"][i])
        print(data["Dday"][i])
        print(data["dday-ing"][i])
        print(data["url"][i])
        print("----------------------------------------")
    print(str(len(data["title"]))+"개의 공모전 정보를 탐색했습니다.")
    


    



