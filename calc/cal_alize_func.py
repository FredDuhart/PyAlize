# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:33:10 2023

@author: f.duhart
"""
''' ensemble de fonctions permettant le calcul des sollicitatiosn dans une
structure à la façon d'Alize LCPC 

'''


import pandas as pd

import numpy as np


from R_double_iteration import R
from func_dbl_jumelage import dbl_charge, extract_soll_y



def gen_z_points (th) :
    
    '''
    th  : liste des épaisseurs des couches
    
    '''
    
    c = 0.000001
    
    
    th=np.array(th)    
    z=[]
    
    for i in range (len(th)) :
        z.append(np.sum(th[0:i+1]))
    
    z=np.array(z)
    
    zp1=np.array(z)
    zp2=np.array(z) + c
    zp0=np.array([0])
    
    zp = np.hstack ((zp1, zp2, zp0))
    zp=np.sort(zp)
    
        
    return zp


def gen_r_points (disj) :
    
    '''
    disj    : distance entre les axes des deux roues du jumelage
        
    '''
    
    rp=[0, disj/2, disj]
    rp=np.array (rp)
    
    return rp


def jum_soll(R, soll) :
    
    '''
    R    : résultat du calcul R_pyalize pour une charge avec plusieurs valeurs de r_points (dictionnaire)
    soll : sollicitation à extraire
    
    '''
    
        
    # extraction
    Rsoll = extract_soll_y(R, soll)
        
    # symetrie et addition
    R_soll_comp = dbl_charge(Rsoll)
    
    # effacement derniere colonne (qui ne sert à rien)

    R_soll_comp = R_soll_comp [:,0:-1]
    
    return R_soll_comp    


''' ********************************************************************* '''

''' _______ /////// ________'''


def calc_alize_jum (data, file) :
    
    ### extraction du chemin de fichier
    
    if file is not None:        
       deb = file.rfind("/", 0, len(file))
       chemin = file[0:deb+1]
       fichier = file [deb:-4] # on considere que l'extension est .pad (4 caractere)
       
       file_output = chemin + fichier +'_output.xlsx'
       
    
    
    
    ### définciton de la charge
    q= 0.662
    a= 0.125
    disj =0.375 # espacement des roues du jumelage
    
    
    
    
    
    ### définition de la structure
    try :
        th = data['th']
        thnp = np.array(th)
        E = data['E']
        nu = data['nu']
        isbonded = data['inter']
        n=len(th)+1 #nombre de couches
    except :
        return 'erreur dans les données'
    
    ### points de calculs
    
    z_points = gen_z_points(th)
    
    r_points = gen_r_points(disj)   
    
    ### iteration 
    
    it = 50
    
    ### calcul
    
    try :
        res_pyalize  =  R (q, a, th, E, nu, isbonded, z_points, r_points, iteration=it) 
    except :
        return 'erreur dans le calcul'
        
    
    ### mise en forme des résultats
    
    l_soll = ['e_t', 's_t', 'e_r', 's_r', 'e_z', 's_z']
    
    Rtot = np.zeros((len(z_points),0))
    
    for soll in l_soll :
        if soll[0] == 'e' :
            coef = 1000000 # pour trasnformer les def en microdef
        else :
            coef = 1
            
        Rsoll = - jum_soll(res_pyalize, soll) * coef 
        Rtot=np.hstack((Rtot,Rsoll))
    
    df_res = pd.DataFrame(Rtot)
    
    l_soll_c=[]
    for soll in l_soll :
             
        l_soll_c.append(soll + '_ar')
        l_soll_c.append(soll + '_ej')
                    
    
    
    df_res.columns = l_soll_c
    
    ### ajout des renseignements sur les couches
        
    # colonne des noms de ligne
    #   couche i sup
    #   couche i inf
    
    l_nom = []
    
    for i, z in enumerate (z_points):
        
        
        
        if i % 2 == 0 :
            n_couche = int(i/2)
            niv = ' sup'
        else :
            n_couche = int((i-1)/2)
            niv = ' inf'
        
        couche = str(n_couche + 1)
            
        couche = couche + niv
        
        l_nom.append([couche, z, E[n_couche], nu[n_couche]])
        
    
    df_noms=pd.DataFrame (l_nom)
    df_noms.columns = ['Point', 'Profondeur', 'Module', 'Coef. de Poisson']
    
    
    df_alize = pd.concat([df_noms,df_res], axis=1)
    #print (df_alize)
    
    df_alize.to_excel(file_output)
    
    return 'Calcul correctement effectué'

def calc_alize_rouesimple (data, file) :
    
    ### extraction du chemin de fichier
    
    if file is not None:        
       deb = file.rfind("/", 0, len(file))
       chemin = file[0:deb+1]
       fichier = file [deb:-4] # on considere que l'extension est .pad (4 caractere)
       
       file_output = chemin + fichier +'_output.xlsx'
       
    
    
    
    ### définciton de la charge
    q= 0.662
    a= 0.125
    disj =0.375 # espacement des roues du jumelage
    
    
    
    
    
    ### définition de la structure
    try :
        th=data['th']
        thnp=np.array(th)
        E = data['E']
        nu = data['nu']
        isbonded = data['inter']
        n=len(th)+1 #nombre de couches
    except :
        return 'erreur dans les données'
    
    ### points de calculs
    
    z_points = gen_z_points(th)
    
    r_points = [0]
    
    ### iteration 
    
    it = 25
    
    ### calcul
    
    try :
        res_pyalize  =  R (q, a, th, E, nu, isbonded, z_points, r_points, iteration=it) 
    except :
        return 'erreur dans le calcul'
        
    
    ### mise en forme des résultats
    
    l_soll = ['e_t', 's_t', 'e_r', 's_r', 'e_z', 's_z']
    
    Rtot = np.zeros((len(z_points),0))
    
    for soll in l_soll :
        if soll[0] == 'e' :
            coef = 1000000 # pour trasnformer les def en microdef
        else :
            coef = 1
            
        Rsoll = extract_soll_y(res_pyalize, soll) * coef 
        Rtot=np.hstack((Rtot,Rsoll))
    
    df_res = pd.DataFrame(Rtot)
    
                      
    
    
    df_res.columns = l_soll
    
    ### ajout des renseignements sur les couches
        
    # colonne des noms de ligne
    #   couche i sup
    #   couche i inf
    
    l_nom = []
    
    for i, z in enumerate (z_points):
        
        
        
        if i % 2 == 0 :
            n_couche = int(i/2)
            niv = ' sup'
        else :
            n_couche = int((i-1)/2)
            niv = ' inf'
        
        couche = str(n_couche + 1)
            
        couche = couche + niv
        
        l_nom.append([couche, z, E[n_couche], nu[n_couche]])
        
    
    df_noms=pd.DataFrame (l_nom)
    df_noms.columns = ['Point', 'Profondeur', 'Module', 'Coef. de Poisson']
    
    
    df_alize = pd.concat([df_noms,df_res], axis=1)
    #print (df_alize)
    
    df_alize.to_excel(file_output)
    
    return df_alize #, 'Calcul correctement effectué'


if __name__ == "__main__" :

    #data structure
    data = {'th' : [0.06, 0.10, 0.12],
            'E' : [7000, 10000, 12000, 50],
            'nu' : [0.35, 0.35, 0.35, 0.35],
            'inter' : [1,1,1]}
    
    file = "C:/Users/f.duhart/Downloads/toto.xlsx"

    res =  calc_alize_rouesimple(data, file)

    print (res)


    import matplotlib.pyplot as plt

    solls = ['s_z', 's_t', 's_r', 't_rz', 'w', 'u', 'e_z', 'e_t', 'e_r', 'E']

    soll = 'e_z'
    X = res[soll]

    
    Y = res['Profondeur']
    

    fig, ax = plt.subplots(figsize=(6,6))

    fig.suptitle (f'sollicitations {soll}')
    ax.plot(X, Y, linewidth=2.0, color='red', alpha = 1)

    plt.show()
