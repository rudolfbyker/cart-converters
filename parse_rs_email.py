#!/usr/bin/env python2

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
    "RS Stock No.",
    "Manufacturer Part Number",
    "Manufacturer",
    "Description",
]

with open(input_filename, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    for line in csvreader:
        
        line = [l.strip() for l in line]
        
        if start:
            lines.append(line)
        
        elif "RS Stock No." in line and len(line) == 9:
            start = True


for i in range(len(lines)):
    if len(lines[i]) == 7 and len(lines[i+1]) == 2 and len(lines[i+2]) == 3:
        item = [
            lines[i+2][1],  # Unit price
            lines[i][0],    # Qty
            lines[i][1],    # RS Stock No.
            lines[i][2],    # Manufacturer Part Number
            lines[i][3],    # Manufacturer
            lines[i][5],    # Description
        ]
        items.append(item)

with open(output_filename, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(items)


