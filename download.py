# coding=utf-8
import requests
import os
import re
import time
import threading
import sys
from bs4 import BeautifulSoup
import signal
from tqdm import tqdm
from threading import Thread

# 请先设置token、首页地址和代理，将________替换为网址，后面不改
token = "AF6sm"
proxies = {"http": 'http://127.0.0.1:1080', "https": 'http://127.0.0.1:1080'}
requestURL = "https://__________.com/"

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'multipart/form-data; session_language=cn_CN',
    'Connection': 'keep-alive',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name',
    'Referer': 'http://91porn.com',
    "Cookie": ""
}


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


def myFunc(f, chunk, pbar):
    f.write(chunk)
    pbar.update(1024)
    return 'success'


def download_from_url(url, title):
    dst = "../91视频MP4/" + title
    while True:
        try:
            response = s.get(url,
                             proxies=proxies,
                             headers=headers,
                             timeout=5,
                             stream=True)  #(1)
            if response.status_code == 404:
                time.sleep(3)
                return 0
            break
        except Exception:
            time.sleep(5)
            continue
    file_size = int(response.headers['content-length'])  #(2)
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)  #(3)
    else:
        first_byte = 0
    if first_byte >= file_size:  #(4)
        return file_size
    if first_byte > 0:
        headersRange = {'Range': f'bytes={first_byte}-{file_size}'}
        headersRange.update({
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name'
        })
        while True:
            try:
                response = s.get(url,
                                 proxies=proxies,
                                 headers=headersRange,
                                 timeout=5,
                                 stream=True)
                break
            except Exception:
                time.sleep(5)
                continue

    pbar = tqdm(total=file_size,
                initial=first_byte,
                unit='B',
                unit_scale=True,
                desc=title)
    with (open(dst, 'ab')) as f:
        try:
            for chunk in response.iter_content(chunk_size=1024):  #(6)
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        except Exception as e:
            str(e)
    pbar.close()
    return file_size


def strencode2(str):
    print(token, str)
    return requests.post("https://www.91api.org/api/decode2",
                         data={
                             "token": token,
                             "str": str
                         }).text


def strencode(str):
    return requests.post("https://www.91api.org/api/decode",
                         data={
                             "token": token,
                             "str": str
                         }).text


def filter_str(title):
    nomakechar = [":", "/", "\\", "?", "*", "“", "<", ">", "|", "\n", '"']
    for item in nomakechar:
        if title.find(item) > -1:
            title = title.replace(item, '')
    title = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]').sub('', title)
    return title


def getVideoUrl(base_req):
    try:        
        if "你每天只可观看" in base_req.text:
            return -2
        video = BeautifulSoup(base_req.text,
                              "html.parser").find_all("video", id="player_one")
        a = re.compile('document.write\(strencode2\("(.*)"').findall(
            str(video))
        url = ''
        if len(a) > 0:
            a = a[0].split(',')
            text = a[0].replace('"', '')
            url = strencode2(text)

        else:
            a = re.compile('document.write\(strencode\("(.*)"').findall(
                str(video))
            text = a[0].split(',')
            url = strencode(text)


        if url == "需要授权":
            print("请修改token")
            return 0
        elif url == "解密失败":
            print("解密失败")
            return 0
        print(url)
        return url
    except IndexError:
        print(base_req.text)
        return -2
    except Exception as e:
        print(e)
        time.sleep(5)
        return 0


requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接


