import urllib.request
import ssl
import cgi
import cgitb
import json

cgitb.enable()
params = cgi.FieldStorage()

keyword = params['keyword'].value

client_id = 'Ze_M4Mr7yphwtkKAnDxT'
client_secret = 'qMtvEksYrR'

encText = urllib.parse.quote("hello")
data = "source=en&target=ko&text=" + encText
url = "https://openapi.naver.com/v1/language/translate"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
ssl._create_default_https_context = ssl._create_unverified_context
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read().decode('utf-8')
    json_obj = re
else:
    print("Error Code:" + rescode)
