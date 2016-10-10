#!/usr/bin/env python2

import unicodecsv as csv
import sys
import os

input_filename = sys.argv[1]
output_filename = os.path.splitext(input_filename)[0] + ".csv"
csv_output_header = ['Unit price [ZAR]', 'Qty', 'TRX Part Number', 'Description']


def filter_cart_lines(lines):
    start = False
    for line in lines:
        if not start:
            if line == [u'Part No ', u'Image ', u'Minimum ', u'Multiple ', u'Availability ', u'Factory Lead Time ', u'Quantity ', u'Price Each ', u'Total (ZAR)']:
                start = True
        else:
            if line[0] == u'SUB TOTAL ':
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
            next(lines),
            next(lines)
        ]

        unit_price = float(item_lines[5][0])
        total_price = float(item_lines[5][1])
        quantity = int(round(total_price / unit_price))

        yield {
            'qty': quantity,
            'part number': item_lines[0][0],
            'description': item_lines[3][0],
            'unit price': unit_price,
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
