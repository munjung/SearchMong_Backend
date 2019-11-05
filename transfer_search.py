import urllib.request
import ssl
import cgi
import cgitb
import json
from urllib.parse import quote

cgitb.enable()
params = cgi.FieldStorage()

keyword = params['keyword'].value

client_id = 'idid'
client_secret = 'secret'

def eng_to_kor(keyword: str):
    encText = urllib.parse.quote(keyword)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/language/translate"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read().decode('utf-8')
        json_data = json.loads(response_body)
        keyword_str = json_data["message"]["result"]["translatedText"]
        find_image(keyword_str)

    else:
        print("Error Code:" + rescode)

def find_image(keyword_str: str):
    keyword_str = quote("태항호")
    url = "https://openapi.naver.com/v1/search/image?query=" + keyword_str + "&display=10&start=1&sort=sim"
    # data = keyword_str + "&display=10&start=1&sort=sim"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200 :
        response_body = response.read()
        print(response_body.decode('utf-8'))