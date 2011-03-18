#!/usr/bin/python

import shutil;
import sys;

for dir in sys.stdin:
	file = sys.stdin.next()
	if file[0:2] == ".%":
		dir = dir[:-1]
		file = file[:-1]
		shutil.move(dir + '/' + file, dir + '/' + file[2:])
		print "",
