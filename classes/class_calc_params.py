# -*- coding: utf-8 -*-
"""

@author: f.duhart
"""
'''

détermine pour une structure donnée les points à calculer
et la charge


'''
import numpy as np
from class_struct import structure, layer


class calc_params :
    def __init__(self, structure : structure):
        
        
        self.struct = structure
        self.layers = self.struct.layers
        
        # points de calcul
        self.z_points=self.gen_z_points()
        self.c_points=self.gen_c_points()
        self.r_points=None


    # --------------------------------------
    #  METHODES POUR DETERMINATION DES POINTS DE CALCULS
    # --------------------------------------

    def gen_z_points (self) :
        z = []
        for l in self.layers :
            z.append(l.z)
        
        z = z[0:-1] # on enleve la dernier couche (substratum)
        
        c = 0.000001

        zp1=np.array(z)    
        zp2=np.array(z) + c
        zp0=np.array([0])
        
        zp = np.hstack ((zp1, zp2, zp0))
        zp=np.sort(zp)

        return zp
    
          

    def gen_c_points(self) :
        if self.z_points is not None :
        
            
            z = []
            for l in self.layers :
                z.append(l.z)
            z = z[0:-1] # on enleve la dernier couche (substratum)
            
            z=np.array(z)


            # calcul de c_points (indice de couches pour les z_points)
                        
            znp=np.hstack(([-0.0001],z))
            
            c_points=[]

            for i, zz in enumerate(self.z_points):
                couche = len(np.where(zz > znp)[0])-1
                c_points.append(couche)

            return  c_points


