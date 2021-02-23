#!/usr/bin/bash
pdflatex main
bibtex main.aux
pdflatex main
cp main.pdf $(date "+main%b%d.pdf")
