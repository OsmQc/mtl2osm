#!/usr/bin/env python

"""
Take a CSV with geographical coordinates as input.
Outputs to the OpenStreetMap .osm file format.

Released under the MIT license: http://opensource.org/licenses/mit-license.php
Contains some code from https://github.com/pnorman/ogr2osm/

This program requires Python 2.7.
"""

import os
import sys
import csv
import argparse
import importlib

from lxml import etree

WGS84_PROJECTION = 'epsg:4326'
PROJECTION_CACHE = {}

class DefaultTranslator:
    def filterTags(self, attrs):
        """ return a dictionary that will make the tags of the node """
        return attrs

    def keepRow(self, row):
        """ return True to keep the row, False otherwise. """
        return True

class OsmId:
    _next = 0

    @classmethod
    def next_id(cls):
        cls._next = cls._next - 1
        return cls._next

def get_translator(filename):
    if not filename:
        return DefaultTranslator()

    # add dirs to path if necessary
    (root, ext) = os.path.splitext(filename)
    if os.path.exists(filename) and ext == '.py':
        # user supplied translation file directly
        sys.path.insert(0, os.path.dirname(root))
    else:
        # first check translations in the subdir translations of cwd
        sys.path.insert(0, os.path.join(os.getcwd(), "translations"))
        # then check subdir of script dir
        sys.path.insert(1, os.path.join(os.path.dirname(__file__), "translations"))
        # (the cwd will also be checked implicityly)

    # strip .py if present, as import wants just the module name
    if ext == '.py':
        filename = os.path.basename(root)

    try:
        imported_translator = __import__(filename, fromlist = [''])
    except SyntaxError as e:
        print "Syntax error in the translator module:"
        raise e
    except Exception as e:
        raise Exception("Could not load translator module '%s'. Translation "
               "script must be in your current directory, or in the "
               "translations/ subdirectory of your current or csv2osm.py "
               "directory. The following directories have been considered: %s"
               % (filename, str(sys.path)))

    translator = DefaultTranslator()
    for translation_method in ('filterTags', 'keepRow'):
        if hasattr(imported_translator, translation_method):
            setattr(translator, translation_method, getattr(imported_translator, translation_method))

    return translator

def read_csv(filename, dialect, encoding):
    with open(filename, 'rb') as csv_file:
        reader = csv.DictReader(csv_file, dialect=dialect)
        for row in reader:
            for key in row:
                row[key] = unicode(row[key], encoding)
            yield row

def text2float(text):
    return float(text.replace(',', '.'))

def get_proj(projection_string):
    global PROJECTION_CACHE
    if projection_string not in PROJECTION_CACHE:
        import pyproj
        PROJECTION_CACHE[projection_string] = pyproj.Proj(init=projection_string)
    return PROJECTION_CACHE[projection_string]

def get_lon_lat(row, longitude_field, latitude_field, source_projection):
    if longitude_field not in row:
        raise Exception("'%s' column not found in CSV file. Please use the --lat option to specify "
                        "the name of the column containing the longitude." % longitude_field)
    if latitude_field not in row:
        raise Exception("'%s' column not found in CSV file. Please use the --lat option to specify "
                        "the name of the column containing the latitude." % latitude_field)

    lon, lat = text2float(row[longitude_field]), text2float(row[latitude_field])

    if source_projection != WGS84_PROJECTION:
        srcproj = get_proj(source_projection)
        wgs84proj = get_proj(WGS84_PROJECTION)
        import pyproj
        lon, lat = pyproj.transform(srcproj, wgs84proj, lon, lat)

    # OpenStreetMap supports 7 decimal places
    lon, lat = round(lon, 7), round(lat, 7)
    return lon, lat

def generate_node_xml(row, args, translator):
    lon, lat = get_lon_lat(row, args.longitude_field, args.latitude_field, args.source_projection)
    xmlattrs = {
        'visible': 'true',
        'lon': str(lon),
        'lat': str(lat),
        'id': str(OsmId.next_id()),
    }
    node = etree.Element('node', xmlattrs)
    node_data = translator.filterTags(row)
    for key, value in node_data.iteritems():
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
    parser.add_argument('--src-proj', dest='source_projection', default=WGS84_PROJECTION,
        help='Projection of the latitude and longitude fields, defined '
             'according to PROJ.4 syntax. Only specify if the projection '
             'is not the standard GPS/WGS84 projection (defined in PROJ.4 as '
             '\'epsg:4326\'). In case of doubt, ignore this parameter. '
             'Requires the pyproj library.')
    parser.add_argument('--translator', help='Python file to import that '
        'contains special translation methods to transform the tags.')
    parser.add_argument('-f', '--force', dest='force_overwrite', action='store_true',
        help='Force overwriting the destination file.')
    return parser.parse_args()

def main():
    args = parse_args()
    if os.path.exists(args.output_file) and not args.force_overwrite:
        print >> sys.stderr, "%s already exists. Use -f to overwrite." % args.output_file
        sys.exit(1)
    translator = get_translator(args.translator)

    # Open up the output file with the system default buffering
    with open(args.output_file, 'w', -1) as output:
        output.write('<?xml version="1.0"?>\n<osm version="0.6" upload="false" generator="csv2osm">\n')
        for row in read_csv(args.csv_file, args.csv_dialect, args.csv_encoding):
            if not translator.keepRow(row):
                continue
            output.write(generate_node_xml(row, args, translator))
            output.write('\n')
        output.write('</osm>\n')

if __name__ == '__main__':
    main()
