# coding: utf-8
"""
Ce fichier est publié sous licence CC0:
http://creativecommons.org/publicdomain/zero/1.0/

Format en entrée:
 Fichier KML contenant les balises suivantes:
  Name: nom du poste
  description: adresse formattée en HTML, sans le code postal

Format en sortie:
 Fichier OSM avec les balises suivantes:
  name
  addr:housenumber
  addr:street
  addr:city

"""

ABBREVIATIONS = {
    'boul': 'boulevard',
    'aven': 'avenue',
    'stre': 'rue',
} 

def filterTags(attrs):
    if not attrs:
        return
    tags = {}
    if 'Name' in attrs:
      tags['name'] = attrs['Name']
    if 'description' in attrs:
      adresse, ville = attrs['description'].split('<br/>')[1:3]
      ville = ville.split('<')[0]
      tags['addr:housenumber'] = adresse.split()[0]
      tags['addr:street'] = adresse.split(' ', 1)[1]
      for abbr in ABBREVIATIONS:
        tags['addr:street'] = tags['addr:street'].replace(abbr, ABBREVIATIONS[abbr])
      tags['addr:city'] = ville
    return tags
