#coding=utf8

from autosqli import *

f = open('urls.txt')
for line in f:
	t = AutoSqli('http://127.0.0.1:8775', line)
	t.run()
