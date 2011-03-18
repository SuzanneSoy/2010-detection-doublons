#!/bin/bash

find "$@" -depth -name '.%*' -printf '%h\n%f\n' | ./unhide.py
