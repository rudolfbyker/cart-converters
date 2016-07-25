#!/usr/bin/env python

import sys
import os
import unicodecsv as csv

input_filename = sys.argv[1]
output_filename = os.path.splitext(input_filename)[0] + ".csv"
start = False
lines = []
items = []
header = [
    "Unit price",
    "Qty",
    "Yebo product code",
    "Yebo item name",
]

with open(input_filename, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    for line in csvreader:
        
        line = [l.strip() for l in line if len(l.strip())]
        
        if len(line) and "Sub-Total:" in line[0]:
            start = False
        
        if start and len(line):
            lines.append(line)

        # First line looks like this:
        # Qty. 	  	Item Name 	Unit 	Total 	 
        
        elif [u'Qty.', u'Item Name', u'Unit', u'Total'] == line:
            start = True


for i in range(len(lines)):
    if len(lines[i]) == 1 and len(lines[i+1]) == 3:
        unitprice = float(lines[i+1][0][1:])
        quantity = int(round(float(lines[i+1][1][1:]) / unitprice))
        name = lines[i][0][:len(lines[i][0]) / 2]
        code = name[-7:-1]
        
        item = [unitprice, quantity, code, name[:-8]]
        items.append(item)

with open(output_filename, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(items)


