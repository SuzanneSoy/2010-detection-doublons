#!/usr/bin/python

import sys
import os
import errno
import shutil

oldhash = ""
original = []
supprimable = []
nblines=0
for line in sys.stdin:
	nblines = (nblines+1)%500
	if nblines == 0:
		os.system("sync");
	hash = line[0:48]
	file = line[50:-1]
	if hash != oldhash:
		for o,s in zip(original,supprimable):
			sys.stdout.write(s+"\n"+o+"\0")
		supprimable = []
		original = []
	if file[0:2] == '1/': # Delete files in the directory named 1
		supprimable.append(file)
	else:
		original.append(file)
	
	oldhash = hash
