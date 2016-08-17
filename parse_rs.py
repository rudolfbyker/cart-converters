#!/usr/bin/env python2

import unicodecsv as csv
import sys
import os
import re

input_filename = sys.argv[1]
output_filename = os.path.splitext(input_filename)[0] + ".csv"
csv_output_header = [
    "Unit price",
    "Qty",
    "RS Stock No.",
    "Manufacturer Part Number",
    "Manufacturer",
    "Description",
]
regex_item = re.compile(r"(?P<description>.+)\nRS stock no. (?P<stock_no>[\d-]+)\n(?P<manufacturer>.+)\nMfr. Part No. (?P<manufacturer_part_number>.+)\n(.*\n)*?R (?P<unit_price>[\d.]+)\n(.*\n)*?R (?P<total_price>[\d.]+)\n", re.MULTILINE | re.IGNORECASE)

def main():

    with open(input_filename, 'rb') as in_file:
        in_text = in_file.read()

    csv_output_lines = []
    for match in regex_item.finditer(in_text):
        item = match.groupdict()
        unit_price = float(item['unit_price'])
        total_price = float(item['total_price'])
        quantity = int(round(total_price / unit_price))
        csv_output_lines.append([
            unit_price,
            quantity,
            item['stock_no'],
            item['manufacturer_part_number'],
            item['manufacturer'],
            item['description']
        ])

    with open(output_filename, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_output_header)
        csv_writer.writerows(csv_output_lines)


if __name__ == "__main__":
    main()
