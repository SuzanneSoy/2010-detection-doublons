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
						print "i-have-moved -i -- '%s' '%s'" % (fpath.replace("'", "'\\''"), dest.replace("'", "'\\''"))
						os.rename(fpath, dest)
	return emptydir

def help():
	print 'Usage : %s directory > "undo-dotpercent-dirs-$(date).sh"' % sys.argv[0]
	sys.exit(1)

if len(sys.argv) != 2:
	help()
for arg in sys.argv[1:]:
	if arg == '-h' or arg == '--help':
		help()

print "#!/bin/sh"
print "echo 'Redefine the i-have-moved command at the beginning of this script to undo, e.g.:'"
print "echo 'i-have-moved() { mv -i -- \"$4\" \"$3\"; }'"
walk(sys.argv[1])
