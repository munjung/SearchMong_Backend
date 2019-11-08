#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import codecs
import cgi
import cgitb
cgitb.enable()
print ("Content-type: text/html; charset=utf-8\r\n")
import json
import urllib.request
import ssl
from urllib.parse import quote

appkey = 'key'
client_id = 'id'
client_secret = 'sec'

status = 0
kor_res = ''


def eng_to_kor(keyword: str):
    url = "https://openapi.naver.com/v1/language/translate"
    data = 'source=en&target=ko&text='+keyword
    request = urllib.request.Request(url)
    request.add_header('X-Naver-Client-Id', client_id)
    request.add_header('X-Naver-Client-Secret', client_secret)
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        print(response_body)
        return kor_res

    else:
        return "Error"


params = cgi.FieldStorage()
keyword = params['keyword'].value
find_image = params['find_image'].value
tmp = params['tmp'].value

#print(int(tmp))

if int(tmp) == 0: #papago
    keyword = keyword.replace('"',"")
    res = eng_to_kor(keyword)
    print(res)

else: #image research
    find_image = find_image.replace('"',"")
    enc = urllib.parse.quote(find_image)
    url = 'https://dapi.kakao.com/v2/search/image'
    request = urllib.request.Request(url)
    request.add_header('Authorization', 'KakaoAK {}'.format(appkey))
    data = 'query=' + enc + "&sort=accuracy"
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        print(response.read())
    else:
        print("Error Code:" + rescode)