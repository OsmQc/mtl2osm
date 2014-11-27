mtl2osm
=======

Scripts pour la conversion des données ouvertes de la Ville de Montréal pour
importation dans OpenStreetMap


Installation
------------

(Étape préliminaire sous Mac OS X: installer VirtualBox et Vagrant, se faire
une machine virtuelle "chef/debian-7.6")

Installer les dépendances Debian:

    $ sudo apt-get install libgdal-dev python-dev python-lxml libspatialindex-dev

Ensuite initiez votre environnement virtuel:

    $ virtualenv .

Installez les dépendances:

    $ pip install requirements.txt


Utilisation du script de découpage par grille
---------------------------------------------

Le script découpage en grille prend un fichier osm en source et une grille de
défination de grille. Par exemple:

    $ mtl2osm-grid-splitter mtl2osm/donnees/monuments/osm/monuments.osm mtl2osm/donnees/montreal_10.json
