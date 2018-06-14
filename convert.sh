#!/bin/sh

./parse_rs.py rs.txt
./parse_digikey.py digikey.txt
./parse_mantech.py mantech.txt

libreoffice --convert-to xls *.csv

