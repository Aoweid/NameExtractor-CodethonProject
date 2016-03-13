#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib, urllib2, httplib
import HTMLParser
import bs4
from bs4 import BeautifulSoup

# Facebook搜索用户的固定开头
search_url_header = "https://www.facebook.com/search/people/?q=key"
key="Ana"
url=search_url_header.replace('key',key.replace(' ','+'))


# 伪装成firefox客户端发送请求
headers={
	'User-Agent' : "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0"
}
req = urllib2.Request(url)
fetchback= urllib2.urlopen(req)
htmlpage=fetchback.read()

# 利用 BeautifulSoup 进行解析
soup=BeautifulSoup(htmlpage,"html5lib")
# 将html转移字符转换回原来字符
html_parser = HTMLParser.HTMLParser()
comment= html_parser.unescape(soup.code.string) # 有用信息在<code>标签下

target=BeautifulSoup(comment,"html5lib")
result=target.find_all("div",class_="_5d-5") # 人名被保存在<div class="_5d-5">标签里
match=0
for name in result:
	relname=name.string[:name.string.find('(')]
	if relname.lower().find(key.lower()) != -1:
		match+=1;
if match>0:
	print key+" is a name of human"
else:
	print key+" is not a name of human"
