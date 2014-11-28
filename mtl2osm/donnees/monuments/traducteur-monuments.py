# coding: utf-8
"""
Ce fichier est publié sous licence CC0:
http://creativecommons.org/publicdomain/zero/1.0/

Format en entrée:
 Fichier CSV contenant les balises suivantes:
  NOM: nom de l'oeuvre. En majuscule, à revoir manuellement.
  NO_OUVRAGE: numéro de référence de la Ville.

Format en sortie:
 Fichier OSM avec les balises suivantes:
  tourism=artwork
  artwork_type=... (à remplir)
  ref:villedemontreal:artwork=$NO_OUVRAGE
  name

Note: ce fichier de données demande de la validation sur le terrain, et ne 
      devrait pas être importé tel quel.
"""

def filterTags(attrs):
    if not attrs:
        return

    tags = {
        'tourism': 'artwork',
        'artwork_type': u'... (à remplir...)'
    }

    if 'NOM' in attrs:
        tags['name'] = attrs['NOM']

    if 'NO_OUVRAGE' in attrs:
        tags['ref:villedemontreal:artwork'] = attrs['NO_OUVRAGE']

    return tags
