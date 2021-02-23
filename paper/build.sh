#!/usr/local/bin/fish
pdflatex main
bibtext mybib
pdflatex main
cp main.pdf "main"(date "+%b%d")".pdf"