def getURLAndDownload(viewurl, titles, author, index, page, isdownload720P):
    print('#' * 100)
    while True:
        try:
            base_req = s.get(url=viewurl[index],
                             proxies=proxies,
                             headers=headers,
                             timeout=5)
            break
        except:
            time.sleep(5)
            continue
    html = BeautifulSoup(base_req.text, "html.parser")
    hdimg = html.find_all(
        lambda tag: tag.name == "img" and tag.attrs["src"] == "images/hd.png")
    if len(html.find_all("span", class_="title-yakov")) == 0:
        return -1, titles[index]
    uploadtime = html.find_all("span", class_="title-yakov")[0].text
    formatTitle = filter_str(titles[index] + "(@" + author[index] + " 上传于" +
                             uploadtime + ").mp4")
    dst = "../91视频MP4/" + formatTitle
    dst1 = "../下载汇总/" + formatTitle
    dst2 = "../91视频/" + formatTitle
    print('第' + str(page) + '页数据,共' + str(len(viewurl)) + '条帖子 =>>>> 正在下载第' +
          str(index + 1) + '个帖子……' + formatTitle)
    if os.path.exists(dst) or os.path.exists(dst1) or os.path.exists(dst2):
        print("已下载，自动跳过！！")
        # print('#' * 100 + '\n')
        time.sleep(3)
        return -1, formatTitle
    hasHD = len(hdimg) > 0
    hasHD = False
    if hasHD and isdownload720P == False:
        Redirect = hdimg[0].find_next_sibling().attrs["href"]
        while True:
            try:
                base_req = s.get(url=requestURL + Redirect,
                                 proxies=proxies,
                                 headers=headers,
                                 timeout=5)
                break
            except:
                time.sleep(5)
                continue
    url = getVideoUrl(base_req)
    if url == 0:
        return 0, formatTitle
    elif url == -2:
        return -2, formatTitle

    # txttime = time.strftime("%Y-%m-%d", time.localtime())
    # videotype = urlparse(url).path.split(".")[1]
    dst = "../91视频MP4/" + formatTitle
    dst1 = "../下载汇总/" + formatTitle
    while True:

        videoSize = download_from_url(url, formatTitle)
        if videoSize == 0:
            break
        downloadSize = os.path.getsize(dst)
        if downloadSize < videoSize:
            continue
        else:
            break
    return videoSize, formatTitle


# 爬虫主体，flag为页码
def spider():
    inputPage = input("请输入开始下载的页数：")
    inputtitle = input("请输入从当前页的第几个帖子开始下载：")
    page = int(inputPage)

    while int(page) <= int(100000):
        viewurl = []
        titles = []
        author = []
        base_url = requestURL + 'view_video.php?viewkey='
        page_url = requestURL + 'v.php?next=watch&page=' + str(page)
        while True:
            try:
                get_page = s.get(url=page_url,
                                 proxies=proxies,
                                 headers=headers,
                                 timeout=5)
                break
            except Exception as e:
                print(e)
                time.sleep(5)
                continue
        # 利用正则匹配出特征地址
        div = BeautifulSoup(get_page.text, "html.parser").find_all(
            "div", class_="well well-sm videos-text-align")
        for i in div:
            hd = i.find_all("div", class_="hd-text-icon")
            title = i.find(
                "span",
                class_="video-title title-truncate m-t-5").text.strip()
            if len(hd) > 0:
                titles.append(filter_str(title) + "-HD")
            else:
                titles.append(filter_str(title))
            author.append(
                i.find_all("span",
                           class_="info")[1].nextSibling.replace("\n",
                                                                 "").strip())
            viewurl.append(i.a.attrs["href"])
        arr = []
        if int(inputPage) == int(page):
            arr = range(-1 + int(inputtitle), len(viewurl))
        else:
            arr = range(0, len(viewurl))
        for index in arr:
            retry = 1
            isdownload720P = False
            while True:
                if retry == 3:
                    isdownload720P = True
                result = getURLAndDownload(viewurl, titles, author, index,
                                           page, isdownload720P)
                dst = "../91视频MP4/" + result[1]
                if result[0] == -2:
                    print("已达上限")
                    return
                elif result[0] == 0 and retry <= 3:
                    retry += 1
                    continue
                elif result[0] != -1 and retry <= 3 and os.path.getsize(
                        dst) < 2000:
                    os.remove(dst)
                    isdownload720P = True
                    retry += 1
                    continue

                else:
                    break

                    # if not os.path.exists(dst) and not os.path.exists(dst1):
                    #     func_downloadmp4.thread(url,dst)

                    # dv = down_video()
                    # dv.set_headers({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name'})
                    # dv.main(url,dst)
            print('#' * 100 + '\n')
            time.sleep(3)
        page += 1


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
