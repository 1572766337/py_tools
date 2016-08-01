#coding=utf8

partnums = int(raw_input('partnums:'))

fr = open('test.txt','r')
f_lst = [line for line in fr]
size = len(f_lst)/partnums
fr.seek(0)

for n in range(partnums):
	fw = open('dicts\part'+str(n)+'.txt','w')
	for i in range(size):
		fw.write(fr.readline())
	fw.close()
	
fr.close()