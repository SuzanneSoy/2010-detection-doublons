#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# Common functions

def removePrefix(fileName):
	while fileName[0:2] == ".%":
		fileName = fileName[2:]
	return fileName

# Code for this utility

def walk(path):
	#print >> sys.stderr, path
	for f in os.listdir(path):
		fpath = os.path.join(path, f)
		if os.path.isdir(fpath) and not os.path.islink(fpath):
			walk(fpath)
		if f[0:2] == ".%":
			dest = os.path.join(path, removePrefix(f))
			if not os.path.exists(dest):
				print "i-have-moved -i -- '%s' '%s'" % (fpath.replace("'", "'\\''"), dest.replace("'", "'\\''"))
				os.rename(fpath, dest)

def help():
	print 'Usage : %s directory > "undo-unhide-dotpercent-$(date).sh"' % sys.argv[0]
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
