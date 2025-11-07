from class_struct import structure
from class_calculation import 
from class_calc_params import *
from class_load import load

from tabulate import tabulate

from class_exports import res_to_tabulate, export_results

import os


def run_roue_simple (struct) : 

    # chargement ****************************
    disj = 0 
    load_ = load(disj = disj)

    # paramètres de calcul ***********************

    params = calc_params(struct, load_)
    rp=[0] 
    params.define_r_points (rp)

    # Calculs *****************************************************
    resultats = calculation(struct, params, load_)
    res  = resultats.final_results

    # ecriture txt
    export_results (res, load_, struct )


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

def run_jumelage (struct) : 

    # chargement ****************************
    disj = 0.375
    load_ = load(disj = disj)

    # paramètres de calcul ***********************

    params = calc_params(struct, load_)
    rp=[0, disj /2,  disj] 
    params.define_r_points (rp)

    # Calculs *****************************************************
    resultats = calculation(struct, params, load_)
    res  = resultats.final_results

    res =  res_jum(res, params.r_points)

    # ecriture txt
    export_results (res, load_, struct )

if __name__ == "__main__" :

    # structure *******************************************************************
    a_layer = layer()
    b_layer = layer()
    c_layer = layer()
    d_layer = layer()
    a_layer.define('BB' , 0.06, 7000, 0.35, True, 0)
    b_layer.define('GB3', 0.12, 10000   , 0.35, True, 1)
    d_layer.define('CdF', None, 50, 0.35, True,3)
    struct = structure()
    struct.add_layer(a_layer)
    struct.add_layer(b_layer)
    struct.add_layer(d_layer)

    type = 1

    if type == 0 :
        run_roue_simple(struct)
    else :
        run_jumelage(struct)


