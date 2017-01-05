#!/bin/sh

./parse_rs.py rs.txt
./parse_digikey.py digikey.txt

libreoffice --convert-to xls *.csv

