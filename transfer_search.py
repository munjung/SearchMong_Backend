import urllib.request
import ssl
import cgi
import cgitb
import json
from urllib.parse import quote
from threading import Thread

cgitb.enable()

appkey = 'appkey'
client_id = 'id'
client_secret = 'sec'

status = 0
kor_res = ''

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
        global status
        global kor_res
        status = 1
        kor_res = json_data["message"]["result"]["translatedText"]
        return kor_res

    else:
        return "Error"



def find_image(keyword_str: str):
    keyword_str = quote(keyword_str)
    url = 'https://dapi.kakao.com/v2/search/image'
    request = urllib.request.Request(url)
    request.add_header('Authorization', 'KakaoAK {}'.format(appkey))
    data = 'query=' + keyword_str + "&sort=accuracy"
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        res = response.read().decode('utf-8')
        print(res)
    else:
        print("Error Code:" + rescode)


params = cgi.FieldStorage()
keyword = params['keyword'].value

t1 = Thread(target=eng_to_kor, args=keyword)
t1.start()
t1.join()

if status > 0:
    find_image(kor_res)

else:
    print("Error")