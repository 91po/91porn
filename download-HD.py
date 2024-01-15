# coding=utf-8
import requests
import os
import re
import time
import random
import threading
import sys
import base64
from bs4 import BeautifulSoup
import js2py
import signal
from tqdm import tqdm
from urllib.parse import urlparse
from threading import Thread

headers={
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Content-Type': 'multipart/form-data; session_language=cn_CN',
    'Connection': 'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name',
    'Referer':'http://91porn.com',
    "Cookie":""}

class MyThread(Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

def myFunc(f,chunk,pbar):
    f.write(chunk)
    pbar.update(1024)
    return 'success'

def download_from_url(url, title):
    dst="../91视频MP4/"+title
    while True:
        try:
            response = s.get(url, proxies=proxies, headers=headers, timeout=5, stream=True) #(1)
            if response.status_code == 404:
                time.sleep(3)
                return 0
            break
        except Exception:
            time.sleep(5)
            continue
    file_size = int(response.headers['content-length']) #(2)
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst) #(3)
    else:
        first_byte = 0
    if first_byte >= file_size: #(4)
        return file_size
    if first_byte >0:
        headersRange = {
                'Range': f'bytes={first_byte}-{file_size}'
            }
        headersRange.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name'})
        while True:
            try:
                response = s.get(url, proxies=proxies, headers=headersRange, timeout=5, stream=True)
                break
            except Exception:
                time.sleep(5)
                continue

    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=title)
    with(open(dst, 'ab')) as f:
        try:
            for chunk in response.iter_content(chunk_size=1024): #(6)
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        except Exception as e:
            str(e)
    pbar.close()
    return file_size


# 定义随机ip地址
def random_ip():
    a=random.randint(1, 255)
    b=random.randint(1, 255)
    c=random.randint(1, 255)
    d=random.randint(1, 255)
    return (str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))

encodedata2 = open("strencode2.js",'r',encoding= 'utf8').read()
encodedata1 =  open("strencode.js",'r',encoding= 'utf8').read()
strencode2 = js2py.eval_js(encodedata2)
strencode = js2py.eval_js(encodedata1)

proxies ={
    "http": 'socks5://127.0.0.1:1080',
    "https": 'socks5://127.0.0.1:1080'
}

def filter_str(title):
    nomakechar =  [":","/","\\","?","*","“","<",">","|","\n",'"']
    for item in nomakechar:
        if title.find(item)>-1:
            title = title.replace(item, '')
    title = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]').sub('',title)
    return title

def getVideoUrl(base_req):
    try:
        video = BeautifulSoup(base_req.text, "html.parser").find_all("video",id="player_one")
        a = re.compile('document.write\(strencode2\("(.*)"').findall(str(video))
        url = ''
        if len(a)>0:
            a = a[0].split(',')
            text = a[0].replace('"', '')
            if BeautifulSoup(strencode2(text), "html.parser").source == None:
                url = BeautifulSoup(strencode2(text), "html.parser").a.attrs['href']
            else:
                url = BeautifulSoup(strencode2(text), "html.parser").source.attrs['src']
        else:
            a= re.compile('document.write\(strencode\("(.*)"').findall(str(video))
            text = a[0].split(',')
            url = BeautifulSoup(strencode(text[0].replace('"', ''),text[1].replace('"', ''),text[2].replace('"', '')), "html.parser").source.attrs['src']
        return url
    except Exception as e:
        print(e)
        time.sleep(5)
        return 0

requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
s = requests.session()
s.keep_alive = False # 关闭多余连接
requestURL = "https://w1030.9p47q.com/"





def quit(signum, frame):
    print("Bye!")
    sys.exit(0)
    
# i为线程数
def main():
    work_thread = threading.Thread(target=spider)
    work_thread.daemon = True
    work_thread.start()
    signal.signal(signal.SIGINT, quit)
    print("Start Working")
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()


