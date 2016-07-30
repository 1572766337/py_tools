#coding=utf8

#Author：陕晨阳
#说明：爬取固定页面深度(2)的url
#用法：get_site_urls url地址

import os
import sys
import urllib
from sgmllib import SGMLParser
import socket
socket.setdefaulttimeout(3)

class URLLister(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.urls = []
	def start_a(self,attrs):
		href = [v for k,v in attrs if k=='href']
		if href:
			self.urls.extend(href)

urlkeys=[]			
def getkeyurls(url):
	sock = urllib.urlopen(url)
	htmlSource = sock.read()
	sock.close()

	parser = URLLister()
	parser.feed(htmlSource)

	urls=[]
	for suburl in parser.urls:
		if suburl.startswith('http') or suburl.startswith('javascript') or suburl.startswith('#'):
			continue
		if not suburl.startswith('/'):
			suburl = '/'+suburl
		suburl = domain + suburl
		keyUrl = suburl.split('?')[0]
		try:
			urlkeys.index(keyUrl)
		except:
			urlkeys.append(keyUrl)
			urls.append(suburl)
			
	return urls

def get_urls_level2(domain):
	domain_urls = getkeyurls(domain)
	dict_urls = {}
	for url in domain_urls:
		dict_urls[url] = getkeyurls(url)
	return dict_urls

#输出的文件名称
filename = 'urls_level2.txt'	
def output2file(dict_urls):
	f = open(filename,'w')
	for k,v in dict_urls.items():
		f.write(k+'\n')
		print k
		for suburl in v:
			f.write(suburl+'\n')
			print suburl
		f.write('\n')
	f.close()
	f = open(filename,'r')
	if len(f.read())==0:
		f.close()
		os.remove(filename)
		
def main():
	if len(sys.argv)==1:
		print "\nUsage: "+sys.argv[0].split(os.sep).pop()+" [URL]"
	else:
		global domain
		domain = sys.argv[1]
		output2file(get_urls_level2(sys.argv[1]))
	
if __name__=='__main__':
	main()