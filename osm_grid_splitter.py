import sys
import json

from lxml import etree
from shapely import geometry

def get_xml_nodes(osm_filename):
    for event, element in etree.iterparse(open(osm_filename, 'r')):
        # Work around Launchpad bug #1185701 by bailing out after the end of the document root.
        if element.getparent() is None:
            break
        if element.tag != 'node':
            continue
        yield element

if __name__ == '__main__':
    osm_filename = sys.argv[1]
    json_filename = sys.argv[2]

    # Load the grid generated from the HOT task manager
    hot_json_grid = json.load(open(json_filename))

    # Transform each square of the grid into a shape with which we can
    # intersect the points from the OSM file
    grid = [(feature, geometry.shape(feature['geometry'])) for feature in hot_json_grid['features']]

    # A dictionary to "classify" each OSM points into each grid
    result = {}

    for xmlnode in get_xml_nodes(osm_filename):
        lon = float(xmlnode.get('lon'))
        lat = float(xmlnode.get('lat'))
        point = geometry.Point(lon, lat)
        for json_feature, square_shape in grid:
            if square_shape.intersects(point):
                result.setdefault(json_feature['id'], []).append(xmlnode)

    for grid_id, xmlnodes in result.iteritems():
        with open('out_%s.osm' % grid_id, 'wb') as output:
            output.write('<?xml version="1.0"?>\n<osm version="0.6" upload="false" generator="osm_grid_splitter">\n')
            osmid = -1
            for xmlnode in xmlnodes:
                xmlnode.set('id', str(osmid))
                output.write(etree.tostring(xmlnode))
                osmid = osmid - 1
            output.write('</osm>\n')
