# -*- coding: utf-8 -*-
"""

@author: f.duhart
"""
'''

à documenter

'''
import numpy as np
from tabulate import tabulate


class layer :

    def __init__(self):
        self.name :str = None
        self.thickness : float = None
        self.module : int = None        
        self.poisson : float = None
        self.interface : bool = None # True = collée (bond)
        self.order : int = None
        self.lb : float = None
        self.z : float = None # profondeur max de la couche

        
    def define(self, name : str ,thickness : float , module : int , poisson : float , interface : bool , order : int ) :
        self.name  = name
        self.thickness : float = thickness
        self.module : int = module        
        self.poisson : float = poisson
        self.interface : bool  = interface
        self.order : int = order

    def re_order (self, order) :
        self.order : int = order

class structure :
    def __init__(self):
        self.name : str = None
        self.layers : layer = []
        

    def add_layer(self, alayer : layer) :
        self.layers.insert(alayer.order, alayer)
        self.calc_struct()

    def remove_layer(self, pos) :
        # remove layer in pos position
        del self.layers[pos]
        self.calc_struct()

    def calc_struct(self) :
        #self.layers[-1].thickness = None
        H = self.htot()
        z = 0 
        for i, l in enumerate(self.layers) :
            l.order = i
            if l.thickness is not None :
                z += l.thickness
                z = round(z,3)
                l.lb = z/H
                l.z = z
        
        self.layers[-1].lb = np.inf
        self.layers[-1].z = np.inf


        
    def htot(self):
        if not (self.layers is None):
            H = 0 
            for l in self.layers :
                if l.thickness is not None :
                    H += l.thickness
        return round(H,3)

    def export_tab(self) :
        dico_struct=[]
        
        for l in self.layers :
            if l.interface : 
                inter = 'Collée'
            else : 
                inter = 'Glissante'
            dico_struct.append({'Matériau' : l.name,
                                'Ep. (m)' : l.thickness,
                                'E (MPA)' : l.module,
                                'nu' : l.poisson,
                                'Interface' : inter} )
            

        #traitement de la dernière couche

        dico_struct[-1]['Interface'] = ''
        dico_struct[-1]['Ep. (m)'] = 'Semi-infinie'
        
        table = tabulate(dico_struct,
                     headers="keys", 
                     
                     tablefmt='rounded_grid', 
                     showindex=True, 
                     numalign="center", 
        )

        return table



