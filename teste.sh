#!/usr/bin/sh
for arq in documentacao/*.sp3; do
    out=$(./simple3.sh "$arq")
    if [ ${#out} -gt 0 ]; then
	echo "Erro ao tentar compilar o arquivo" "$arq"
    fi
done
