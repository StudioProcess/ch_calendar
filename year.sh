#!/usr/bin/env sh

if [[ -z $1 ]]; then
    echo "Usage: $0 <year>"
    exit 1
fi

python script.py $1 > out/$1.tex
pdflatex -output-directory=out out/$1.tex
