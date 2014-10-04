#!/usr/bin/env python

"""
Take a CSV with geographical coordinates as input.
Outputs to the OpenStreetMap .osm file format.

Released under the MIT license: http://opensource.org/licenses/mit-license.php
Somewhat inspired from https://github.com/pnorman/ogr2osm/

This program requires Python 2.7.
"""

import csv
import argparse

from lxml import etree

class OsmId:
    _next = 0

    @classmethod
    def next_id(cls):
        cls._next = cls._next - 1
        return cls._next

def read_csv(filename, dialect, encoding):
    with open(filename, 'rb') as csv_file:
        reader = csv.DictReader(csv_file, dialect=dialect)
        for row in reader:
            for key in row:
                row[key] = unicode(row[key], encoding)
            yield row

def get_lon_lat(row, longitude_field, latitude_field):
    if longitude_field not in row:
        raise Exception("'%s' column not found in CSV file. Please use the --lat option to specify "
                        "the name of the column containing the longitude." % longitude_field)
    if latitude_field not in row:
        raise Exception("'%s' column not found in CSV file. Please use the --lat option to specify "
                        "the name of the column containing the latitude." % latitude_field)
    return row[longitude_field], row[latitude_field]

def generate_node_xml(row, longitude_field, latitude_field):
    lon, lat = get_lon_lat(row, longitude_field, latitude_field)
    xmlattrs = {
        'visible': 'true',
        'lon': str(lon),
        'lat': str(lat),
        'id': str(OsmId.next_id()),
    }
    node = etree.Element('node', xmlattrs)
    for key, value in row.iteritems():
        tag = etree.Element('tag', {'k':key, 'v':value})
        node.append(tag)
    return etree.tostring(node)

def parse_args():
    parser = argparse.ArgumentParser(description='Converts a CSV file to an OSM file')
    parser.add_argument('csv_file', help='CSV file to read')
    parser.add_argument('output_file', help='Output file name')
    parser.add_argument('--csv-dialect', default='excel',
        help='The csv dialect, i.e. the algorithm used to interpret the textual data. '
             'Can be one of: ' + ', '.join(csv.list_dialects()))
    parser.add_argument('--csv-encoding', default='utf-8',
            help='Character encoding of the CSV file. Examples: utf-8, latin1')
    parser.add_argument('--lon', dest='longitude_field', default='longitude',
        help='Name of the field that contains the longitude')
    parser.add_argument('--lat', dest='latitude_field', default='latitude',
        help='Name of the field that contains the latitude')
    #parser.add_argument('--translation', help='Python file to import that '
    #    'contains special translation methods to transform the tags.')
    return parser.parse_args()

def main():
    args = parse_args()

    # Open up the output file with the system default buffering
    with open(args.output_file, 'w', -1) as output:
        output.write('<?xml version="1.0"?>\n<osm version="0.6" upload="false" generator="csv2osm">\n')
        for row in read_csv(args.csv_file, args.csv_dialect, args.csv_encoding):
            output.write(generate_node_xml(row, args.longitude_field, args.latitude_field))
            output.write('\n')
        output.write('</osm>\n')

if __name__ == '__main__':
    main()
