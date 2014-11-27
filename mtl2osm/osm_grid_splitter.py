"""
A program to split a .osm file based on a grid provided in GeoJSON format.

Copyright 2014 Guillaume Pratte <guillaume@guillaumepratte.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json

from argparse import ArgumentParser

from lxml import etree
from shapely import geometry


def get_xml_nodes(osm_filename):
    for event, element in etree.iterparse(open(osm_filename, 'r')):
        # Work around Launchpad bug #1185701 by bailing out after the
        # end of the document root.
        if element.getparent() is None:
            break
        if element.tag != 'node':
            continue
        yield element


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("osm", help="OSM filename as input")
    parser.add_argument("grid", help="Grid of reference")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Verbose display")
    return parser.parse_args()


def main():
    args = parse_args()

    # Load the grid generated from the HOT task manager
    hot_json_grid = json.load(open(args.grid))

    # Transform each square of the grid into a shape with which we can
    # intersect the points from the OSM file
    grid = [(feature, geometry.shape(feature['geometry'])) for feature in
            hot_json_grid['features']]

    # A dictionary to "classify" each OSM points into each grid
    result = {}

    # Intersect the points from the .osm file with the JSON grid
    for xmlnode in get_xml_nodes(args.osm):
        lon = float(xmlnode.get('lon'))
        lat = float(xmlnode.get('lat'))
        point = geometry.Point(lon, lat)
        for json_feature, square_shape in grid:
            if square_shape.intersects(point):
                result.setdefault(json_feature['id'], []).append(xmlnode)

    # Write the set of .osm files, one per grid element
    for grid_id, xmlnodes in result.iteritems():
        with open('out_%s.osm' % grid_id, 'wb') as output:
            output.write('<?xml version="1.0"?>\n<osm version="0.6" upload="false" generator="osm_grid_splitter">\n')  # noqa
            # We need to reinitialize the id for each .osm file
            osmid = -1
            for xmlnode in xmlnodes:
                xmlnode.set('id', str(osmid))
                output.write(etree.tostring(xmlnode))
                osmid = osmid - 1
            output.write('</osm>\n')


if __name__ == '__main__':
    main()
