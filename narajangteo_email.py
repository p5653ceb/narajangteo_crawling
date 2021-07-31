#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import datetime, time
from time import localtime, strftime
from datetime import timedelta
import urllib
import urllib.request
from urllib.parse import quote
from urllib.request import Request, urlopen
import smtplib, os
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 


# 카테고리 파일 열고 읽어오기
f = open("category.txt")
line = f.readline()
category_list = line.split('/')
f.close


# 날짜 설정 (현재 공고일 당일 기준 15일 전까지 크롤링하도록 함)
d = datetime.date.today()
td = timedelta(days=15)
fromtd = d - td;
fromBidDt = "20" + str(fromtd.strftime("%y/%m/%d"))
toBidDt = "20" + str(d.strftime("%y/%m/%d"))

datas = []
for category in category_list:
    bidNm = category
    bidNm = urllib.parse.quote_plus(category, encoding='euc-kr')
    instNm = ""
    radOrgan = 1
    fromOpenBidDt = "";
    toOpenBidDt = "";
    bidno="";
    urlString = "http://www.g2b.go.kr:8101/ep/tbid/tbidList.do?searchType=1&bidSearchType=1taskClCds=5&bidNm=" + bidNm + "&searchDtType=1&fromBidDt=" + urllib.parse.quote_plus(fromBidDt, encoding='euc-kr') + "&toBidDt=" + urllib.parse.quote_plus(toBidDt, encoding='euc-kr') + "&fromOpenBidDt=" + fromOpenBidDt + "&toOpenBidDt=" + toOpenBidDt + "&radOrgan=1&instNm=&instSearchRangeType=&refNo=&area=&areaNm=&industry=&industryCd=&budget=&budgetCompare=UP&detailPrdnmNo=&detailPrdnm=&procmntReqNo=&intbidYn=&regYn=Y&recordCountPerPage=30"
    body = urllib.request.urlopen(urlString)    
    soup = BeautifulSoup(body, 'html.parser')
    selector = '#container div td div'
    num = int(len(soup.select(selector))/10)
    ls = [3]       
    ls2 = []
    for i in range(num):
        for j in ls:
            ls2.append(j + 10*i)
            
    for j, i in enumerate(ls2):
        # 3 : 공고명
        # 4 : 공고기관
        # 5: 수요기관
        # 7: 입력일시(입찰마감일시) .text
        datas.append({
            '검색어' : category,
            '용역명' : soup.select(selector)[i].text,
            '공고기관': soup.select(selector)[i+1].text,
            '수요기관': soup.select(selector)[i+2].text,
            '공고일자(마감일자)' : soup.select(selector)[i+4].text,
            'url' : soup.select(selector + ' a')[j*2+1]['href']
        })
        
        items_df = pd.DataFrame(datas)

html = items_df.to_html(justify='center')
items_df = items_df


import smtplib, os
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 

id = 'wemac' 
password = 'columbus13!' 
sendEmail = 'wemac@naver.com' 
subject = str(fromBidDt) + '~' + str(toBidDt) + ' 나라장터 공고 리스트'
text = html
addrs = ['sj@simonre.co.jp', 'shinekim@simonre.co.kr', 'parkhyungjae@kongje.or.kr','sklee@wemacc.com', 'jslee@wemacc.com', 'kimhyungki@kongje.or.kr', 'sunny@simonre.co.jp' ,'veronica@simonre.co.kr', 'rachelkoo@simonre.co.kr', 'dan@simonre.co.kr','hongchungmin@kongje.or.kr', 'koyeongchan@kongje.or.kr', 'jhlee@wemacc.com', 'ebchoi@wemacc.com', 'jessie@wemacc.com']  # send mail list 

# login 
smtp = smtplib.SMTP('smtp.naver.com', 587) 
smtp.ehlo() 
smtp.starttls() 
smtp.login(id, password) 

# message 
message = MIMEMultipart() 
message.attach(MIMEText(text, 'html')) 


message["From"] = sendEmail 
message["To"] = ",".join(addrs)
message['Subject'] = subject 
smtp.sendmail(sendEmail, addrs, message.as_string()) 

smtp.quit()