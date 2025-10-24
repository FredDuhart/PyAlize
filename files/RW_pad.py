# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:47:07 2023

@author: f.duhart
"""
'''
PyALIZE

ce groupe de fonctions gère les écritures / lectures des fichiers de data (et résultats?)

'''

''' IMPORTS '''


    
def read_pad (filename):
    
    file_pad = open(filename,'r+')
    
    contenu = file_pad.read()
    
    #contenu=str(file_pad)
    
    try :
        
        # enleve les retours chariots
        c_split = contenu.split("\n") 
        
        c=[]
        for i, line in enumerate (c_split):
               
            c.append(line.split(';'))
            
        nom = c[0][0]
        n_couches=int(c[1][0])
        noms_couches = c[2]
        th = [float(i) for i in c[3]]
        E = [float(i) for i in c[4]]
        nu = [float(i) for i in c[5]]
        inter = [int(i) for i in c[6]]
        
        dict_struct = {'nom' : nom,
                       'n_couches' : n_couches,
                       'noms_couches' : noms_couches,
                       'th' : th,
                       'E' : E,
                       'nu' : nu,
                       'inter' : inter}
    
    except :
        
        dict_struct ='error'
    
    file_pad.close()
    
    return dict_struct

def write_pad (dict_struct, filename):
    
    file_pad = open(filename,"w+")
    
    nom=dict_struct['nom']
    n_couches=dict_struct['n_couches']
    noms_couches=dict_struct['noms_couches']
    th=dict_struct['th']
    E=dict_struct['E']
    nu=dict_struct['nu']
    inter=dict_struct['inter']
    
    
    
    n_couches=str(n_couches)
    th = [str(i) for i in th]
    E = [str(i) for i in E]
    nu = [str(i) for i in nu]
    inter = [str(i) for i in inter]
    
    ligne=[]
    ligne.append(nom)
    ligne.append(n_couches)
    ligne.append(liste_to_string(noms_couches))
    ligne.append(liste_to_string(th))
    ligne.append(liste_to_string(E))
    ligne.append(liste_to_string(nu))
    ligne.append(liste_to_string(inter))
    
    k=7
    for i in range (k):
        if i !=k-1 :
            file_pad.writelines(ligne[i]+'\n')
        else:
            file_pad.writelines(ligne[i])
        
    
    file_pad.close()
    
    
    return

def liste_to_string(liste):
    
    l=len(liste)
    texte=''
    for i, elem in enumerate(liste):
        if i!= l-1 :
           texte = texte + elem + ';'
        else:
            texte = texte + elem
        
    return texte

# filename=r"C:/Users/f.duhart/Documents/06-Git/PyAlize/GUI/test.pad"
# filename_w=r"C:/Users/f.duhart/Documents/06-Git/PyAlize/GUI/test3.pad"

# nom = "test d'écriture"
# n_couches = 4
# noms_couches = ['C1', 'C2', 'C3','C4']
# th=[0.06,0.11,0.13]
# E=[5500,45000,11000,80]
# nu=[0.35,0.35,0.35,0.35]
# inter=[1,0,1]

# dict_struct_w = {'nom' : nom,
#                    'n_couches' : n_couches,
#                    'noms_couches' : noms_couches,
#                    'th' : th,
#                    'E' : E,
#                    'nu' : nu,
#                    'inter' : inter}


# a = write_pad(dict_struct_w, filename_w)


# dict_struct_r = read_pad(filename_w)

# if dict_struct_r == dict_struct_w :
#     print ('YOUPI!!')
# else:
#     print ('bouuuu')