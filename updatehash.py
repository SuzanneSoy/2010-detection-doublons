#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import os
import sqlite3
import time

def checksumFile(path):
	md5 = hashlib.md5()
	sha1 = hashlib.sha1()
	with open(path,'rb') as f: 
		while True:
			chunk = f.read(2*md5.block_size*sha1.block_size)
			if not chunk:
				return {'md5':md5.hexdigest(), 'sha1':sha1.hexdigest()}
			md5.update(chunk)
			sha1.update(chunk)

def fileInfo(path):
	stat = os.stat(path)
	return {'mtime':stat.st_mtime, 'size':stat.st_size}

def initdb(cursor):
	cursor.execute("create table if not exists files(tag,path primary key,md5,sha1,mtime,size)")
	cursor.execute("create index if not exists i_files_tag on files(tag)")
	cursor.execute("create index if not exists i_files_path_md5_sha1 on files(path,md5,sha1)")

def cacheFileInfo(cursor, path):
	cursor.execute('select mtime,size from files where path = ?', (path,))
	data = cursor.fetchone()
	return data and {'mtime':data[0], 'size':data[1]}

def update(connection,cursor,path):
	currentTime = time.clock()
	lastTime = currentTime
	for d in os.walk(path):
		dirpath=d[0]
		for f in d[2]:
			fpath = os.path.join(dirpath, f)
			if os.path.isfile(fpath):
				fi = fileInfo(fpath)
				cfi = cacheFileInfo(cursor,fpath)
				if fi != cfi:
					print " updating", fpath
					md5,sha1 = checksumFile(fpath)
					values = ('no tag',fpath,md5,sha1,fi['mtime'],fi['size'])
					cursor.execute("insert or replace into files(tag,path,md5,sha1,mtime,size) values(?,?,?,?,?,?)", values)
					
					currentTime = time.clock()
					if abs(lastTime-currentTime) >= 0.1:
						lastTime = currentTime
						connection.commit()
						print "commit!"

def walk(db,path):
	connection = sqlite3.connect(db)
	connection.text_factory = str # For utf-8 file names…
	cursor = connection.cursor()
	initdb(cursor)
	update(connection, cursor, path)
	connection.commit()
	cursor.close()

walk('/tmp/files','/home/js')
