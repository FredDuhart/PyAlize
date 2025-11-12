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

# Problèmes 
- Seuls les cas de structures avec interfaces entièrement collées fonctionnent. Une tentative d'implémentation des interfaces glissantes a été testée mais donne des résultats érronés => à conforter avec un test sur alize

# Améliorations
- ajouter une interface semi-collée : les résulats seront la demi-somme des cas collés et glissant (cf. NP 98-086)
    => premiere implémentation faite => verif ok la moyenne se fait bien. (mais résultat faux à cause bug sur glissant)
- prévoir une bibliotheque de matériaux (NF P 98 086)

    ## GUI - Interface graphique
    Pour l'instant l'interface graphique est limitée à la saisie de la structure et au lancement du calcul.
    Reste à faire :
    - présentation des résultats
    - possibilité de choisir une autre charge de référence, voire de construire un chargement complexe...

# tests à faire
- test de vitesse de calcul sur les deux méthodes (en commençant par toutes interfaces collées)
 ===> Fait la méthode 'optimisée' ne l'est pas du tout ! + 40 % de temps
       la méthode optimisée a été supprimée

# Inspirations
https://www.mathworks.com/matlabcentral/fileexchange/69465-multi-layer-elastic-analysis
https://github.com/Mostafa-Nakhaei/PyMastic





