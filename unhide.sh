#!/bin/bash

find "$@" -depth -name '.%*' | while read ab; do aa="${ab##*/}"; mv -i "$ab" "${ab%/*}/${aa#.%}"; echo -n .; done
