# PyAlize
Elastic MultiLayer Model (Burmister)

# Objectif
Outil de calcul des sollicitations (déformations et contraintes) dans un modèle multicouche élastique semi-infini, par le modèle de Burmister.

# Calculs des sollicitations
Les sollicitations sont calculées sur les interfaces des couches uniquement (bas et haut).
La dernière couche est semi-infinie.

Pour chaque couche il faut renseigner : 
- un nom
- une épaisseur
- un module (MPa)
- un coefficient de poisson
- une condition d'interface (collée ou glissante)

# Charges
Le modèle peut prendre en compte une charge isolée de type circulaire.
L'interface graphique prpose deux cas de charegs pour l'instant :
- uen charge unique r=0.125 Q = 0.662 MPa
- un jumelage de deux charges (r=0.125 / Q=0.662MPa) espacées de 0.375 m

# Résultats
Les résultats sont édités sous forme d'un fichier texte.

# GUI - Interface graphique
Pour l'instant l'interface graphique est limitée à la saisie de la structure et au lancement du calcul.
Reste à faire :
- présentation des résultats
- possibilité de choisir une autre charge de référence, voire de construire un chargement complexe...

# Problèmes et améliorations
- Seuls les cas de structures avec interfaces entièrement collées focntionnent. Une tentative d'implémentation des interfaces glissantes a été testée mais donne des résultats érronés.
- prévoir une bibliotheque de matériaux (NF P 98 086)




