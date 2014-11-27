# coding: utf-8
"""
Ce fichier est publié sous licence CC0:
http://creativecommons.org/publicdomain/zero/1.0/

Format en entrée:
 Fichier KML contenant les balises suivantes:
  Name: nom de la caserne
  description: adresse formattée en HTML, sans le code postal

Format en sortie:
 Fichier OSM avec les balises suivantes:
  amenity=fire_station
  name
  addr:housenumber
  addr:street
  addr:city

"""

def filterTags(attrs):
    if not attrs:
        return

    tags = {
         'amenity': 'fire_station'
    }

    if 'Name' in attrs:
        tags['name'] = attrs['Name']

    if 'description' in attrs:
        adresse, le_reste = attrs['description'].split('<br/>')[1:3]
        numero = adresse.split()[0]
        rue = adresse.split(' ', 1)[1]
        rue = CORRECTION_RUES.get(rue, rue)
        ville = le_reste.split('<')[0]
        tags['addr:housenumber'] = numero
        tags['addr:street'] = rue
        tags['addr:city'] = ville

    return tags


CORRECTION_RUES = {
    u'rue  Young': u'rue Young',
    u'Boulevard Pierrefonds': u'boulevard Pierrefonds',
    u"Chemin du Tour-de-L'Isle": u"chemin du Tour-de-L'Isle",
    u'Notre-Dame Est': u'rue Notre-Dame Est',
}
