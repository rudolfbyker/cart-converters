#!/usr/bin/env python

import unicodecsv as csv
import sys
import os

input_filename = sys.argv[1]
output_filename = os.path.splitext(input_filename)[0] + ".csv"
csv_output_header = ['Unit price', 'Qty', 'Mantech Stock Code', 'Part Number', 'Description']

def filter_cart_lines(lines):
    start = False
    for line in lines:
        if not start:
            if line == [u'Remove', u'Stock Code', u'Qty', u'Part Number', u'Description', u'Sold In', u'Unit Price', u'Priced Per', u'Total']:
                start = True
        else:
            if line == [u'', u'Delivery Charge ', u'TBA']:
                break
            else:
                yield line

def filter_cart_items(lines):
    for line in lines:
        if len(line) == 9:
            
            unitprice = float(line[6][1:])
            total = float(line[8][1:])
            qty = int(round(total / unitprice))
            
            yield {
                'stock code':   line[1],
                'qty':          qty,
                'part number':  line[3],
                'description':  line[4],
                'sold in':      line[5],
                'unit price':   unitprice,
                'priced per':   line[7],
                'total':        total,
            }


with open(input_filename, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    lines = filter_cart_lines(csvreader)
    items = filter_cart_items(lines)
    output_lines = ([
        item['unit price'],
        item['qty'],
        item['stock code'],
        item['part number'],
        item['description'],
    ] for item in items)
   
    with open(output_filename, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(csv_output_header)
        csvwriter.writerows(output_lines)

