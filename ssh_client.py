#-*- coding: utf-8 -*-

#Author：陕晨阳

import paramiko
import threading

class ssh_client:
	def __init__(self,ip,username,passwd):
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(ip,22,username,passwd,timeout=5)

	def __del__(self):
		self.ssh.close()
		
	def shell(self,cmd):
		try:
			stdin, stdout, stderr = self.ssh.exec_command(cmd)
			#stdin.write("Y")   #简单交互，输入 ‘Y’ 
			out = stdout.readlines()
			for o in out:
				print o,
			print '%s\tCmd Exec OK\n'%(ip)
		except:
			print '%s\tCmd Exec Error\n'%(ip)

	def upfile(self,localpath, remotepath):
		try:
			sftp = self.ssh.open_sftp()
			sftp.put(localpath, remotepath)
			print '\n%s\t%s\tFileUp OK\n'%(ip,remotepath)
		except:
			print '\n%s\t%s\tFileUp Error\n'%(ip,remotepath)

	def downfile(self,remotepath, localpath):
		try:
			sftp = self.ssh.open_sftp()
			sftp.get(remotepath, localpath)
			print '\n%s\t%s\tFileDown OK\n'%(ip,localpath)
		except:
			print '\n%s\t%s\tFileDown Error\n'%(ip,localpath)
		
if __name__ == '__main__':
	ip = "192.168.1.230"
	username = "root"
	passwd = "123456"
	cmd = "ls -l /home/"
	localpath = "C:\Users\Admin-SCY\Desktop\scy.jpg"
	remotepath = "/home/scy/scy1.jpg"

	client = ssh_client(ip,username,passwd)
	client.upfile(localpath,remotepath)
	client.shell(cmd)
