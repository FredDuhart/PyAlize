# -*- coding: utf-8 -*-
"""

aide à ajouter


Cette fonction calcule les sollicitations soumises à la charge -m*J0(m*rho)

Elle prend comme paramètres :
    n          : nombre de couches (integer)
    H          : épaisseur totale de la structure
    z          : liste des profondeurs de couches
    lb         : liste des valeurs de lambda par couche (lambda = z(couche)/H)
    R          : liste des valeurs de R par couche (R(couche) = (E[i]/E[i+1])*(1+nu[i+1])/(1+nu[i]) )
    E          : Modules des n couches (en MPa) - liste de taille (n)
    nu         : Coefficient de poisson (sans unité) - liste de taille (n)
    isbonded   : 1 si interface collée - 0 si interface glissante
                    pour l'instant soit tout est collé soit tout es glissnat ====> évolution à venir
    m          : valeur de m
    z_points   : liste des z des points à calculer (en m)                    
    rr         : position des points de calcul par rapport à l'axe de la charge (en m)
    c_points   : liste des indices des couches pour les z_points (liste d'entier)
   
                                                                  
Elle retourne un tableau des solllicitaitions R* pour chaque z_points

"""
import numpy as np
import math
from scipy.special import j0
from scipy.special import j1



# ''' TEST '''


# n=4
# H=0.28
# z=[0.06, 0.16, 0.28]



# lb=[0.21428571428571425, 0.5714285714285714, 1.0, np.Inf]
# R=[0.7, 0.8333333333333335, 239.99999999999997]
# E=[7000, 10000, 12000, 50]
# nu=[0.35, 0.35, 0.35, 0.35]
# isbonded= [1,1,1]


# z_points=[0]
# c_points=[0, 0, 0, 1, 2, 3]




# m=20
# rr=0






