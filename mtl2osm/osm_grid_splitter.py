"""
A program to split a .osm file based on a grid provided in GeoJSON format.

Copyright 2014 Guillaume Pratte <guillaume@guillaumepratte.net>
Copyright 2014 Mathieu Leduc-Hamel <mathieu@mlhamel.org>

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

import os
import json

from collections import defaultdict
from argparse import ArgumentParser

from lxml import etree
from shapely import geometry


def get_xml_nodes(osm_filename, node_type="node"):
    for event, element in etree.iterparse(open(osm_filename, 'r')):
        # Work around Launchpad bug #1185701 by bailing out after the
        # end of the document root.
        if element.getparent() is None:
            break
        if element.tag != node_type:
            continue
        yield element


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("osm", help="OSM filename as input")
    parser.add_argument("grid", help="Grid of reference")
    parser.add_argument("outbasedir", help="Output directory")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Verbose display")
    return parser.parse_args()


def main():
    args = parse_args()

    # Dictionaries to "classify" each OSM points into each grid
    points = {}
    ways = defaultdict(list)
    nodes = defaultdict(list)

    # An index of the JSON grid features
    json_feature_index = {}

    # Load the grid generated from the HOT Tasking Manager
    hot_json_grid = json.load(open(args.grid))

    grid = []
    for feature in hot_json_grid['features']:
        # Pre-emptively transform each square of the grid into a shape
        # with which we can intersect the points from the OSM file.
        # This is an optimization to avoid creating shapes
        # in a O(n^2) loop.
        grid.append((feature, geometry.shape(feature['geometry'])))

        # Index each feature by its id
        json_feature_index[feature['id']] = feature

    # Intersect the points from the .osm file with the JSON grid
    for xmlnode in get_xml_nodes(args.osm):
        lon = float(xmlnode.get('lon'))
        lat = float(xmlnode.get('lat'))
        point = geometry.Point(lon, lat)
        points[xmlnode.get("id")] = point
        for json_feature, square_shape in grid:
            if square_shape.intersects(point):
                nodes[json_feature['id']].append(xmlnode)

    # Intersect the points from the .osm file with the JSON grid
    for xmlnode in get_xml_nodes(args.osm, node_type="way"):
        for node in xmlnode.getchildren():
            if node.tag != "nd":
                continue
            point = points[node.get("ref")]
            for json_feature, square_shape in grid:
                if square_shape.intersects(point):
                    ways[json_feature['id']].append(xmlnode)

    # Write the set of .osm files, one per grid element
    for json_feature, square_shape in grid:
        prop = json_feature['properties']
        outdir = '%s/%s' % (prop['zoom'], prop['x'])
        outdir = os.path.join(args.outbasedir, outdir)
        outfile = '%s/%s.osm' % (outdir, prop['y'])
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        with open(outfile, 'wb') as output:
            output.write('<?xml version="1.0"?>\n<osm version="0.6" upload="false" generator="osm_grid_splitter">\n')  # noqa
            # Write the boundaries of the .osm file to help JOSM properly display the data
            # shapely.geometry.Point.bounds is a tuple (minx, miny, maxx, maxy)
            # In this script we have mapped x to the longitude and y to the lattitude
            output.write('<bounds minlon="%s" minlat="%s" maxlon="%s" maxlat="%s"/>\n' % square_shape.bounds)  # noqa
            for xmlnode in nodes[json_feature['id']]:
                output.write(etree.tostring(xmlnode))
            for xmlnode in ways[json_feature['id']]:
                output.write(etree.tostring(xmlnode))
            output.write('</osm>\n')


if __name__ == '__main__':
    main()
