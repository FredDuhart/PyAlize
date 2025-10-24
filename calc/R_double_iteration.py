# -*- coding: utf-8 -*-
"""
Created on Tue May 16 11:19:46 2023

@author: f.duhart
"""

import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.special import j0
from scipy.special import j1

from list_m import list_quad_m
from R_star_unbonded import R_star_u
from R_star import R_star


def R (q, a, th, E, nu, isbonded, z_points, r_points, iteration = 25) :
    
    '''
    
    
    Données d'entrées :
        q          : charge (en MPa)
        a          : rayon de la charge (en m)
        
        th         : épaisseurs des couches (en m) - liste de taille (n-1) - la dernière couche est semi-infinie
        E          : Modules des n couches (en MPa) - liste de taille (n)
        nu         : Coefficient de poisson (sans unité) - liste de taille (n)
        isbonded   : 1 si interface collée - 0 si interface glissante
                        pour l'instant soit tout est collé soit tout es glissnat ====> évolution à venir
       
        z_points   : liste des z des points à calculer (en m)                    
        r_points   : liste des r (rayons) des points à calculer (en m)                    
       
        iteration  : nombre d'intervalles d'integration 
       
    '''
    
    ''' -------------------------------------------------------------------------------------
        Calculs préalables 
    '''    
    
    
    #  nombre de couches 

    n = len(th)+1
    
    
    
    # calcul de z(i) 

    th=np.array(th)    
    z=[]
    for i in range (n-1) :
        z.append(np.sum(th[0:i+1]))
    
    z=np.array(z)
    
    # calcul de H (hauteur de la structure) 

    H=z[-1]
    
    # toutes les couches sont elles collées ?
    
    isb = np.array(isbonded)
    # if isb.sum() == len (isb)  :
    #     all_bonded = True
    
    # if all_bonded :
    #     print ('toutes les couches sont collées ! ')
    # else :
    #     print ('au moins une glissante')
    
    
    # calcul de c_points (indice de couches pour les z_points)
                   
    znp=np.hstack(([-0.0001],z))
    

    c_points=[]

    for i, zz in enumerate(z_points):
        couche = len(np.where(zz > znp)[0])-1
        c_points.append(couche)
    
    # calcul des valeurs de E et nu pour chaque z_point
    
    EE = []
    vv = []
    
    for jj in c_points:
        EE.append(E[jj])
        vv.append(nu[jj])
    
    EE=np.array(EE)
    vv=np.array(vv)
    
    #print (f'Taille EE {np.shape(EE)}')
    
    # calcul de lambda (lb) --- z(i) / H 
    lb=[]
    for i in range (n-1):
        zi=z[i]/H
        lb.append(zi)
    
    lb.append(np.inf) # infini pour couche n (substratum)
        
    
    # calcul des valeurs R(i)
    #    on en calcule pas F(i) car dépendant de la valeur de m 
    
    
    R=[]
    
    # R[0] -  equations B.12a et B.12b 
    
    R0=(E[0]/E[1])*(1+nu[1])/(1+nu[0])
    R.append(R0)
    
    # R[i] pour i=1 to n-1-1  -  equations B.12a et B.12b 
    
    for i in range (n-2):
        
        Ri = (E[i+1]/E[i+2])*(1+nu[i+2])/(1+nu[i+1])
        R.append(Ri)
    
    # calcul de alpha
    
    alpha = a/H
    
    
    
    
    ''' ---------------------------------------------------------------------------------
        Boucle sur les valeurs de r_points
    '''
    
    response = {'s_z' : [], 's_t' : [], 's_r' : [], 't_rz' : [], 'w' : [], 'u' : [], 'e_z' : [], 'e_t' : [], 'e_r' : [], 'E' : []}
    
    for i , rr in enumerate( r_points) :
        
        # calcul des points d'intégration
        
        l_quad_r=list_quad_m (a, rr, H, iteration)
        
                    
                    
        # -------   Boucle sur les valeurs d'intégration   -------
        
        
        # initialisation des variables de résultats
        
        
        k_max = np.shape(l_quad_r)[0]
        
                
        sig_z   = np.zeros((len(z_points)))
        sig_z_0 = np.zeros((len(z_points)))                
        sig_t   = np.zeros((len(z_points)))
        sig_t_0 = np.zeros((len(z_points)))               
        sig_r   = np.zeros((len(z_points)))
        sig_r_0 = np.zeros((len(z_points)))
        tau_rz   = np.zeros((len(z_points)))
        tau_rz_0 = np.zeros((len(z_points)))
        w   = np.zeros((len(z_points)))
        w_0 = np.zeros((len(z_points)))
        u   = np.zeros((len(z_points)))
        u_0 = np.zeros((len(z_points)))
        
        # boucle
        for k, couple_m in enumerate(l_quad_r) :
            
            m=couple_m[0]
            poids_m = couple_m[1]
            
            
            # choix du mode de calcul
            
            if isb.sum() == len (isb) :
                            
                try :                                       
                    
                    #print('Calcul optimisé')
                    rstar=R_star(n, H, z, lb , R , E, nu, isbonded, m, z_points, rr, c_points)
                                    
                except:
                    print (' ')
                    print ("//!\\ //!\\ //!\\ //!\\ //!\\") 
                    print (f'erreur itération {k}')
                    print ("//!\\ //!\\ //!\\ //!\\ //!\\")
                    print (' ')
                       
            if isb.sum() != len (isb) :
                            
                try :                                       
                   #print('calcul complet') 
                   rstar=R_star_u(n, H, z, lb , R , E, nu, isbonded, m, z_points, rr, c_points)
                                    
                except:
                    print (' ')
                    print ("//!\\ //!\\ //!\\ //!\\ //!\\") 
                    print (f'erreur itération {k}')
                    print ("//!\\ //!\\ //!\\ //!\\ //!\\")
                    print (' ')
                               
            
            
            # Récupération des valeurs pour itréation - 1           
            
            if k == (k_max)-4 : 
                sig_z_0 = sig_z
                sig_t_0 = sig_t
                sig_r_0 = sig_r
                tau_rz_0 = tau_rz
                w_0 = w
                u_0 = u
           
            # calcul des sollicitation pour 'itération'
            
            s_z_star = np.array(rstar['s_z*'])
            sig_z = sig_z + poids_m * (q * alpha * 1 / m * j1(m * alpha))  * s_z_star  
            
            s_t_star = np.array(rstar['s_t*'])
            sig_t = sig_t + poids_m * (q * alpha * 1 / m * j1(m * alpha)) * s_t_star
                        
            s_r_star = np.array(rstar['s_r*'])
            sig_r = sig_r + poids_m * (q * alpha * 1 / m * j1(m * alpha)) * s_r_star
                        
            t_rz_star = np.array(rstar['t_rz*'])
            tau_rz = tau_rz + poids_m * (q * alpha * 1 / m * j1(m * alpha)) * t_rz_star
                        
            w_star = np.array(rstar['w*'])
            w = w + poids_m * (q * alpha * 1 / m * j1(m * alpha)) * w_star
                        
            u_star = np.array(rstar['u*'])
            u = u + poids_m * (q * alpha * 1 / m * j1(m * alpha)) * u_star
            
           
            rstar=None
        
        l_quad_r=None
        
            
                
        # moyenne des deux itérations pour une valeur de r
              
        sig_z_moy =  np.vstack((sig_z,sig_z_0)).T
        sig_z =  np.mean(sig_z_moy, axis = 1)
        sig_t_moy =  np.vstack((sig_t,sig_t_0)).T
        sig_t =  np.mean(sig_t_moy, axis = 1)
        sig_r_moy =  np.vstack((sig_r,sig_r_0)).T
        sig_r =  np.mean(sig_r_moy, axis = 1)
        tau_rz_moy =  np.vstack((tau_rz,tau_rz_0)).T
        tau_rz =  np.mean(tau_rz_moy, axis = 1)
        w_moy =  np.vstack((w,w_0)).T
        w =  np.mean(w_moy, axis = 1)
        u_moy =  np.vstack((u, u_0)).T
        u =  np.mean(u_moy, axis = 1)            
   
    
        # calcul des déformations
        
        e_z = 1 / EE * (sig_z - vv * (sig_t + sig_r))
        e_t = 1 / EE * (sig_t - vv * (sig_z + sig_r))
        e_r = 1 / EE * (sig_r - vv * (sig_t + sig_z))
        
        #resultat= np.resize(resultat[0], (len(z_points),1))
        #resultat=resultat.flatten()
        
        response['s_z'].append(sig_z)
        response['s_t'].append(sig_t)
        response['s_r'].append(sig_r)
        response['t_rz'].append(tau_rz)
        response['w'].append(w)
        response['u'].append(u)
        response['e_z'].append(e_z)
        response['e_t'].append(e_t)
        response['e_r'].append(e_r)
        response['E'].append(EE)
        
    return response 





