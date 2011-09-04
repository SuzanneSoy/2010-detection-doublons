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
original = []
supprimable = []
for line in sys.stdin:
	hash = line[0:48]
	file = line[50:-1]
	if hash != oldhash:
		if original != []:
			for i in supprimable:
				if os.path.exists(i):
					for j in original:
						if os.path.exists(i) and os.path.exists(j) and identicalFiles(j, i):
							print i + " |||||||||| " + j
							destfile = "delete/" + i
							try:
								os.makedirs(os.path.dirname(destfile))
							except OSError as e:
								if e.errno == errno.EEXIST:
									pass
								else:
									raise
							shutil.move(i, destfile);
							break
		supprimable = []
		original = []
	if file[0:2] == '1/': # Delete files in the directory named 1
		supprimable.append(file)
	else:
		original.append(file)
	
	oldhash = hash
