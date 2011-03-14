#!/bin/zsh

setopt dotglob

dohide() {
	local x pseudo_empty subdirs si
	echo "[$1] $PWD"
	cd "./$1"
	pseudo_empty="1"
	si=1
	subdirs=()
	for x in *(N/); do
		if [ "${x[0,2]}" != ".%" ]; then
			subdirs[si]="$x"
			si=$(($si+1))
		fi
	done
	while [ $si -gt 1 ]; do
		si=$(($si-1))
		dohide "${subdirs[si]}"
	done
	for x in *(N); do
		if [ "${x[0,2]}" != ".%" ]; then
			pseudo_empty="0"
			break;
		fi
	done
	cd ..
	[ "$pseudo_empty" = "1" ] && [ "${1[0,2]}" != ".%" ] && mv -i -- "$1" ".%$1"
}

dohide .
