#!/usr/bin/python

import sys
import os
import errno
import shutil

def identicalFiles(pathA, pathB):
	bufsize = 4096
	with open(pathA, 'rb') as a:
		with open(pathB, 'rb') as b:
			while True:
				dataA = a.read(bufsize)
				dataB = b.read(bufsize)
				if dataA != dataB:
					return False
				if not dataA:
					return True

oldhash = ""
original = ""
supprimable = []
nblines=0
for line in sys.stdin:
	nblines = (nblines+1)%500
	if nblines == 0:
		os.system("sync");
	hash = line[0:48]
	file = line[50:-1]
	if hash != oldhash:
		if original != "":
			for i in supprimable:
				print i
				if os.path.exists(i) and identicalFiles(original, i):
					destfile = "delete/" + i
					try:
						os.makedirs(os.path.dirname(destfile))
					except OSError as e:
						if e.errno == errno.EEXIST:
							pass
						else:
							raise
					shutil.move(i, destfile);
		supprimable = []
		original = ""
	if file[0:2] == 'd/': # Delete files in the directory named d
		supprimable.append(file)
	else:
		if original == "" and os.path.exists(file):
			original = file
	
	oldhash = hash
