#!/bin/bash

if [ -z "$1" -o "$1" == "--help" -o "$1" == "-h" ]; then
        cat <<EOF
Affiche les fichiers qui SONT des doublons, sous forme d'un script
  permettant leur suppression.
Pour afficher les fichiers qui ne sont pas des doublons, utilisez
  showunique.

Syntaxe : remdoubles dossier-où-chercher-les-doublons < md5sums

Exemple :
  md5sums contient :
    604c442629170d4bee5804b13e9a587f  ./a/fichier_un
    a3d0c4f97abec8c2ceaaf83020f00809  ./b/fichier_deux
    a3d0c4f97abec8c2ceaaf83020f00809  ./b/fichier_trois
    604c442629170d4bee5804b13e9a587f  ./b/fichier_XYZ
  Si on lance "remdoubles ./b/ < md5sums", il affichera
    #!/bin/sh
    
    echo Si vous lancez ce script, il supprimera un grand nombre de fichiers dans ./b/ .
    exit
    
    rm './b/fichier_XYZ'
  car il est dans ./b/, ET a un fichier identique ailleurs que
  dans ./b/ .
  Il n'affichera pas ./a/fichier_un car il n'est pas dans ./b/
  Il n'affichera pas ./b/fichier_deux ni ./b/fichier_trois car
  ils n'ont pas de doublons en dehors de ./b/ .
EOF
	exit 1
fi

echo "#!/bin/sh"
echo ""

oldsum=""
unset supprimable
n=0
orig=""
q="'\\''" # escaped quote.
#sort | \
while read ab; do
	sum="${ab%%  *}"
	nom="${ab#*  }"
	if [ "$sum" != "$oldsum" ]; then
		if [ -n "$orig" ]; then
			for i in "${supprimable[@]}"; do
				if true; then # diff -q "$orig" "$i" > /dev/null; then
					qi="${i//\'/$q}"
					echo "mv -i '$qi' '${qi%/*}/.%${qi##*/}' # '${orig//\'/$q}'"
				fi
			done
		fi
		
		unset supprimable
		orig=""
		n=0
	fi
	
	if [ "${nom#$1}" != "$nom" ]; then
		supprimable[n]="$nom"
		n=$(($n+1))
	else
		orig="$nom"
	fi
	
	oldsum="$sum"
done