def R_star_u(n, H, z, lb , R , E, nu, isbonded, m, z_points, rr, c_points):
        
     
                
    ''' --------------------------------------- '''
    ''' calcul des valeurs F(i) dépendantes de m '''
    
    
    F=[]
    
    
    ''' F[0] '''
    ''' equations B.12a et B.12b '''
    
    F0=math.exp(-m* (lb[0]-0))
    F.append(F0)
    
    
    ''' F[i]  pour i=1 to n-1-1 '''
    ''' equations B.12a et B.12b '''
    
    for i in range (n-2):
        Fi = math.exp(-m* (lb[i+1]-lb[i]))
        F.append(Fi)
        
    
    # valeur de Fn (dernière couche)
    
    lb.append(np.Inf) # Infini pour couche n (substratum)
    Fn=math.exp(-m * (lb[n-1] - lb[n-2]))
    
    F.append(Fn)
    
    
    ''' -------------- calcul de la matrice de dimensions 4n-2 x 4n-2 -----------------
    '''
    
    s_Mat = (4 * n  - 2 , 4 * n  ) # il manquerait pas un -2 ???!!!
    Mat = np.zeros (s_Mat, dtype=np.float64)
    
    # equations B.9 ====> condtions limites à la surface
    
    Mat[0,0] = math.exp(-lb[0] * m)
    Mat[1,0] = math.exp(-lb[0] * m)
    Mat[0,1] = 1
    Mat[1,1] = -1
    
    Mat[0,2] = -(1 - 2 * nu[0]) * math.exp(-m * lb[0]);
    Mat[1,2] = 2 * nu[0] * math.exp(-m * lb[0]);
    Mat[0,3] = 1 - 2 * nu[0];
    Mat[1,3] = 2 * nu[0];
    
    
    # equations B.11 ou B.17 ======> conditions d'interfaces de couches
    
    for couche in range (n-1): 
        
        # la premiere ligne est la troisième => indice = 2
        # ligne1 = 2 + (couche)*4
        
        lig = 2 + couche * 4
        col = couche * 4
        
        
        if isbonded[couche] == 1: #] interface collée
                        
            # partie gauche
            Mat[lig+0,col+0]=1
            Mat[lig+1,col+0]=1
            Mat[lig+2,col+0]=1
            Mat[lig+3,col+0]=1
    
            Mat[lig+0,col+1] = F[couche]
            Mat[lig+1,col+1] = -F[couche]
            Mat[lig+2,col+1] = F[couche]
            Mat[lig+3,col+1] = -F[couche]
            
            Mat[lig+0,col+2] = -(1 - 2 * nu[couche] - m * lb[couche])
            Mat[lig+1,col+2] = (2 * nu[couche] + m * lb[couche])
            Mat[lig+2,col+2] = 1 + m * lb[couche]
            Mat[lig+3,col+2] = -(2 - 4 * nu[couche] - m * lb[couche])
    
            Mat[lig+0,col+3] = (1 - 2 * nu[couche] + m * lb[couche]) * F[couche]              
            Mat[lig+1,col+3] = (2 * nu[couche] - m * lb[couche]) * F[couche]
            Mat[lig+2,col+3] = -(1 - m * lb[couche] )* F[couche]
            Mat[lig+3,col+3] = -(2 - 4 * nu[couche] + m * lb[couche]) * F[couche]
            
            
            # partie droite
           
            Mat[lig+0,col+4+0] = -F[couche+1]  
            Mat[lig+1,col+4+0] = -F[couche+1]
            Mat[lig+2,col+4+0] = -R[couche] * F[couche+1]  
            Mat[lig+3,col+4+0] = -R[couche] * F[couche+1]
    
            Mat[lig+0,col+4+1] = -1  
            Mat[lig+1,col+4+1] = 1
            Mat[lig+2,col+4+1] = -R[couche]  
            Mat[lig+3,col+4+1] = R[couche]
    
            Mat[lig+0,col+4+2] = (1 - 2 * nu[couche+1] - m * lb[couche]) * F[couche+1]  
            Mat[lig+1,col+4+2] = -(2 * nu[couche+1] + m * lb[couche]) * F[couche+1]
            Mat[lig+2,col+4+2] = -(1 + m * lb[couche]) * R[couche] * F[couche+1]
            Mat[lig+3,col+4+2] = (2 - 4 * nu[couche+1] - m * lb[couche]) * R[couche] * F[couche+1]
            
            Mat[lig+0,col+4+3] = -(1 - 2 * nu[couche+1] + m * lb[couche])  
            Mat[lig+1,col+4+3] = -((2 * nu[couche+1] - m * lb[couche]))
            Mat[lig+2,col+4+3] = (1 - m * lb[couche]) * R[couche]  
            Mat[lig+3,col+4+3] = (2 - 4 *nu[couche+1] + m * lb[couche]) * R[couche]
            
            
          
        elif isbonded[couche] == 0: # cas glissant
            zro = 0 #1e-50
        
            # partie gauche
    			
            Mat[lig+0,col+0] = 1
            Mat[lig+1,col+0] = 1
            Mat[lig+2,col+0] = 1
            Mat[lig+3,col+0] = zro
            
            Mat[lig+0,col+1] = F[i]
            Mat[lig+1,col+1] = F[i]
            Mat[lig+2,col+1] = -F[i]
            Mat[lig+3,col+1] = zro
            
            Mat[lig+0,col+2] = -(1 - 2 * nu[i] - m * lb[i])
            Mat[lig+1,col+2] = 1 + m * lb[i]
            Mat[lig+2,col+2] = 2*nu[i] + m * lb[i]
            Mat[lig+3,col+2] = zro
            
            Mat[lig+0,col+3] = (1 - 2 * nu[i] + m * lb[i]) * F[i]
            Mat[lig+1,col+3] = -(1 - m * lb[i]) * F[i]
            Mat[lig+2,col+3] = (2 * nu[i] - m * lb[i]) * F[i]
            Mat[lig+3,col+3] = zro 
    
            # partie droite
            
            Mat[lig+0,col+4+0] = -F[i + 1]  
            Mat[lig+1,col+4+0] = -R[i]*F[i + 1]
            Mat[lig+2,col+4+0] = zro  
            Mat[lig+3,col+4+0] = -F[i + 1]
                
            Mat[lig+0,col+4+1] = -1  
            Mat[lig+1,col+4+1] = -R[i]
            Mat[lig+2,col+4+1] = zro  
            Mat[lig+3,col+4+1] = 1
              
            Mat[lig+0,col+4+2] = (1 - 2 * nu[i + 1] - m * lb[i]) * F[i+1]
            Mat[lig+1,col+4+2] = -(1 + m * lb[i]) * R[i] * F[i+1]
            Mat[lig+2,col+4+2] = zro
            Mat[lig+3,col+4+2] = -(2 * nu[i+1] + m * lb[i]) * F[i+1]
              
            Mat[lig+0,col+4+3] = -(1 - 2 * nu[i+1] + m * lb[i])
            Mat[lig+1,col+4+3] = (1 - m * lb[i]) * R[i]
            Mat[lig+2,col+4+3] = zro
            Mat[lig+3,col+4+3] = -(2*nu[i+1]-m*lb[i])
            
    
    # réduction de la matrice en enlevant les colonnes pour An et Cn (car An = 0 et Cn = 0)    
    
    Mat_reduit = Mat[:,0:-4]
    Mat_Bn = Mat [:,-3]
    Mat_Dn = Mat [:,-1]
    
    Mat_BnDn = np.vstack((Mat_Bn,Mat_Dn)).T
    
    Mat_fin = np.hstack((Mat_reduit, Mat_BnDn))
    
    # définiiton du vecteur de droite (nul partout sauf pour le premier élément = 1)
    
    vect_droite = np.zeros(4 * n -2)
    vect_droite[0] = 1 # cf. equation B.9
    
    # résolution des équations
    
    res = np.linalg.solve(Mat_fin, vect_droite)
    
    
    # définition des tableau A, B, C et D
    
    A=np.zeros(n,dtype=np.float64)
    B=np.zeros(n,dtype=np.float64)
    C=np.zeros(n,dtype=np.float64)
    D=np.zeros(n,dtype=np.float64)
    
    for i in range (n) :
    
        if i != n-1 :
            A[i]=res[4*i]
            B[i]=res[4*i+1]
            C[i]=res[4*i+2]
            D[i]=res[4*i+3]
            
        else :
            A[i]=0
            B[i]=res[-2]
            C[i]=0
            D[i]=res[-1]
        
    
    
    ''' --------------------------------------- '''
    ''' calcul des sollicitations R* '''
    
    #initialisation de la variable de rendu
    # la variable de rendu est un dictionnaire
    
    response = {'s_z*' : [], 's_t*' : [], 's_r*' : [], 't_rz*' : [], 'w*' : [], 'u*' : []}
    
    rho=rr/H
    
    for i, zz in enumerate(z_points): # boucle sur les z
        
        lmm = zz/H
        ii = c_points[i]
      
        lb.append(0) # permet d'éviter les erreurs sur la première couche => lb (i-1) = lb (-1) = 0
        
        # pour gérer rho = 0 pour sigma t et sigma r            
        if rho == 0 :
            COEF1 = m/2 # reste à vérifier car vu nulle part !
        else :
            COEF1 = j1(m * rho) / rho            
        
        # sigma z
        sigma_z = -m * j0(m * rho) * ((A[ii] - C[ii] * (1 - 2 * nu[ii] - m * lmm)) * math.exp(-m * (lb[ii] - lmm)) 
                                      + (B[ii] + D[ii] * (1 - 2 * nu[ii] + m * lmm)) * math.exp(-m * (lmm - lb[ii - 1]))) 
    
        # sigma t
        sigma_t = COEF1 * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (lb[ii] - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - lb[ii - 1]))) + 2 * nu[ii] * m * j0(m * rho) * (C[ii] * math.exp(-m * (lb[ii] - lmm)) - D[ii] * math.exp(-m * (lmm - lb[ii - 1])))
        
            
        # sigma r
        sigma_r = (m * j0( m * rho) - COEF1) * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (lb[ii] - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - lb[ii-1]))) + 2 * nu[ii] * m * j0( m * rho) * (C[ii] * math.exp(-m * (lb[ii] - lmm)) - D[ii] * math.exp(-m * (lmm - lb[ii-1])))
        
        # tau rz
        tau_rz = m * j1( m * rho) * ((A[ii] + C[ii] * (2 * nu[ii] + m * lmm)) * math.exp(-m * (lb[ii] - lmm)) - (B[ii] - D[ii] * (2 * nu[ii] - m * lmm)) * math.exp(-m * (lmm - lb[ii-1])))
        
        # w 
        w = -H*(1 + nu[ii]) / E[ii] * j0( m * rho) * ((A[ii] - C[ii] * (2 - 4 * nu[ii] - m * lmm)) * math.exp(-m * (lb[ii] - lmm)) - (B[ii] + D[ii] * (2 - 4 * nu[ii] + m * lmm)) * math.exp(-m * (lmm - lb[ii-1])))         
        
        # u 
        u = H*(1 + nu[ii]) / E[ii] * j1( m * rho) * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (lb[ii] - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - lb[ii-1])))
    
        response['s_z*'].append(sigma_z)
        response['s_t*'].append(sigma_t)
        response['s_r*'].append(sigma_r)
        response['t_rz*'].append(tau_rz)
        response['w*'].append(w)
        response['u*'].append(u)
    
    # fin de boucle z
    
    return response          
   

   







                 
