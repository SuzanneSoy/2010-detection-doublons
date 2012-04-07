#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

def walk(path):
	#print >> sys.stderr, path
	for f in os.listdir(path):
		fpath = os.path.join(path, f)
		if f[0:2] == ".%":
			ff = f
			while ff[0:2] == ".%":
				ff = ff[2:]
			dest = os.path.join(path, ff)
			if not os.path.exists(dest):
				print "i-have-moved -i '%s' '%s'" % (fpath.replace("'", "'\\''"), dest.replace("'", "'\\''"))
				os.rename(fpath, dest)
		if os.path.isdir(fpath) and not os.path.islink(fpath):
			walk(fpath)
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
