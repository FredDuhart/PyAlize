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
a_layer = layer()
b_layer = layer()
c_layer = layer()
d_layer = layer()
a_layer.define('BB' , 0.06, 7000, 0.35, True, 0)
b_layer.define('GB3', 0.12, 10000   , 0.35, False, 1)
d_layer.define('CdF', None, 50, 0.35, True,3)
struct = structure()
struct.add_layer(a_layer)
struct.add_layer(b_layer)
struct.add_layer(d_layer)



# chargement ****************************
disj = 0.375
#disj = 0 
load_ = load(disj = disj)


# paramètres de calcul ***********************

params = calc_params(struct, load_)

#params.add_z_points(0.02)


# distance entre les deux roues du jumelage
rp=[0] 
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

#################################
file_name = "C:/Users/f.duhart/OneDrive - Département de la Gironde/Documents/06-Git/PyAlize/exports/test_UB2.txt"
# ecriture txt
export_results (res, load_, struct, file_name)

