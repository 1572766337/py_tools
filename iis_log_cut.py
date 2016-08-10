#coding=utf8

#iis日志分割工具，辅助分析日志
#分割结果以%ip%.txt格式保存在log_part目录下

import os
import re
import time
reg_ip = ' [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} '

folder = 'log_part'
os.path.exists(folder) or os.mkdir(folder)

dic_ips = {}
f = open('ex160727.log')

print u'正在收集ip，请稍后...'
start = time.time()
for line in f:
	ips = re.findall(reg_ip,line)
	if len(ips) < 2: continue
	ip = ips[1].strip()
	if not dic_ips.has_key(ip):
		dic_ips[ip] = []
	dic_ips[ip].append(line)
f.close()
end = time.time()
get_ip_time = end - start

print u'正在导出每个ip日志到文件，请稍后...'
start = time.time()
for k,v in dic_ips.items():
	f = open(folder + os.sep + k + '.log','w')
	for line in v:
		f.write(line)
	f.close()
end = time.time()
output_time = end - start
print u'处理完毕！\n获取ip耗时：%d秒\n导出ip耗时：%d秒' % (get_ip_time,output_time)