<p align="center">
    <a href="https://github.com/91po/91porn"><img src="https://github.com/91po/91porn/blob/main/logo.jpg"></a>
</p>

  
# 介绍
* 这个是一个使用python构建的获取某网站视频资源的简易爬虫，无须安装Chrome等浏览器，直接js解密（strencode1 strencode2函数）

# 基本要求
* 需要能访问得到某不存在的网站(某些校园网因为IPV6或教育网的原因可能可以直接访问)
* 若使用源码运行，需要预先安装python3及第三方包bs4及requests

# 使用方法
* 1.python download.py

# 改进
* 改进下载部分代码，实现重连以及多点下载
* 伪造cookie模拟登录，解除一个IP一天只能下10个视频的限制
* 完成友好的GUI界面

今日口令（每日21:00更新 ）**9vauB**, 时效:1天, 总次数:1000

# API版接口 

接口baseUrl: https://91api.org/api/

## 接口：获取视频列表
| 描述     | 内容               |
| -------- | ------------------ |
| 接口功能 | 请求91porn视频列表 |
| 请求协议 | HTTPS              |
| 请求方法 | GET                |
| 请求url  | list               |
| 响应格式 | json               |

### 请求参数

| 参数     | 描述                                             | 必填 | 类型   |
| -------- | ------------------------------------------------ | ---- | ------ |
| token    | 授权码                                            | 是   | String |
| category | 列表种类： rf-精华 tf-收藏 top-本月最热 hot-当前最热   | 否   | String |
| page     | 页码 默认: 1                                       | 否   | int    |

### 响应参数

| 参数        | 描述                     | 必有 | 类型          |
| ----------- | ------------------------ | ---- | ------------- |
| success     | 是否成功 0:失败 1: 成功    | 是   |       int     |
| data        | 视频列表，object格式见下   | 否   | Array[Object] |
| total       | 总页数                   | 否   | int           |
| msg         | 提示消息                 | 否   | String        |

data object结构,如下：

| 参数       | 描述        | 必有 | 类型   |
| ---------- | ----------- | ---- | ------ |
| viewkey    | 视频viewkey | 是   | String |
| title      | 视频标题    | 是   | String |
| pic        | 封面图片URL | 是   | String |
| duration   | 视频时长    | 是   | String |
| loadtime   | 上传日期    | 是   | Int |
| authorName | 作者名字    | 是   | String |
| pop        | 热度       | 是   | Int |
| fav        | 收藏        | 是   | Int |
| comments   | 留言        | 是   | Int |
| like       | 点赞       | 是   | Int |
| dislike    | 不喜欢     | 是   | Int |
| thumb      | 缩略视频URL | 是   | String |

### 请求示例

```
https://91api.org/api/list?category=rf&page=1
```

### 响应示例


```
{
    "data": [
        {
            "authorName": "匿名",
            "duration": "00:39:36",
            "loadtime": 1706909369,
            "pic": "https://172913mb/931273.jpg",
            "title": "看视频水印",
            "viewkey": "ce7cdddefa4799fd0451"
        },
        {
            "authorName": "匿名",
            "duration": "00:59:18",
            "loadtime": 1706909654,
            "pic": "https://17291rg/thumb/931270.jpg",
            "title": "刚开完家长会",
            "viewkey": "9f64fec40d63d153faaf"
        },
    ],
    "success": 1
}
```




## 接口：视频链接解密
| 描述     | 内容                |
| -------- | ------------------ |
| 接口功能 | 解密91porn加密链接    |
| 请求协议 | HTTPS               |
| 请求方法 | POST                |
| 请求url  | decode1 decode2     |
| 响应格式 | string               |


### 请求参数

| 参数      | 描述                                              | 必填 | 类型   |
| -------- | ------------------------------------------------ | ---- | ------ |
| token    | 授权码                                            | 是   | String |
| str      | 加密链接                                           | 是   | String |


### 响应参数

| 参数        | 描述                     | 必有 | 类型            |
| ----------- | ------------------------ | ---- | ------------- |
| str        | 解密链接                   | 是   | String        |



### 请求示例

```
wget https://www.91api.org/api/decode2 --post-data "token=口令&str=加密字符串"
```


### 响应示例


```
https://xxxxx.mp4?secure=NriB2E5ciJs0kKG1d3q7cmI/o
```


## 联系方式

https://t.me/crawler91

https://t.me/py91porn
