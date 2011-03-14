#!/bin/sh

find "$@" -type f -printf "%s\n%p\n" | ./quickhash.py
