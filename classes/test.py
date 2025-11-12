from class_struct import *
from class_calculation import *
from class_calc_params import *
from class_load import load

from tabulate import tabulate
from IPython.display import display

from class_exports import res_to_tabulate, export_results

import os

'''
n=3
H=0.28
z=[0.06, 0.16, 0.28]



lb=[0.21428571428571425, 0.5714285714285714, 1.0, np.inf]
R=[0.7, 0.8333333333333335, 239.99999999999997]
E=[7000, 10000, 12000, 50]
nu=[0.35, 0.35, 0.35, 0.35]
isbonded= 1
'''
# structure *******************************************************************


def cas1_bb() :
    a_layer = layer()
    aa_layer = layer()
    b_layer = layer()
    c_layer = layer()
    d_layer = layer()
    bb_layer = layer()
    aa_layer.define('BBTM', 0.025, 3000, 0.35, 0, 0)
    a_layer.define('BB' , 0.06, 7000, 0.35, 0, 1)
    b_layer.define('GB3', 0.13, 9000   , 0.35, 0, 2)
    bb_layer.define('GB3', 0.13, 9000   , 0.35, 0, 3)
    d_layer.define('CdF', None, 50, 0.35, 0, 4)
    struct = structure()
    struct.add_layer(aa_layer)
    struct.add_layer(a_layer)
    struct.add_layer(b_layer)
    struct.add_layer(bb_layer)
    struct.add_layer(d_layer)
    struct.calc_struct()

    return struct

def cas1_rigide() :
    a_layer = layer()
    b_layer = layer()
    c_layer = layer()
    a_layer.define('BC5', 0.23, 35000, 0.25, 2, 0)
    b_layer.define('BC2', 0.18, 20000, 0.25, 0, 1)
    c_layer.define('PF2', None, 50, 0.35, 0, 2)
    struct = structure()
    
    struct.add_layer(a_layer)
    struct.add_layer(b_layer)
    
    struct.add_layer(c_layer)
    struct.calc_struct()

    return struct

struct = cas1_bb()
struct = cas1_rigide()

print (struct.export_tab())


# chargement ****************************
disj = 0.375
disj = 0 
load_ = load(disj = disj)


# paramètres de calcul ***********************

params = calc_params(struct, load_)

params.add_z_points(0.02)


# distance entre les deux roues du jumelage
rp=[0, 0.1875] 
if load_.type == 'jumelage' :
    rp = [0, disj/2, disj]

#, disj/2, disj]#, disj/2]#, disj]
params.define_r_points (rp)

# Calculs *****************************************************


resultats = calculation(struct, params, load_)
res  = resultats.final_results



###### Cas d'un jumelage ####################

def res_jum (res, rr) :
    
    solls = ['s_z','s_t','s_r','t_rz','w','u','e_z','e_t','e_r']
    
    for soll in solls :
        for i, r in enumerate(rr) :
            res[soll, r] = res[soll, r] + res[soll, rr[-1-i]]
        
    res = res.drop(rr[-1], level = 1, axis=1) # on enlève la derniere position de r mais ça ne mets pas à jour la liste des colonnes....

    #renomage des colonnes
    # level 1
    l_1 = rr[:-1] * len(solls)
    # level 0
    l_0 = []
    for soll in solls :
        for i in range(len(rr[:-1])) :
            l_0.append(soll)
    
    res.columns = res.columns.remove_unused_levels()

    return res
    
if load_.type == 'jumelage' :
    res =  res_jum(res, params.r_points)

res  =res [['s_z', 's_t', 't_rz', 'w', 'u' ]]

print (res.head(25))

