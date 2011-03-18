#!/bin/zsh

# masque les dossiers qui ne contiennent que des fichiers dont le nom est
# .%fichier, récursivement (les dossiers sont masqués en préfixant ".%" à
# leur nom, donc les dossiers ne contenant que des fichiers / dossiers
# masqués le seront eux aussi.
# Un dossier n'est pas masqué ssi il contient au moins un fichier
# (regular file) ou dossier non masqué.

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
	for x in *(/,.NoN); do # N = pas d'erreur quand vide, oN = order none, / = dossiers, . = fichiers
		if [ "${x[0,2]}" != ".%" ]; then
			pseudo_empty="0"
			break;
		fi
	done
	cd ..
	[ "$pseudo_empty" = "1" ] && [ "${1[0,2]}" != ".%" ] && mv -i -- "$1" ".%$1"
}

dohide .
