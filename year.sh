#!/usr/bin/env sh

OUT=out

if [[ -z $1 ]]; then
    echo "Usage: $0 <year>"
    exit 1
fi

mkdir -p $OUT
python script.py $1 > $OUT/$1.tex
pdflatex -output-directory=$OUT $OUT/$1.tex

# remove aux and log files
rm -f $OUT/$1.log $OUT/$1.aux
