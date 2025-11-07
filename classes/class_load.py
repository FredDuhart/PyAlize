
import numpy as np
from class_struct import structure, layer


class load :
    def __init__(self, q = 0.662 , radius = 0.125, disj = 0) :

        self.type = 'roue simple'
        if disj >0 : self.type ='jumelage'

        self.disj = disj # si > 0 alors jumelage 
        self.load = q # en MPa
        self.radius = radius # en mètres
        


