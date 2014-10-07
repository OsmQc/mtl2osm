# coding: utf-8
"""
Ce fichier est publié sous licence CC0:
http://creativecommons.org/publicdomain/zero/1.0/

Format en entrée:
 Fichier Shape File contenant les balises suivantes:
  Text_: nom du jardin en lettres majuscules
  NomAr_DESC: nom des arrondissements ou de la Ville lié(s) (non utilisé)
  Index: numéro de référence de la Ville

Format en sortie:
 Fichier OSM avec les balises suivantes:
  name=Jardin communautaire $Text_
    où $Text_ provient du Shape File, majuscules ajustées
  landuse=allotments
  operator=(dérivé de NomAr_DESC via une table de correspondance)
  ref:ville_de_montreal:index_jardin_communautaire=$Index
"""

def filterTags(attrs):
    if not attrs:
        return
    tags = {
        'landuse': 'allotments',
        'operator': u'Ville de Montréal',
    }

    if 'Text_' in attrs:
        tags['name'] = 'Jardin communautaire ' + TRAD_NOMS[attrs['Text_']]

    if 'Index' in attrs:
        tags['ref:ville_de_montreal:index_jardin_communautaire'] = attrs['Index']

    if 'NomAr_DESC' in attrs:
        if TYPE_ARR[attrs['NomAr_DESC']] == 'arrondissement':
            tags['operator'] = u"Ville de Montréal, arrondissement " + attrs['NomAr_DESC']
        else:
            tags['operator'] = u"Ville de " + attrs['NomAr_DESC']

    return tags


