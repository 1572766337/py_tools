#coding=utf8

# from autosqli import *

# f = open('urls.txt')
# for line in f:
# 	t = AutoSqli('http://127.0.0.1:8775', line)
# 	t.run()

import threading
from autosqli import *

f = open('urls.txt')
for line in f:
	t = threading.Thread(target=AutoSqli,args=('http://127.0.0.1:8775', line.strip()))
	t.start()