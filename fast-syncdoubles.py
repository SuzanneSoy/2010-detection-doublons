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

nblines=0
for supprimable in sys.stdin:
	nblines = (nblines+1)%10240
	if nblines == 0:
		os.system("sync");
	original = sys.stdin.next()
	supprimable = supprimable[0:-1]
	original = original[0:-1]
	if supprimable[0:2] == '1/' and os.path.exists(supprimable) and os.path.exists(original) and identicalFiles(original, supprimable):
		destfile = "sync/" + original
		if not os.path.exists(destfile):
			try:
				os.makedirs(os.path.dirname(destfile))
			except OSError as e:
				if e.errno == errno.EEXIST:
					pass
				else:
					raise
			shutil.move(supprimable, destfile);
