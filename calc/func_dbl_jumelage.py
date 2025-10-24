# -*- coding: utf-8 -*-
"""
Created on Wed May 24 08:24:42 2023

@author: f.duhart
"""
import numpy as np



def rr_jumelage (disj, pas , a) :
    
    '''
    Défini la liste de points radiaux à calculer
    
    disj   : espacement des deux roues (en m)
    pas    : pas souhaité de calcul (en m)
    a      : rayon de la charge
    
    '''
    
    if (disj*1000) % (pas*1000) != 0 :
        return "Le pas doit être un diviseur entier de l'espacement du jumelage"
    
    coef_plus = 2 # > 1
    
    r_max = (round((disj + a * coef_plus)/pas,0)  ) * pas
    
       
    r_points = np.arange(0, r_max + pas ,pas)

    arrondi = 4

    r_points = np.around(r_points, arrondi)

    return r_points



def rr_comp_gauche (res, rr, disg) :
    
    '''
    ajoute à gauche la partie symetrique jusqu'au point d'asbcisse disg
    
    res  : tableau de résulats
    rr   : tableau de rayons (absicsses)
    disg : distance à symetriser
    
    '''

    # recherche de l'indice de colonne
    
    i_disg, = np.where(np.isclose(rr, disg))[0]# floating-point

    # extrait la partie à symétriser
    
    res_comp = res [:,1:i_disg+1]
    rr_comp = rr [1:i_disg+1]

    
    # symetrisation verticale
    
    res_comp = np.flip (res_comp, axis = 1)
    rr_comp = np.flip (rr_comp, axis = 0)
    
    # assemblage des deux matrices
    
    res_final = np.hstack((res_comp, res))
    rr_final = np.hstack((-rr_comp, rr))
    
    return res_final, rr_final


def dbl_charge (res) :
    
    res2 = np.flip (res, axis = 1)
    res_final = res + res2
    
    return res_final


def extract_soll_y (res, soll):
        
    
    '''
    res        : dictionnaire de résultats
    soll       : sollicitation à extraire
        
    n_z        : nombre de z de calculs
    r_points   : liste des r de calcul (entre 0 et rmax et passant par disj)
    
    
    '''
    r_soll = res[soll]
    n_r = len(r_soll)    
    n_z = len (r_soll[0])
   
    
    # extraction d'une sollicitation donnée et conversion tableau de dimensions n_z x n_r
    

        
    tab_res=np.zeros((n_z, n_r))
    
    for i in range(n_r):
        coli = r_soll[i]
        tab_res[:,i]=coli
        
    tab_final = tab_res
        
    return tab_final   

