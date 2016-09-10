#coding=utf8

import re
import requests

# 设置谷哥语法（可修改）
keywords = u'inurl:gov 大同'
# 设置爬取页面数（可修改）
page_num = 10

# 常量及初始变量
url_search = 'http://www.baidu.com/s?wd='+keywords+'&pn='
reg_url = '<a.+class="c-showurl".+?</a>'
lst_url = []

# 爬取代码
for i in range(0,page_num*10,10):
	url = url_search + str(i)
	print url
	r = requests.get(url)
	txt = r.text.encode('utf-8')
	# 未处理的url
	lst_url_tmp = re.findall(reg_url,txt)
	# 处理url
	for url in lst_url_tmp:
		start = url.find('>') + 1
		end = url.rfind('<')
		url = url[start:end].replace('<b>','').replace('</b>','').replace('&nbsp;','').replace('...','')
		if url.find('/') != -1:
			url = 'http://' + url[0:url.find('/')+1]
		else:
			url = 'http://' + url
		try:
			lst_url.index(url)
		except:
			lst_url.append(url)

# 输出结果到文件
f = open('urls.txt','w')
for url in lst_url:
	f.write(url+'\n')
f.close()
