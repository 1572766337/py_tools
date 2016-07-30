#coding=utf8

#Author：陕晨阳
#说明：为了进一步对某一站点进行深入挖掘，对其进行同ip扫描，可同时扫描多个站点的同ip网站
#用法：get_sameip_site.py filename

import re
import os
import sys
import urllib
import threading
from sgmllib import SGMLParser
import socket
socket.setdefaulttimeout(3)
mylock = threading.Lock()

class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []
    def start_a(self,attrs):
        href = [v for k,v in attrs if k=='href']
        if href:
            self.urls.extend(href)

class mythread(threading.Thread):
    def __init__(self,urllist):
        threading.Thread.__init__(self)
        self.urls = urllist
    def run(self):
        while len(self.urls)!=0:
            mylock.acquire()
            if len(self.urls)!=0:
                url = self.urls.pop()
            mylock.release()
            if len(self.urls)!=0:
                try:
                    get_sameip_site(url)
                except:
                    mylock.acquire()
                    print threading.currentThread().getName()+"\tFail: "+url
                    mylock.release()

reg = '<ul class="ResultListWrap">.+?</ul>'
regex = re.compile(reg,re.S)
reg_title = '<title>.+?</title>'
regex_title = re.compile(reg_title,re.S)
			
def gettitle(url):
	try:
		sock = urllib.urlopen(url)
		htmlsrc = sock.read()
		titles = re.findall(regex_title,htmlsrc)
		title = len(titles) and '' or titles[0]
		return title and '' or title[7:title.rfind('</title>')]
	except:
		return u'-->获取title出错'

cudir = sys.path[0]+os.sep

def get_sameip_site(url):
	#使用站长之家工具
	samesite = 'http://s.tool.chinaz.com/same?s='+url

	parser = URLLister()

	try:
		sitesock = urllib.urlopen(samesite)
		htmlsrc = sitesock.read()
		sitesock.close()
		
		urls = re.findall(regex,htmlsrc)
		
		parser.feed(urls[0])
		
		mylock.acquire()
		print threading.currentThread().getName()+"\tGET: "+url
		mylock.release()
		
		if len(parser.urls)>1:
			filename = cudir+folder+os.sep+url.split('/').pop().replace('\n','')+".txt"
			f = open(filename,'w')
			
			for suburl in parser.urls:
				f.write(suburl+'\n')
				#print suburl+'\t'+gettitle(suburl)
			f.close()	
			f = open(filename,'r')
			if len(f.read())==0:
				f.close()
				os.remove(filename)
	except:
		mylock.acquire()
		print threading.currentThread().getName()+"\tGET: "+url,
		print u'\t站长工具网出问题了'
		mylock.release()

def usage():
	print "\nUsage: "+sys.argv[0].split(os.sep).pop()+" [filename]"

def main():	
	if len(sys.argv)==1:
		usage()
	else:
		#定义文件保存目录
		global folder
		folder = 'samesite_'+sys.argv[1].split(os.sep).pop().split('.')[0]
		if not os.path.exists(folder):
			os.mkdir(folder)
		urls = []
		f = open(sys.argv[1])
		for line in f:
			url = line.replace('\n','')
			urls.append(url)
		for i in range(10):
			mythread(urls).start()
	
if __name__=='__main__':
	main()