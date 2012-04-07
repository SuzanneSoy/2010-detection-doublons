#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

def walk(path):
	#print >> sys.stderr, path
	emptydir = True
	for f in os.listdir(path):
		fpath = os.path.join(path, f)
		if (not os.path.islink(fpath)) and f[0:2] != ".%":
			if os.path.isfile(fpath):
				emptydir = False
			if os.path.isdir(fpath):
				emptysubdir = walk(fpath)
				emptydir = emptydir and emptysubdir
				if emptysubdir:
					dest = os.path.join(path, ".%%%s" % f)
					if not os.path.exists(dest):
						print "mv -i '%s' '%s'" % (fpath.replace("'", "'\\''"), dest.replace("'", "'\\''"))
						os.rename(fpath, dest)
	return emptydir

def help():
	print 'Usage : %s directory' % sys.argv[0]
	sys.exit(1)

if len(sys.argv) != 2:
	help()
for arg in sys.argv[1:]:
	if arg == '-h' or arg == '--help':
		help()

print "#!/bin/sh"
walk(sys.argv[1])