TRAD_NOMS = {
    u'ADRIEN-D.-ARCHAMBAULT': u'Adrien-D.-Archambault',
    u'AHUNTSIC': u'Ahuntsic',
    u'ALEXIS-NIHON': u'Alexis-Nihon',
    u'ANGRIGNON': u'Angrignon',
    u'ARC-EN-SOI': u'Arc-en-soi',
    u'ARTHUR-PÉLOQUIN': u'Arthur-Péloquin',
    u'B.P. TÉTREAULVILLE': u'B.P. Tétreaulville',
    u'BABYLONE': u'Babylone',
    u'BALDWIN': u'Baldwin',
    u'BASILE-PATENAUDE': u'Basile-Patenaude',
    u'BENNY FARM': u'Benny Farm',
    u'BONS VOISINS': u'Bons voisins',
    u'BRITTANY/AINSLEY': u'Brittany/Ainsley',
    u'CABRINI': u'Cabrini',
    u'CABRINI (ANNEXE)': u'Cabrini (annexe)',
    u'CENTRE-SUD': u'Centre-Sud',
    u'CHAMPDORÉ': u'Champdoré',
    u'CHARLES-NAGUY': u'Charles-Naguy',
    u'CHRIST-ROI': u'Christ-Roi',
    u'CHÂTEAUFORT': u'Châteaufort',
    u'CITÉ DES RETRAITÉS': u'Cité des retraités',
    u'COUTURE': u'Couture',
    u'DE LA PETITE-BOURGOGNE': u'de la Petite-Bourgogne',
    u'DE LA SAVANE': u'de la Savane',
    u'DE LILLE': u'de Lille',
    u'DE LORIMIER': u'de Lorimier',
    u'DE NORMANVILLE': u'de Normanville',
    u'DES 50 CITOYENS': u'des 50 citoyens',
    u'DES RAPIDES': u'des Rapides',
    u'DES SEIGNEURS': u'des Seigneurs',
    u'DESCHAMPS': u'Deschamps',
    u'DU CARREFOUR': u'du Carrefour',
    u'DUPÉRÉ': u'Dupéré',
    u'FAUBOURG SAINT-LAURENT': u'Faubourg Saint-Laurent',
    u'GEORGES-VANIER': u'Goerges-Vanier',
    u'HABITATION SAINT-MARC': u'Habitation Saint-Marc',
    u'HABITATIONS JEANNE-MANCE': u'Habitations Jeanne-Mance',
    u'HALLOWELL': u'Hallowell',
    u'HARTENSTEIN': u'Hartenstein',
    u'HENRI-BOURASSA': u'Henri-Bourassa',
    u'HENRI-JULIEN MAGUIRE': u'Henri-Julien Maguire',
    u'HILLSIDE': u'Hillside',
    u'HOCHELAGA': u'Hochelaga',
    u'JARDIN CARDINAL': u'Jardin Cardinal',
    u'KILDARE/KELLERT': u'Kildare/Kellert',
    u"L'ÉGLANTIER": u"L'églantier",
    u'LA LÉGUMIÈRE ROSE-DE-LIMA': u'La légumière Rose-de-Lima',
    u'LA MENNAIS': u'la Mennais',
    u'LAFOND': u'Lafond',
    u'LANTHIER/SAINTE-ANNE': u'Lauthier/Sainte-Anne',
    u'LAURIER': u'Laurier',
    u'LE GOUPILLIER': u'le Goupillier',
    u'LE MICHELOIS': u'le Michelois',
    u'LES ARPENTS VERTS': u'les Arpents verts',
    u'LES CASTORS': u'les Castors',
    u'LES DEUX SAPINS': u'les Deux sapins',
    u'LES POUCES VERTS DE VERDUN': u'les Pouces verts de Verdun',
    u'LUCIE-BRUNEAU': u'Lucie-Bruneau',
    u'MAISONNEUVE': u'Maisonneuve',
    u'MARCELIN-WILSON': u'Marcelin-Wilson',
    u'MARSEILLE': u'Marseille',
    u'MONSABRÉ': u'Monsabré',
    u'MONTRÉAL-NORD': u'Montréal-Nord',
    u'MÉDÉRIC-MARTIN': u'Médéric-Martin',
    u'NOTRE-DAME-DE-GRÂCE': u'Notre-Dame-de-Grâce',
    u'NOËL-NORD': u'Noël-Nord',
    u'PANET': u'Panet',
    u'PIERRE-BERTRAND': u'Pierre-Bertrand',
    u'PIERRE-LACROIX': u'Pierre-Lacroix',
    u'PIERRE-ÉLLIOTT-TRUDEAU': u'Pierre-Élliott-Trudeau',
    u'POINTE-VERTE': u'Pointe-Verte',
    u'POP': u'Pop',
    u'PRÉ-CARRÉ': u'Pré-Carré',
    u'PÈRE-MARQUETTE': u'Père-Marquette',
    u'RENCONTRES': u'Rencontres',
    u'RIVARD': u'Rivard',
    u'ROI-RENÉ': u'Roi-René',
    u'ROSEMONT': u'Rosemont',
    u'SAINT-ANDRÉ': u'Saint-André',
    u'SAINT-EUSÈBE': u'Saint-Eusèbe',
    u'SAINT-LAURENT': u'Saint-Laurent',
    u'SAINT-MARC': u'Saint-Marc',
    u'SAINT-RAYMOND': u'Saint-Raymond',
    u'SAINT-SULPICE': u'Saint-Sulpice',
    u'SAINTE-ANNE-DE-BELLEVUE': u'Sainte-Anne-de-Bellevue',
    u'SAINTE-CATHERINE': u'Sainte-Catherine',
    u'SAINTE-MARIA-GORETTI': u'Sainte-Maria-Goretti',
    u'SAINTE-MARIE': u'Sainte-Marie',
    u'SAINTE-MARTHE': u'Sainte-Marthe',
    u'SAULT-AU-RÉCOLLET': u'Sault-au-Récollet',
    u"SOCIÉTÉ D'HORTICULTURE DE VERDUN": u"de la Société d'Horticulture de Verdun",
    u'SOULIGNY': u'Souligny',
    u'SUPER JARDIN': u'Super jardin',
    u'THORNCREST/LYAL': u'Thorncrest/Lyal',
    u'VALOIS': u'Valois',
    u'VERSAILLES': u'Versailles',
    u'VICTORIA': u'Victoria',
    u'VILLERAY': u'Villeray',
    u'ÉTIENNE-DESMARTEAU': u'Étienne-Desmarteau',
}

TYPE_ARR = {
    u'Ahuntsic-Cartierville': 'arrondissement',
    u'Anjou': 'arrondissement',
    u'C\xf4te-des-Neiges\x97Notre-Dame-de-Gr\xe2ce': 'arrondissement',
    u'C\xf4te-Saint-Luc': 'ville',
    u'LaSalle': 'arrondissement',
    u'Le Plateau-Mont-Royal': 'arrondissement',
    u'Le Sud-Ouest': 'arrondissement',
    u"L'\xeele-Dorval": 'ville',
    u'Mercier\x97Hochelaga-Maisonneuve': 'arrondissement',
    u'Mont-Royal': 'ville',
    u'Montr\xe9al-Nord': 'arrondissement',
    u'Outremont': 'arrondissement',
    u'Pointe-Claire': 'ville',
    u'Rivi\xe8re-des-Prairies\x97Pointe-aux-Trembles': 'arrondissement',
    u'Sainte-Anne-de-Bellevue': 'ville',
    u'Saint-Laurent': 'arrondissement',
    u'Saint-L\xe9onard': 'arrondissement',
    u'Verdun': 'arrondissement',
    u'Ville-Marie': 'arrondissement',
    u'Villeray\x97Saint-Michel\x97Parc-Extension': 'arrondissement',
    u'Westmount': 'ville',
}
