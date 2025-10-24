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
L'outil est conçu pour répondre aaux régles françaises, c'est donc le jumelage standard qui est pris en compte dans l'interface graphique.

# GUI - Interface graphique
Pour l'instant l'interface graphique est limitée à la saisie de la structure et au lancement du calucl
Reste à faire :
- présentation des résultats
- possibilité de choisir une autre charge de référence, voire de construire un chargement complexe...

# Problèmes
Seuls les cas de structures avec interfaces entièrement collées focntionnent. Une tentative d'implémentation des interfaces glissantes a été testée mais donne des résultats érronés.
Toute aide serait la bienvenue.

# Améliorations à prévoir
- passer sous Qt


# Remerciements
Merci à Mostafa-Nakhaei pour son inspiration - voir son dépot gitHub https://github.com/Mostafa-Nakhaei