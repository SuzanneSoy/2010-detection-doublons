#!/bin/sh
./pre-fast-remdoubles.py | sort -z | tr '\0' '\n'
