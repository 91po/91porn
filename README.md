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

今日口令（每日21:00更新 ）**Ef3OJ**, 时效:1天, 总次数:1000

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
| category | 列表种类 ：rf-精华 tf-本月最热 空字符串-所有视频 | 否   | String |
| page     | 页码                                             | 是   | int    |

### 响应参数

| 参数        | 描述                     | 必有 | 类型          |
| ----------- | ------------------------ | ---- | ------------- |
| totalPage   | 总页数                   | 是   | String        |
| currentPage | 当前页                   | 是   | String        |
| category    | 回显列表种类字段         | 是   | String        |
| list        | 视频列表，object格式见下 | 是   | Array[Object] |

list object结构,如下：

| 参数       | 描述        | 必有 | 类型   |
| ---------- | ----------- | ---- | ------ |
| viewkey    | 视频viewkey | 是   | String |
| title      | 视频标题    | 是   | String |
| pic        | 封面图片URL | 是   | String |
| duration   | 视频时长    | 是   | String |
| loadtime   | 上传日期    | 否   | Int |
| authorName | 作者名字    | 是   | String |

### 请求示例

```
https://91api.org/api/list?category=&page=1
```

### 响应示例


```
{
	"success": 1,
	"data": {
		"key": "1rf",
		"list": [{
			"viewkey": "c8cf551c39e0421239a2",
			"title": "标题示例1",
			"pic": "http://img.t6k.co/thumb/1_357370.jpg",
			"duration": "00:03:55",
			"loadtime": 1706785428,
			"authorName": "作者名字1"
		}, {
			"viewkey": "406e4a6c648a881a81d0",
			"title": "标题示例2",
			"pic": "http://img.t6k.co/thumb/1_357369.jpg",
			"duration": "00:03:55",
			"loadtime": 1706785428,
			"authorName": "作者名字2"
		}],
		"totalPage": "146",
		"currentPage": "1",
		"category": "rf"
	}
}
```


## 联系方式

https://t.me/crawler91

https://t.me/py91porn
