#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

# 특정 문자열 제거 함수 
# input : wordList( 제거할 문자열로 이루어진 리스트 )
#         string( 특정 문자열을 제거할 문자열 )
# output : 특정 문자열을 제거한 문자열
# ex) RemoveWords(["hi","hello"] , "hi,my name is youngwoo hello~") ==> ( ",my name is youngwoo ~" )
def RemoveWords(wordlist , string) :
    return re.sub('|'.join(wordlist) , '' , string)

# field에서 각 필드를 나누고 앞의 "분야 : " 문자를 제거하는 함수
# 우선 field에 맞춤 설계 - 이후 수정가능성 있음
def SplitFieldString(s ,wordlist=["분야 : "]) :
    result = re.sub(r'[/,]' ,' ', RemoveWords(wordlist , s))
    return result

# wevity의 사이트에서 공모전 목록 페이지가 얼마나 있는지 확인하는 함수 
# input : page - 현재 페이지 넘버 
#         URL - 사이트 주소 url
# output : 배열 index[0] - 현 페이지에서 갈 수 있는 최대 페이지 넘버
#              index[1] - 현 페이지와 최대 페이지의 차이가 9면 True , 아니면 False
def FindMaxPage_wevity(page ,URL ) :
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    maximum = 0
    initialpage = page
    isNext = True

    # 몇페이지까지 있는지 확인하는 while문
    # wevity는 https://www.wevity.com/?c=find&s=1&gub=1&gp=1 같은 주소
    # 뒤의 gp="num"으로 페이지 확인 가능하고 위의 예시는 1페이지임
    # 페이지 하단에 페이지 이동 a태그의 href를 통해 1페이지에서 시작하면 10페이지까지 있는지   

    while 1:
        page_list = soup.findAll(href=re.compile("gp="+str(page)))        
        if not page_list:                      
            maximum = page - 1
            break
        page = page + 1
    
    # ⚠️ 페이지 이동 a 태그가 10개가 최대이니 10개가 있다면 다음 페이지도 있다고 가정하여 작성함 ⚠️
    # ⚠️ 만약 10개 페이지가 전부이고 이후 페이지가 더 없다면 오류 발생할 가능성 높음 ⚠️
    if maximum - initialpage != 9 :
        isNext = False 
    
    return  [ maximum , isNext ]



def CrawlingByField_wevity(field=0 , mode="ing") :

    """ ---------- wevity 크롤링 함수 ---------- 
     분야와 접수정보를 parameter로 받아 해당하는 페이지의 정보를 return
    
     - filed : 분야 설정 (default : "" - 모든분야 )

        기획/아이디어 - 1 , 광고/마케팅 - 2 , 논문/리포트 - 3 
        영상/UCC/사진 - 10 , 디자인/케릭터/웹툰 - 19 , 웹/모바일/플래시 - 20
        게임/소프트웨어 - 21 , 과학/공학 - 22 , 문학/글/시나리오 - 23
        건축/건설/인테리어 - 24 , 네이밍/슬로건 - 25 , 예체능/미술/음악 - 26
        대외활동/서포터즈 - 27 , 봉사활동 - 89 , 취업/창업 - 88
        해외 - 28 , 기타 - 29

     - mdoe :  접수 정보 (default : "ing" - 접수중 )

        스페셜 - "spec" , 신규 - "new" , 마감임박 - "soon"
        접수중 - "ing", 접수예정 - "future" , 마감 - "end"
    """

    mode = "&mode="+ mode
    if field == 0 :
        field = ""
    else :
        field = "&cidx="+ str(field)

    URL = "https://www.wevity.com/?c=find&s=1"+ mode + "&gub=1" + field + "&gp=1"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    page = 1    # 최종 페이지 탐색 while문에서 페이지넘버 값 저장
    maximum = []    # index:0 => 최종 페이지 넘버 , index:1 => 이후페이지 존재여부 bool type 

    while True :
        maximum =  FindMaxPage_wevity(page,URL)
        if not maximum[1] :
            break
        page = maximum[0] + 1


    whole_source = "" # 페이지 순회하며 필요한 정보만 저장할 문자열
    URL = URL[:-1] 

    #해당 테이블을 포함하는 html들을 whole_sourse 문자열에 저장
    for page_number in range(1, maximum[0]+1):
	    URLS = URL + str(page_number)
	    response = requests.get(URLS)
	    whole_source = whole_source + response.text

    # 출력값 - 이름 , 분야 , 주최자 정보를 list로 가지는 dict
    result = { "title" : [] , "field" : [] , "host" : []}

    #통합된 html에서 공모전 이름 , 분야 , 주최자 정보 추출 
    soup = BeautifulSoup(whole_source, 'html.parser')

    find_title = soup.select("li > div.tit > a")
    for title in find_title :

        # 임시로 SPECIAL , IDEA 넣어놓음 이후 수정
	    
        result["title"].append(RemoveWords(["SPECIAL" , "IDEA"] , title.text.encode('utf8')).rstrip())

    find_field = soup.select("li > div.tit > div.sub-tit")
    for field in find_field :
        result["field"].append(SplitFieldString(field.text.encode('utf-8')))
        
    find_host = soup.select("li > div.organ")
    for host in find_host :
        result["host"].append(host.text.encode('utf8'))

    return result
    


if __name__ == "__main__" :
    # 여기서 테스트 해보세요 
    data = CrawlingByField_wevity(field=2)
    
    for i in range(len(data["title"])) :
        print(data["title"][i] + " / " + data["field"][i] + " / " + data["host"][i] )



    



