#!/usr/bin/python

import hashlib;
import sys;

for size in sys.stdin:
	file = sys.stdin.next()
	print "%16.16x%s" % (int(size), hashlib.md5(open(file[:-1], 'r').read(512)).hexdigest()),
	print " " + file,

#!/bin/sh
#
#find "$@" -type f -printf "%s  %p\n" | while read ab; do
#	sum="$(printf %16.16x "${ab%%  *}")"
#	nom="${ab#*  }"
#	mdsum="$(dd if="$nom" bs=512 count=1 2>/dev/null | md5sum 2>/dev/null)"
#	mdsum="${mdsum%%  *}"
#	sum="$sum$mdsum"
#	if [ "${#sum}" != "48" ]; then
#		echo "ERROR : $sum $nom" >&2
#		sum="0000000000000000000000000000000000000000"
#	fi
#	echo "$sum  $nom"
#done
