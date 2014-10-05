# coding: utf-8
"""
Ce fichier est publié sous licence CC0:
http://creativecommons.org/publicdomain/zero/1.0/

Format en entrée:
 Fichier Shape File contenant les balises suivantes:
  STATUT_R:
    AV À valider
    HS Hors d’usage
    A  Abandonné
    E  Existant
  NOTRCGB: Numéro se rapportant à un tronçon (entre deux intersections) de la Géobase.
  ID_AQU_BI: Numéro se rapportant à l'adresse la plus proche (en vol d'oiseau)
    de la borne d'incendie.

Format en sortie:
 Fichier OSM avec les balises suivantes:
  emergency=fire_hydrant
  ref:ville_de_montreal:notrcgb
  ref:ville_de_montreal:id_aqu_bi

"""

def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    if 'STATUT_R' in attrs:
        statut = attrs['STATUT_R']

        if statut == 'A':
            # http://wiki.openstreetmap.org/wiki/Key:abandoned
            tags['abandoned:emergency'] = 'fire_hydrant'
        elif statut == 'HS':
            # http://wiki.openstreetmap.org/wiki/Key:disused
            tags['disused:emergency'] = 'fire_hydrant'
        else: # AV et E
            tags['emergency'] = 'fire_hydrant'

    if 'NOTRCGB' in attrs:
        tags['ref:ville_de_montreal:notrcgb'] = attrs['NOTRCGB']

    if 'ID_AQU_BI' in attrs:
        tags['ref:ville_de_montreal:id_aqu_bi'] = attrs['ID_AQU_BI']

    return tags
