# coding: utf-8
"""
Ce fichier est publié sous licence CC0:
http://creativecommons.org/publicdomain/zero/1.0/

Format en entrée:
 Fichier CSV contenant les balises suivantes:
  Numero station: identifiant de la station
  Nom: nom de la station
  Adresse, arrondissement: ignoré

Format en sortie:
 Fichier OSM avec les balises suivantes:
  man_made=monitoring_station
  operator=Ville de Montréal
  ref:ville_de_montreal:stations_rsqa:${Numero station}

"""

def filterTags(attrs):
    if not attrs:
        return

    tags = {
        'man_made': 'monitoring_station',
        'operator': u'Ville de Montréal',
    }

    if 'Nom' in attrs:
        tags['name'] = "Station RSQA " + attrs['Nom']

    if 'Numero station' in attrs:
        tags['ref:ville_de_montreal:stations_rsqa'] = attrs['Numero station']

    return tags
