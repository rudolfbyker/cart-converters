#!/usr/bin/env python2

import unicodecsv as csv
import sys
import os

input_filename = sys.argv[1]
output_filename = os.path.splitext(input_filename)[0] + ".csv"
csv_output_header = ['Unit price [USD]', 'Qty', 'DigiKey Part Number', 'Description']


def filter_cart_lines(lines):
    start = False
    for line in lines:
        if not start:
            if line == [u'Index', u'Quantity', u'Image', u'Part Number', u'Description', u'Customer Reference', u'Available Quantity', u'Backorder Quantity', u'Unit Price', u'Extended Price']:
                start = True
        else:
            if line[0] == u'' and line[1] == u'Subtotal':
                break
            else:
                yield line


def filter_cart_items(lines):

    while True:
        item_lines = [
            next(lines),
            next(lines),
            next(lines),
            next(lines),
            next(lines)
        ]

        yield {
            'qty': int(item_lines[2][1]),
            'part number': item_lines[1][2],
            'description': item_lines[1][3],
            'unit price': float(item_lines[4][1]),
        }


def main():

    with open(input_filename, 'rb') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        lines = filter_cart_lines(csv_reader)
        items = filter_cart_items(lines)
        output_lines = ([
                            item['unit price'],
                            item['qty'],
                            item['part number'],
                            item['description'],
                        ] for item in items)

        with open(output_filename, 'wb') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(csv_output_header)
            csv_writer.writerows(output_lines)


if __name__ == "__main__":
    main()
