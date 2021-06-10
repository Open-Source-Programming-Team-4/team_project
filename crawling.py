#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup




#---------------------------------------------------------- sub function ----------------------------------------------------------




def SplitFieldString(s , wordlist=[ "분야" ] , dividchar=[",",":","/"]) :
    '''
     field에서 각 필드를 나누고 앞의 "분야 : " 문자를 제거하는 함수
     worldlist에 있는 문자열이 확인되면 return에서 제거
     dividchar로 문자를 구분하는 기호들의 리스트를 받음
     dividchar[0] => 기준이 되는 기호 ( 최소한 하나는 있어야 함 )
     dividchar[1~n] => 0번째 요소로 바뀔 기호 ( 선택 )

     이부분은 별로라고 생각해서 바꿀수 있으면 바꿔주세요...

     return : 분야(문자열)들이 담긴 리스트
    '''
    
    if len(dividchar) > 1 :
        for i in dividchar[1:] :
            s = s.replace( i , dividchar[0] )
    
    return list(filter(lambda x : x not in wordlist , list(map( str.strip , s.split(dividchar[0])))))









def FindMaxPage_wevity(page ,URL ) :
    '''
     wevity의 사이트에서 공모전 목록 페이지가 얼마나 있는지 확인하는 함수

     input : page - 현재 페이지 넘버
             URL - 사이트 주소 url

     output : 배열 index[0] - 현 페이지에서 갈 수 있는 최대 페이지 넘버
                  index[1] - 현 페이지와 최대 페이지의 차이가 9면 True , 아니면 False
    '''

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
        # 이거땜에 re 못지움 ==> 더 좋은 방법 구하는 중
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


#---------------------------------------------------------- crawling fuction ----------------------------------------------------------







def CrawlingByField_wevity( pagenum , whatfield=0 , mode="") :

    """ ---------- wevity 크롤링 함수 ---------- 
     분야와 접수정보를 parameter로 받아 해당하는 페이지의 정보를 return

     - page : 페이지 수 
    
     - filed : 분야 설정 (default : 0 - 모든분야 )

        기획/아이디어 - 1 , 광고/마케팅 - 2 , 논문/리포트 - 3 
        영상/UCC/사진 - 10 , 디자인/케릭터/웹툰 - 19 , 웹/모바일/IT - 20
        게임/소프트웨어 - 21 , 과학/공학 - 22 , 문학/글/시나리오 - 23
        건축/건설/인테리어 - 24 , 네이밍/슬로건 - 25 , 예체능/미술/음악 - 26
        대외활동/서포터즈 - 27 , 봉사활동 - 89 , 취업/창업 - 88
        해외 - 28 , 기타 - 29

     - mode :  접수 정보 (default : "" - 전체 )

        스페셜 - "spec" , 신규 - "new" , 마감임박 - "soon"
        접수중 - "ing", 접수예정 - "future" , 마감 - "end"

     출력값 - 공모전 정보를 list로 가지는 dict

    """
    if mode != "" :
        mode = "&mode=" + mode
        
    if whatfield == 0 :
        whatfield = ""
    else :
        whatfield = "&cidx="+ str(whatfield)

    URL = "https://www.wevity.com/?c=find&s=1"+ mode + "&gub=1" + whatfield + "&gp=1"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    whole_source = "" # 페이지 순회하며 필요한 정보만 저장할 문자열
    URL = URL[:-1] 

    #해당 테이블을 포함하는 html들을 whole_sourse 문자열에 저장
    for page_number in range(1, pagenum):
	    URLS = URL + str(page_number)
	    response = requests.get(URLS)
	    whole_source = whole_source + response.text

    # 출력값 - 이름 , 분야 , 주최자 정보를 list로 가지는 dict
    result = { "site" : [] , "title" : [] , "field" : [] , "host" : [] , "Dday" : [] , "dday-ing" : [] ,"url" : [] }

    #통합된 html에서 공모전 이름 , 분야 , 주최자 정보 추출 
    soup = BeautifulSoup(whole_source, 'html.parser')


    #############################################################################################


    # ⚠ 주의 - 지극히 wevity html 파일에 맞춰진 코드로 이후 다른 사이트에서 크롤링시 작동하지 않을 가능성 매우 높음 ⚠

    # title ( string ) - 공모전 이름을 저장하는 부분
    find_title = soup.select("li > div.tit > a")
    for title in find_title :
        result["url"].append("https://www.wevity.com/" + title["href"])
        result["site"].append("wevity")
        # title은 a tag 안에 span tag가 자식태그로 있어서 자식 태그 span을 제외하고 a의 내용만 받아야 함
        t_soup = BeautifulSoup(str(title), 'html.parser')           # a tag => t_soup
        if t_soup.select('span') != [] :                            # span 태그가 자식으로 있다면
            for i in t_soup.select('span') : i.decompose()          # decompose()로 제거해줌
            result["title"].append(t_soup.text.rstrip())
        else :                                                      # span 태그 없다면 그냥 결과물 딕셔너리에 넣어줌
            result["title"].append(title.text.rstrip())

    # filed ( list[ type(string) ] ) - 공모전의 분야들을 저장하는 부분
    find_field = soup.select("li > div.tit > div.sub-tit")
    for field in find_field :
        result["field"].append(SplitFieldString(field.text))

    # host ( string ) - 공모전 주최자를 저장하는 부분
    find_host = soup.select("li:not(.top) > div.organ")
    for host in find_host :
        result["host"].append(host.text)

    #D-day 와 진행상황을 얻기 위한 코드
    find_Dday = soup.select("li:not(.top) > div.day")
    for day in find_Dday :
        d_soup = BeautifulSoup(str(day), 'html.parser')
        result["dday-ing"].append(d_soup.find('span').text.replace('\n',''))
        for i in d_soup.select('span') : i.decompose()
        result["Dday"].append(' '.join(d_soup.text.split()))

    
    

    #############################################################################################


    return result
    


#---------------------------------------------------------- test ----------------------------------------------------------



if __name__ == "__main__" :
    # 여기서 테스트 해보세요 
    #data = CrawlingByField_wevity(whatfield=2, mode="end")
    #data = CrawlingByField_wevity(whatfield=28, mode="soon")
    #data = CrawlingByField_wevity(whatfield=21)
    data = CrawlingByField_wevity(2 , whatfield=0 , mode="ing")
    
    for i in range(len(data["title"])) :
        print(data["site"][i])
        print(data["title"][i])
        print(data["field"][i])
        print(data["host"][i])
        print(data["Dday"][i])
        print(data["dday-ing"][i])
        print(data["url"][i])
        print("----------------------------------------")
    print(str(len(data["title"]))+"개의 공모전 정보를 탐색했습니다.")
    


    



