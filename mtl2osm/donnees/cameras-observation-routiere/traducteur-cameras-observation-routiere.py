# coding: utf-8
"""
Ce fichier est publié sous licence CC0:
http://creativecommons.org/publicdomain/zero/1.0/

Documentation d'importation pour ce jeu de données:
http://wiki.openstreetmap.org/wiki/Montr%C3%A9al/Imports/Cam%C3%A9ras_d%27observation_routi%C3%A8re

Format en entrée:
 Fichier CSV contenant les colonnes suivantes:
  INT: numéro de l'intersection
  RIRE_1: numéro de l'axe routier #1
  RIRE_2: numéro de l'axe routier #2
  RUE1 / RUE2: nom des rues de l'intersection routière où est installé la caméra
  X et Y: coordonnées en format SCOPQ projetée SCOPQ MTM Nad83, fuseau 8 (ceci est une hypothèse)

  Ces données ne sont pas utiles pour OpenStreetMap; seulement les coordonnées seront utilisées.

Format en sortie:
 Fichier OSM avec les balises suivantes:
  man_made=surveillance
  surveillance=outdoor
  surveillance:type=camera
  surveillance:zone=traffic
  camera:type=panning
  camera:feature=zoom
  camera:angle=360
  operator=Ville de Montréal

 Les balises sont dérivées du texte suivant, en provenance du portail de données:
  Ces caméras de type PTZ (Pan-tilt-zoom) installées aux intersections permettent
  le monitoring en temps réel de points stratégiques du réseau. Les principales
  caractéristiques de ce type de caméra sont de pouvoir pivoter sur 360 degrés et
  d'effectuer des «zooms» (agrandissements d'image).
"""

def filterTags(attrs):
    if not attrs:
        return

    tags = {
        'man_made': 'surveillance',
        'surveillance': 'outdoor',
        'surveillance:type': 'camera',
        'surveillance:zone': 'traffic',
        'camera:type': 'panning',
        'camera:feature': 'zoom',
        'camera:angle': '360',
        'operator': u'Ville de Montréal',
    }

    return tags
