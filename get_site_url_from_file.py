#encoding=utf-8

#说明：多线程爬取文件列表网站页面中的url。
#工作中有一段时间做渗透测试，需要查找被挂黑链的网站，同时获取动态链接，为下一步sql注入收集url
#用法：getsiteurl ip列表文件

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
                    getUrls(url)
                except:
                    mylock.acquire()
                    print threading.currentThread().getName()+"\tFail: "+url
                    mylock.release()

def getUrls(url):
    
    sock = urllib.urlopen(url)
    htmlSource = sock.read()
    sock.close()

    parser = URLLister()
    parser.feed(htmlSource)

	# 判断第一级页面是否暗链
    anlian = ""
#    if htmlSource.find('赌博')!=-1 or htmlSource.find('博彩')!=-1:
#        anlian = u"疑似暗恋"
    mylock.acquire()
    print threading.currentThread().getName()+"\tGET: "+url+"\t"+anlian
    mylock.release()
    filename = cudir+folder+os.sep+url.split('/').pop().replace('\n','')+".txt"
    f = open(filename,'w')

    urlList = []

	# 提取有用的链接并处理
    for suburl in parser.urls:
        if suburl.find('=') != -1:
            if suburl.startswith('/') or suburl.startswith('.'):
                suburl = url+suburl
            elif not suburl.startswith('http://'):
                suburl = url+'/'+suburl
            keyUrl = suburl.split('?')[0]
            try:
                urlList.index(keyUrl)
            except:
                urlList.append(keyUrl)
                f.write(suburl+'\n')
                
    f.close()

    f = open(filename,'r')
    if len(f.read())==0:
        f.close()
        os.remove(filename)
    
cudir = sys.path[0]+os.sep

if len(sys.argv)==1:
    print "\nUsage: "+sys.argv[0].split(os.sep).pop()+" [filename]"
else:
    global folder
    folder = 'params_'+sys.argv[1].split(os.sep).pop().split('.')[0]
    if not os.path.exists(folder):
        os.mkdir(folder)
    urls = []
    f = open(sys.argv[1])
    for line in f:
        url = line.replace('\n','')
        urls.append(url)
    for i in range(10):
        mythread(urls).start()
