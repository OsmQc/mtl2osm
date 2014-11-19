import fiona
from shapely.geometry import shape, mapping

grid = fiona.open('data/hot_osmtm_619.json', 'r')
print grid

from rtree import index
idx = index.Index()

gns = fiona.open('data/gns_sierra_leone_2014_06_14_sl_test_ppl_osm.geojson', 'r')

for pos, point in enumerate(gns):
    geom = shape(point['geometry'])
    idx.insert(pos, geom.bounds)
print "index OK"

for task in grid:
    print task['id']
    polygon = shape(task['geometry'])

    schema = gns.schema.copy()
    p = task['properties']
    filename = 'export/gns_%s_%s_%s.shp' % (p['zoom'], p['x'], p['y'])

    overlapping = [gns[pos] for pos in idx.intersection(polygon.bounds)]
    with fiona.collection(filename, 'w', 'ESRI Shapefile', schema=gns.schema, crs=gns.crs) as output:
        for point in overlapping:
            geom = shape(point['geometry'])
            if geom.within(polygon):
                output.write({'properties': point['properties'], 'geometry': mapping(shape(geom))})
