import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()


setup(name='mtl2osm',
      version='0.0.1',
      description='mtl2osm',
      long_description=README,
      url='https://github.com/guillaumep/mtl2osm',
      keywords='osm',
      packages=find_packages(),
      include_package_data=True,
      entry_points="""\
      [console_scripts]
      mtl2osm-grid-splitter = mtl2osm.osm_grid_splitter:main
      """,
      )
