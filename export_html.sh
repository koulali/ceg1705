#!/bin/bash

prac=$1

jupyter nbconvert --to html ceg1705_ceg2719_practical${prac}.ipynb --HTMLExporter.theme=dark
