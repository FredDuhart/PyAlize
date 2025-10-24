# -*- coding: utf-8 -*-
"""

aide à ajouter


Cette fonction calcule les sollicitations soumises à la charge -m*J0(m*rho)

ATTENTION ne fonctionne que dans le cas de couches liées

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



def R_star(n, H, z, lb , R , E, nu, isbonded, m, z_points, rr, c_points):
    
 
    
            
    ''' --------------------------------------- '''
    ''' calcul des valeurs F(i)  '''

    
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
        
        
    
    
    # valeur de Fn
    
    lb.append(np.Inf) # Infini pour couche n (substratum)
    Fn=math.exp(-m * (lb[n-1] - lb[n-2]))
    
    F.append(Fn)
    

    ''' --------------------------------------- '''
    ''' calcul des matrices de l'équation B.11 '''

    MM1=[]
    MM2=[]
    M=[]
    
    for couche in range(n-1): # toutes les couches sauf le substratum

        s=(4,4)
        M1 = np.zeros(s, dtype=np.float64)
        M2 = np.zeros(s, dtype=np.float64)

   
                    
        # Matrice M1 (gauche)
        M1[0,0]=1
        M1[1,0]=1
        M1[2,0]=1
        M1[3,0]=1

        M1[0,1] = F[couche]
        M1[1,1] = -F[couche]
        M1[2,1] = F[couche]
        M1[3,1] = -F[couche]
        
        M1[0,2] = -(1 - 2 * nu[couche] - m * lb[couche])
        M1[1,2] = (2 * nu[couche] + m * lb[couche])
        M1[2,2] = 1 + m * lb[couche]
        M1[3,2] = -(2 - 4 * nu[couche] - m * lb[couche])

        M1[0,3] = (1 - 2 * nu[couche] + m * lb[couche]) * F[couche]              
        M1[1,3] = (2 * nu[couche] - m * lb[couche]) * F[couche]
        M1[2,3] = -(1 - m * lb[couche] )* F[couche]
        M1[3,3] = -(2 - 4 * nu[couche] + m * lb[couche]) * F[couche]
        
        MM1.append(M1)
    
        # Matrice M2 (droite)
       
        M2[0,0] = F[couche+1]
        M2[1,0] = F[couche+1]
        M2[2,0] = R[couche] * F[couche+1]
        M2[3,0] = R[couche] * F[couche+1]

        M2[0,1] = 1
        M2[1,1] = -1
        M2[2,1] = R[couche]
        M2[3,1] =-R[couche]

        M2[0,2] = -(1 - 2 * nu[couche+1] - m * lb[couche]) * F[couche+1]
        M2[1,2] = (2 * nu[couche+1] + m * lb[couche]) * F[couche+1]
        M2[2,2] = (1 + m * lb[couche]) * R[couche] * F[couche+1]
        M2[3,2] = -(2 - 4 * nu[couche+1] - m * lb[couche]) * R[couche] * F[couche+1]
        
        M2[0,3] = 1 - 2 * nu[couche+1] + m * lb[couche]
        M2[1,3] = (2 * nu[couche+1] - m * lb[couche])
        M2[2,3] = -(1 - m * lb[couche]) * R[couche]
        M2[3,3] = -(2 - 4 *nu[couche+1] + m * lb[couche]) * R[couche]
        
        MM2.append(M2)
      
   
         
        
        #  calcul de M
            
        try :
                            
            
            M_ = np.linalg.solve(M1, M2)     
            M.append(M_)
            
        except :
            a= np.linalg.det(M2) 
            texte = f'Le déterminant de M2 pour la couche {couche+1} vaut {a}'
            M.append(texte)
        
    ''' --------------------------------------- '''
    ''' calcul de la matrice de l'équation B.15 '''
    

    MM = np.identity(4, dtype=np.float64)
        
    for i in range (n-1):
        if type(M[i])=='string':
            pass
        MM=np.dot(MM, M[i])

    # MM est une matrice 4x4, il faut la réduire à une 4x2 pour trouver celle de l'équation B.15
    # toutes les lignes mais uniquement les colonnes 2(1 pour np) et 4 (3 pour np)

    ixgrid = np.ix_([0,1,2,3], [1, 3])
    MM=MM[ixgrid] # récupère le tableau 4x2 avec toutes les lignes et les colonnes 2 et 4
    
    ''' --------------------------------------- '''
    ''' calcul des valeurs An, Bn, Cn et Dn '''
    
    
    
    b11 = math.exp(-lb[0] * m)
    b21 = math.exp(-lb[0] * m)
    b12 = 1
    b22 = -1
    
    c11 = -(1 - 2 * nu[0]) * math.exp(-m * lb[0]);
    c21 = 2 * nu[0] * math.exp(-m * lb[0]);
    c12 = 1 - 2 * nu[0];
    c22 = 2 * nu[0];
    
    
    
    k11 = b11 * MM[0,0] + b12 * MM[1,0] + c11 * MM[2,0] + c12 * MM[3,0]
    k12 = b11 * MM[0,1] + b12 * MM[1,1] + c11 * MM[2,1] + c12 * MM[3,1]
    k21 = b21 * MM[0,0] + b22 * MM[1,0] + c21 * MM[2,0] + c22 * MM[3,0]
    k22 = b21 * MM[0,1] + b22 * MM[1,1] + c21 * MM[2,1] + c22 * MM[3,1]
    
    
    ''' calculs de Bn et Dn avec division par 1exx de k pour éviter overflow '''
    
    p_k11=round(math.log10(abs(k11)),0)
    p_k12=round(math.log10(abs(k12)),0)
    p_k21=round(math.log10(abs(k21)),0)
    p_k22=round(math.log10(abs(k22)),0)

    p_=min(p_k11, p_k12, p_k21, p_k22)

    p_ = 10**p_

    k11= k11 / p_
    k12= k12 / p_
    k21= k21 / p_
    k22= k22 / p_


    A=np.zeros(4,dtype=np.float64)
    B=np.zeros(4,dtype=np.float64)
    C=np.zeros(4,dtype=np.float64)
    D=np.zeros(4,dtype=np.float64)

    

    A[n-1] = 0
    B[n-1] = k22 / (k11 * k22 - k12 * k21) * (1/p_)
    C[n-1] = 0
    D[n-1] = 1 / (k12 - k22 * k11 / k21) * (1/p_)
    
    ''' version de base  
    
    
    
    A=np.zeros(4,dtype=np.float64)
    B=np.zeros(4,dtype=np.float64)
    C=np.zeros(4,dtype=np.float64)
    D=np.zeros(4,dtype=np.float64)
    
    
    A[n-1] = 0
    B[n-1] = k22 / (k11 * k22 - k12 * k21);
    C[n-1] = 0
    D[n-1] = 1 / (k12 - k22 * k11 / k21);
    
    
    '''
    
    for i in reversed(range(n-1)):
       
        
       vnp=np.vstack((A[i+1], B[i+1], C[i+1], D[i+1]))
        
       BC = np.dot(M[i], vnp)
              
       BC=np.dot(M[i],vnp)
       
        
       A[i]=BC[0]
       B[i]=BC[1]
       C[i]=BC[2]
       D[i]=BC[3]


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



''' TEST 


n=3
H=0.28
z=[0.06, 0.16, 0.28]



lb=[0.21428571428571425, 0.5714285714285714, 1.0, np.Inf]
R=[0.7, 0.8333333333333335, 239.99999999999997]
E=[7000, 10000, 12000, 50]
nu=[0.35, 0.35, 0.35, 0.35]
isbonded= 1


z_points=[0]
c_points=[0, 0, 0, 1, 2, 3]




m=20
rr=0



R=R_star(n, H, z, lb , R , E, nu, isbonded, m, z_points, rr, c_points)

'''

                 
