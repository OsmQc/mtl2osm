# coding: utf-8
"""
Ce fichier est publié sous licence CC4-BY, car il contient des données
sous cette licence:
https://creativecommons.org/licenses/by/4.0/

(c) 2014 Guillaume Pratte

Contient des données provenant du portail des données ouvertes de
la Ville de Montréal:
http://donnees.ville.montreal.qc.ca/dataset/arceaux-velos/

L'auteur accorde son autorisation explicite d'utiliser ce script
pour l'import de données dans OpenStreetMap.

Format en entrée:
 Fichier CSV contenant les balises suivantes:
  INV_ID, INV_NO, INV_CATL_NO: Numéros dans l'inventaire de la Ville.
      INV_NO contient la même information que INV_ID et sera ignoré.
      INV_CATL_NO est le type de support et on peut en déduire la
          capacité grâce à l'analyse manuelle de la description
          dans MARQ.
  MATERIAU: acier, aluminum, béton, bois

Format en sortie:
 Fichier OSM avec les balises suivantes:
  amenity=bicycle_parking
  ref:ville_de_montreal:arceaux_velos:inv_id=$INV_ID
  ref:ville_de_montreal:arceaux_velos:inv_no=$INV_NO
  ref:ville_de_montreal:arceaux_velos:inv_catl_no=$INV_CATL_NO
  capacity=<nombre de places> (si peut être déduit de MARQ)
  operator=Ville de Montréal

"""

# INV_CATL_NO -> nombre de places
CAPACITE = {
    '689': 3,     # Support à bicyclettes à haute densité 3 places (cp-3)
    '688': 7,     # Support à bicyclettes à haute densité 7 places (cp-7)
    '692': 8,     # Support à bicyclettes «tremblant» 8 places (svtrgo8)
    '686': 30,    # Support pour 30 bicyclettes (64294) - ancien standard
}

MATERIEL = {
    'Acier':     'steel',
    'Aluminium': 'aluminium',
    u'Béton':    'concrete',
    'Bois':      'wood',
}

def filterTags(attrs):
    if not attrs:
        return

    tags = {
        'amenity': 'bicycle_parking',
        'operator': u'Ville de Montréal',
    }

    if 'INV_ID' in attrs:
        tags['ref:ville_de_montreal:arceaux_velos:inv_id'] = attrs['INV_ID']

    if 'INV_CATL_NO' in attrs:
        catl_no = attrs['INV_CATL_NO']
        tags['ref:ville_de_montreal:arceaux_velos:inv_catl_no'] = catl_no
        if catl_no in CAPACITE:
            tags['capacity'] = str(CAPACITE[catl_no])

    if 'MATERIAU' in attrs and attrs['MATERIAU'] in MATERIEL:
        tags['material'] = MATERIEL[attrs['MATERIAU']]

    return tags
