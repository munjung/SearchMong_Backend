#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import codecs
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import cgi
import cgitb
cgitb.enable()

print("Content-type: text/html; charset=utf-8\r\n")

import json
import cv2
import os
import requests
from PIL import Image
import urllib
import urllib.request
import urllib.parse
import ssl
from threading import Thread
from urllib import parse
import copy

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024
LIMIT_BOX = 40

def image_url_save(image_url, image_type):
    ssl._create_default_https_context = ssl._create_unverified_context
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]

    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(image_url, "/home/ubuntu/searchmong/tmp/temp."+image_type)


def ocr_resize(image_path: str):
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None

def ocr_detect(image_path: str, appkey: str):

    API_URL = 'https://kapi.kakao.com/v1/vision/text/detect'
    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"file": data})


def ocr_recognize(image_path: str, boxes: list, appkey: str):
    API_URL = 'https://kapi.kakao.com/v1/vision/text/recognize'
    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"file": data}, data={"boxes": json.dumps(boxes)})

def remove_img(image_path):
    os.remove(image_path)
    if os.path.exists(image_path) is False:
        return True

params = cgi.FieldStorage()
image_url = params["image_url"].value
image_type = params['image_type'].value

image_url = image_url.replace('"'," ")
image_type = image_type.replace('"'," ")

image_url_save(image_url,image_type)

image_path = "/home/ubuntu/searchmong/tmp/temp."+image_type
#print(image_path)
appkey = "appkey"

resize_impath = ocr_resize(image_path)
if resize_impath is not None:
    image_path = resize_impath

output = ocr_detect(image_path, appkey).json()
boxes = output["result"]["boxes"]
boxes = boxes[:min(len(boxes), LIMIT_BOX)]
status = ocr_recognize(image_path, boxes, appkey).status_code

if status == 200:
    output = ocr_recognize(image_path, boxes, appkey).json()
   # remove_img(image_path)
    print(output["result"]["recognition_words"])

else:
    print(status)
