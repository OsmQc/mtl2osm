# coding: utf-8
"""
Ce fichier est publié sous licence CC0:
http://creativecommons.org/publicdomain/zero/1.0/

Documentation d'importation pour ce jeu de données:
http://wiki.openstreetmap.org/wiki/Montr%C3%A9al/Imports/Postes_de_police

Format en entrée:
 Fichier KML contenant les balises suivantes:
  Name: nom du poste
  description: adresse formattée en HTML, sans le code postal

Format en sortie:
 Fichier OSM avec les balises suivantes:
  amenity=police
  operator=Service de police de la ville de Montréal
  name
  addr:housenumber
  addr:street

"""

ABBREVIATIONS = {
    'boul': 'boulevard',
    'aven': 'avenue',
    'stre': 'rue',
    'St-': 'Saint-',
    'Ste-': 'Sainte-',
} 

def filterTags(attrs):
    if not attrs:
        return

    tags = {
        'amenity': 'police',
        'operator': u'Service de police de la ville de Montréal'
    }

    if 'Name' in attrs:
        tags['name'] = attrs['Name']

    if 'description' in attrs:
        adresse, ville = attrs['description'].split('<br/>')[1:3]
        #ville = ville.split('<')[0]
        tags['addr:housenumber'] = adresse.split()[0]
        tags['addr:street'] = adresse.split(' ', 1)[1]
        for abbr in ABBREVIATIONS:
            tags['addr:street'] = tags['addr:street'].replace(abbr, ABBREVIATIONS[abbr])
        tags['addr:street'] = tags['addr:street'][0].upper() + tags['addr:street'][1:]
        if tags['addr:street'] == u'Avenue 15e':
            tags['addr:street'] = u'15e Avenue'

    return tags
