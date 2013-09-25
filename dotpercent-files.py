#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3

# Common functions

def removePrefix(fileName):
	while fileName[0:2] == ".%":
		fileName = fileName[2:]
	return fileName

def removePrefixPath(path):
	return '/'.join([removePrefix(component) for component in path.split('/')])

def prefixedExists(path):
	components = path.split('/')
	prefixedPaths = ('/'.join(components[0:i] + ['.%' + component for component in components[i:]]) for i in reversed(xrange(len(components))))
	return any((os.path.exists(prefixedPath) for prefixedPath in prefixedPaths))

# Code for this utility

prefix = '.%'

def help():
	print 'usage: %s database.db --vrac ./dbl/vrac-1 ./dbl/vrac-2 ./dbl/vrac-3 --tri ./dbl/tri-1 ./dbl/tri-2 ./dbl/tri-3' % sys.argv[0]
	sys.exit(1)

vracs = []
tris = []

db = sys.argv[1]

if len(sys.argv) < 6:
	help()

state=None
for arg in sys.argv[2:]:
	if arg == '-h' or arg == '--help':
		help()
	elif arg == '--vrac':
		state = "vrac"
	elif arg == '--tri':
		state = "tri"
	elif state == 'tri':
		if arg[-1:] == '/':
			tris.append(arg)
		else
			tris.append(arg + '/')
	elif state == 'vrac':
		if arg[-1:] == '/':
			vracs.append(arg)
		else
			vracs.append(arg + '/')
	else:
		help()

print 'vracs=%s' % ', '.join(vracs)
print 'tris=%s' % ', '.join(tris)

connection = sqlite3.connect(db)
connection.text_factory = str # For utf-8 file names…
cursor = connection.cursor()

cursor.execute("create temp table hashesVrac(id, hash);")
for path in vracs:
	likepath=('' + path).replace('%', '%%') + '%';
	cursor.execute("insert into hashesVrac select rowid,size||'#'||md5||'#'||sha1 from files where path like ?;", (likepath,))

cursor.execute("create temp table hashesTri(id, hash);")
for path in tris:
	likepath=('' + path).replace('%', '%%') + '%';
	cursor.execute("insert into hashesTri select rowid,size||'#'||md5||'#'||sha1 from files where path like ?;", (likepath,))

cursor.execute("create index i_hashesTri_hash on hashesTri(hash);")
cursor.execute("create index i_hashesVrac_hash on hashesVrac(hash);")

for fpath, in cursor.execute("select (select path from files where rowid == hashesVrac.id) as path from hashesVrac where hashesVrac.hash in (select hash from hashesTri);"):
	dest = '%s/%s%s' % (os.path.dirname(fpath), prefix, os.path.basename(fpath),)
	if prefixedExists(fpath) and not os.path.exists(fpath):
		pass # Already moved
	elif not os.path.exists(fpath):
		print "# Couldn't hide %s as %s: source doesn't exist" % (fpath, dest,)
		print "i-have-not-moved-because-no-source -i -- '%s' '%s'" % (fpath.replace("'", "'\\''"), dest.replace("'", "'\\''"),)
	elif os.path.exists(dest):
		print "# Couldn't hide %s as %s: destination exists" % (fpath, dest,)
		print "i-have-not-moved-because-dest-exists -i -- '%s' '%s'" % (fpath.replace("'", "'\\''"), dest.replace("'", "'\\''"),)
	else:
		print "i-have-moved -i -- '%s' '%s'" % (fpath.replace("'", "'\\''"), dest.replace("'", "'\\''"),)
		os.rename(fpath, dest)
