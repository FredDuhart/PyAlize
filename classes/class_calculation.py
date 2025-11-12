# -*- coding: utf-8 -*-
"""

@author: f.duhart
"""
'''

à documenter

'''
import pandas as pd
import numpy as np
import math
from scipy.special import j0
from scipy.special import j1

import os
import sys
sys.path.append(os.getcwd())

from classes.class_struct import structure, layer
from classes.class_calc_params import calc_params
from classes.class_load import load

class calculation :
    def __init__(self, structure : structure, params : calc_params, load : load , iteration = 25):
        self.name : str = None
        
        self.struct = structure
        #self.layers = self.struct.layers

        self.params = params
        self.load = load

        
        self.final_results = self.R_final(iteration)

    def R(self) :
        # calcul des valeurs R(i)
        
        n = len(self.struct.layers)

        R=[]
        
        # R[0] -  equations B.12a et B.12b 
        
        #R0=(E[0]/E[1])*(1+nu[1])/(1+self.struct.layers[0].poisson)
        R0=(self.struct.layers[0].module/self.struct.layers[1].module)*(1+self.struct.layers[1].poisson)/(1+self.struct.layers[0].poisson)
        R.append(R0)
        
        # R[i] pour i=1 to n-1-1  -  equations B.12a et B.12b 
        
        for i in range (n-2):
            
            #Ri = (E[i+1]/E[i+2])*(1+nu[i+2])/(1+nu[i+1])
            Ri = (self.struct.layers[i+1].module/self.struct.layers[i+2].module)*(1+self.struct.layers[i+2].poisson)/(1+self.struct.layers[i+1].poisson)
            R.append(Ri)

        return R

    def F_m(self,  m):
                     
        n = len (self.struct.layers)
                        
        ''' --------------------------------------- '''
        ''' calcul des valeurs F(i)  '''

        F=[]

        ''' F[0] '''
        ''' equations B.12a et B.12b '''
   
        #F0=math.exp(-m* (lb[0]-0))
        F0=math.exp(-m* (self.struct.layers[0].lb-0))
        F.append(F0)
        
        
        ''' F[i]  pour i=1 to n-1-1 '''
        ''' equations B.12a et B.12b '''
        
        for i in range (n-1):
            Fi = math.exp(-m* (self.struct.layers[i+1].lb-self.struct.layers[i].lb))
            F.append(Fi)
                

        return F
       
    
    def soll_star(self, ABCD, m, z_points, r_point, c_points ) :
        #initialisation de la variable de rendu
        # la variable de rendu est un dictionnaire
        

        A = ABCD[0]
        B = ABCD[1]
        C = ABCD[2]
        D = ABCD[3]
        
      


        response = {'s_z*' : [], 's_t*' : [], 's_r*' : [], 't_rz*' : [], 'w*' : [], 'u*' : []}
        

        H = self.struct.htot()
        rho=r_point/H

        n = len (self.struct.layers)
        
        for i, zz in enumerate(z_points): # boucle sur les z
            
            

            lmm = zz/H
            ii = c_points[i]
        
            # ajout d'uen couche virtuelle en fin de structure pour éviter
            # les erreurs sur la première couche => lb (i-1) = lb (-1) = 0
            #lb.append(0) # permet d'éviter les erreurs sur la première couche => lb (i-1) = lb (-1) = 0
            if ii == 0 :
                virtual_l = layer()
                virtual_l.define('virtual', None, None, None, None, n)
                virtual_l.lb = 0
                self.struct.layers.append(virtual_l)
            
            


            # pour gérer rho = 0 pour sigma t et sigma r            

            if rho == 0 :
                COEF1 = m/2 # reste à vérifier car vu nulle part !
            else :
                COEF1 = j1(m * rho) / rho            


            # sigma z
            
                
            sigma_z = -m * j0(m * rho) * ((A[ii] - C[ii] * (1 - 2 * self.struct.layers[ii].poisson - m * lmm)) * math.exp(-m * (self.struct.layers[ii].lb - lmm)) 
                                        + (B[ii] + D[ii] * (1 - 2 * self.struct.layers[ii].poisson + m * lmm)) * math.exp(-m * (lmm - self.struct.layers[ii - 1].lb))) 

            # sigma t
                        
                        
            sigma_t = COEF1 * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (self.struct.layers[ii].lb - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - self.struct.layers[ii - 1].lb))) + 2 * self.struct.layers[ii].poisson * m * j0(m * rho) * (C[ii] * math.exp(-m * (self.struct.layers[ii].lb - lmm)) - D[ii] * math.exp(-m * (lmm - self.struct.layers[ii - 1].lb)))
            
                
            # sigma r
            
            sigma_r = (m * j0( m * rho) - COEF1) * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (self.struct.layers[ii].lb - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - self.struct.layers[ii-1].lb))) + 2 * self.struct.layers[ii].poisson * m * j0( m * rho) * (C[ii] * math.exp(-m * (self.struct.layers[ii].lb - lmm)) - D[ii] * math.exp(-m * (lmm - self.struct.layers[ii - 1].lb)))

            
            
            
            # tau rz
            
            tau_rz = m * j1( m * rho) * ((A[ii] + C[ii] * (2 * self.struct.layers[ii].poisson + m * lmm)) * math.exp(-m * (self.struct.layers[ii].lb - lmm)) - (B[ii] - D[ii] * (2 * self.struct.layers[ii].poisson - m * lmm)) * math.exp(-m * (lmm - self.struct.layers[ii - 1].lb)))
            
            # w 
            
            w = -H*(1 + self.struct.layers[ii].poisson) / self.struct.layers[ii].module * j0( m * rho) * ((A[ii] - C[ii] * (2 - 4 * self.struct.layers[ii].poisson - m * lmm)) * math.exp(-m * (self.struct.layers[ii].lb - lmm)) - (B[ii] + D[ii] * (2 - 4 * self.struct.layers[ii].poisson + m * lmm)) * math.exp(-m * (lmm - self.struct.layers[ii - 1].lb)))         
            
            # u 
            
            u = H*(1 + self.struct.layers[ii].poisson) / self.struct.layers[ii].module * j1( m * rho) * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (self.struct.layers[ii].lb - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - self.struct.layers[ii - 1].lb)))

            response['s_z*'].append(sigma_z)
            response['s_t*'].append(sigma_t)
            response['s_r*'].append(sigma_r)
            response['t_rz*'].append(tau_rz)
            response['w*'].append(w)
            response['u*'].append(u)

            if ii == 0 :
                del self.struct.layers[-1]
                virtual_l = None  


                
        # fin de boucle z

        
        return response
        
    def ABCD_ub(self, m, R,  l_interface) :
        
        '''
        l_interface = liste des conditions d'interface [True ou False]
        '''

                    
        ''' --------------------------------------- '''
        ''' calcul des valeurs F(i) dépendantes de m '''
        F=self.F_m(m)
        

        # nombre de couches
        n = len (self.struct.layers)    
        
        ''' -------------- calcul de la matrice de dimensions 4n-2 x 4n-2 -----------------
        '''
        
        s_Mat = (4 * n  - 2 , 4 * n  )
        Mat = np.zeros (s_Mat, dtype=np.float64)

        
        # equations B.9 ====> condtions limites à la surface
        
        Mat[0,0] = math.exp(-self.struct.layers[0].lb * m)
        Mat[1,0] = math.exp(-self.struct.layers[0].lb * m)
        Mat[0,1] = 1
        Mat[1,1] = -1
        
        Mat[0,2] = -(1 - 2 * self.struct.layers[0].poisson) * math.exp(-m * self.struct.layers[0].lb);
        Mat[1,2] = 2 * self.struct.layers[0].poisson * math.exp(-m * self.struct.layers[0].lb);
        Mat[0,3] = 1 - 2 * self.struct.layers[0].poisson;
        Mat[1,3] = 2 * self.struct.layers[0].poisson;
        
        
        # equations B.11 ou B.17 ======> conditions d'interfaces de couches
        
        for couche in range (n-1): 
            
            # la premiere ligne est la troisième => indice = 2
            # ligne1 = 2 + (couche)*4
            
            lig = 2 + couche * 4
            col = couche * 4
            
            
            if l_interface[couche] :#] interface collée
                            
                # partie gauche
                Mat[lig+0,col+0]=1
                Mat[lig+1,col+0]=1
                Mat[lig+2,col+0]=1
                Mat[lig+3,col+0]=1
        
                Mat[lig+0,col+1] = F[couche]
                Mat[lig+1,col+1] = -F[couche]
                Mat[lig+2,col+1] = F[couche]
                Mat[lig+3,col+1] = -F[couche]
                
                Mat[lig+0,col+2] = -(1 - 2 * self.struct.layers[couche].poisson - m * self.struct.layers[couche].lb)
                Mat[lig+1,col+2] = (2 * self.struct.layers[couche].poisson + m * self.struct.layers[couche].lb)
                Mat[lig+2,col+2] = 1 + m * self.struct.layers[couche].lb
                Mat[lig+3,col+2] = -(2 - 4 * self.struct.layers[couche].poisson - m * self.struct.layers[couche].lb)
        
                Mat[lig+0,col+3] = (1 - 2 * self.struct.layers[couche].poisson + m * self.struct.layers[couche].lb) * F[couche]              
                Mat[lig+1,col+3] = (2 * self.struct.layers[couche].poisson - m * self.struct.layers[couche].lb) * F[couche]
                Mat[lig+2,col+3] = -(1 - m * self.struct.layers[couche].lb )* F[couche]
                Mat[lig+3,col+3] = -(2 - 4 * self.struct.layers[couche].poisson + m * self.struct.layers[couche].lb) * F[couche]
                
                
                # partie droite
            
                Mat[lig+0,col+4+0] = -F[couche+1]  
                Mat[lig+1,col+4+0] = -F[couche+1]
                Mat[lig+2,col+4+0] = -R[couche] * F[couche+1]  
                Mat[lig+3,col+4+0] = -R[couche] * F[couche+1]
        
                Mat[lig+0,col+4+1] = -1  
                Mat[lig+1,col+4+1] = 1
                Mat[lig+2,col+4+1] = -R[couche]  
                Mat[lig+3,col+4+1] = R[couche]
        
                Mat[lig+0,col+4+2] = (1 - 2 * self.struct.layers[couche+1].poisson - m * self.struct.layers[couche].lb) * F[couche+1]  
                Mat[lig+1,col+4+2] = -(2 * self.struct.layers[couche+1].poisson + m * self.struct.layers[couche].lb) * F[couche+1]
                Mat[lig+2,col+4+2] = -(1 + m * self.struct.layers[couche].lb) * R[couche] * F[couche+1]
                Mat[lig+3,col+4+2] = (2 - 4 * self.struct.layers[couche+1].poisson - m * self.struct.layers[couche].lb) * R[couche] * F[couche+1]
                
                Mat[lig+0,col+4+3] = -(1 - 2 * self.struct.layers[couche+1].poisson + m * self.struct.layers[couche].lb)  
                Mat[lig+1,col+4+3] = -((2 * self.struct.layers[couche+1].poisson - m * self.struct.layers[couche].lb))
                Mat[lig+2,col+4+3] = (1 - m * self.struct.layers[couche].lb) * R[couche]  
                Mat[lig+3,col+4+3] = (2 - 4 *self.struct.layers[couche+1].poisson + m * self.struct.layers[couche].lb) * R[couche]
                
                
            
            elif not (l_interface[couche]): # cas glissant
                zro = 0  #?+ 1e-50
            
                # partie gauche
                    
                Mat[lig+0,col+0] = 1
                Mat[lig+1,col+0] = 1
                Mat[lig+2,col+0] = 1
                Mat[lig+3,col+0] = zro
                
                Mat[lig+0,col+1] = F[couche]
                Mat[lig+1,col+1] = F[couche]
                Mat[lig+2,col+1] = -F[couche]
                Mat[lig+3,col+1] = zro
                
                Mat[lig+0,col+2] = -(1 - 2 * self.struct.layers[couche].poisson - m * self.struct.layers[couche].lb)
                Mat[lig+1,col+2] = 1 + m * self.struct.layers[couche].lb
                Mat[lig+2,col+2] = 2*self.struct.layers[couche].poisson + m * self.struct.layers[couche].lb
                Mat[lig+3,col+2] = zro
                
                Mat[lig+0,col+3] = (1 - 2 * self.struct.layers[couche].poisson + m * self.struct.layers[couche].lb) * F[couche]
                Mat[lig+1,col+3] = -(1 - m * self.struct.layers[couche].lb) * F[couche]
                Mat[lig+2,col+3] = (2 * self.struct.layers[couche].poisson - m * self.struct.layers[couche].lb) * F[couche]
                Mat[lig+3,col+3] = zro 
        
                # partie droite
                
                Mat[lig+0,col+4+0] = -F[couche+1]  
                Mat[lig+1,col+4+0] = -R[couche]*F[couche+1]
                Mat[lig+2,col+4+0] = zro  
                Mat[lig+3,col+4+0] = -F[couche+1]
                    
                Mat[lig+0,col+4+1] = -1  
                Mat[lig+1,col+4+1] = -R[couche]
                Mat[lig+2,col+4+1] = zro  
                Mat[lig+3,col+4+1] = 1
                
                Mat[lig+0,col+4+2] = (1 - 2 * self.struct.layers[couche+1].poisson - m * self.struct.layers[couche].lb) * F[couche+1]
                Mat[lig+1,col+4+2] = -(1 + m * self.struct.layers[couche].lb) * R[couche] * F[couche+1]
                Mat[lig+2,col+4+2] = zro
                Mat[lig+3,col+4+2] = -(2 * self.struct.layers[couche+1].poisson + m * self.struct.layers[couche].lb) * F[couche+1]
                
                Mat[lig+0,col+4+3] = -(1 - 2 * self.struct.layers[couche+1].poisson + m * self.struct.layers[couche].lb)
                Mat[lig+1,col+4+3] = (1 - m * self.struct.layers[couche].lb) * R[couche]
                Mat[lig+2,col+4+3] = zro
                Mat[lig+3,col+4+3] = -(2*self.struct.layers[couche+1].poisson - m*self.struct.layers[couche].lb)
                
        
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
        
        try :

            res = np.linalg.solve(Mat_fin, vect_droite)
            
        except Exception as e:
            print ( f"Échec dans la résolution : {e}")
        
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

        ABCD = []
        ABCD.append(A)
        ABCD.append(B)
        ABCD.append(C)
        ABCD.append(D)  
        
        return ABCD
    
    
    # --------------------------------------
    #  METHODE FINALE
    # --------------------------------------
    def R_final (self, iteration = 25) :
              
        
        isbonded =[]
        for l in self.struct.layers :
            isbonded.append(l.interface)
        
        isbonded = isbonded [0:-1]
        
       
        '''
        Données d'entrées :
            Self.load.load
                q          : charge (en MPa)
                a          : rayon de la charge (en m)
            self.struct.layers
                th         : épaisseurs des couches (en m) - liste de taille (n-1) - la dernière couche est semi-infinie
                E          : Modules des n couches (en MPa) - liste de taille (n)
                nu         : Coefficient de poisson (sans unité) - liste de taille (n)
                isbonded   : True si interface collée - False si interface glissante
                            pour l'instant soit tout est collé soit tout es glissnat ====> évolution à venir
            self.params       
                z_points   : liste des z des points à calculer (en m)                    
                r_points   : liste des r (rayons) des points à calculer (en m)                    
        
            iteration  : nombre d'intervalles d'integration 
        
        Retrun :
            Un DataFrame (Pandas) 
                avec une double indexation en colonnes (sollicitations x positions radiales)
                    sollicitations = 's_z', 's_t' , 's_r' , 't_rz', 'w', 'u', 'e_z', 'e_t', 'e_r', 'E'}
                    positions radiales = celles de r_points
                avec une double indexation en lignes (z x couche)
                    z = celui de z_points
                    couche = celle de c_points
        
        '''
        
        
        

        ''' ---------------------------------------------------------------------------------
            cas des interfaces semi-collées
        '''

        if 1 in isbonded : # si il y a des interfaces semi-collées
            l_interface=[]
            l_interface.append( [True if x==0 else False for x in isbonded]) # cas glissant
            l_interface.append( [False if x==2 else True for x in isbonded]) # cas collé
        else : 
            l_interface=[]
            l_interface.append( [True if x==0 else False for x in isbonded]) 
            

        
        # CALCULS INDEPENDANTS DES CONDITIONS D'INTERFACE ------
    
        # charge
        q = self.load.load
        a = self.load.radius

        # structure
        th = []
        E = []
        nu = []
        isbonded =[]
        z = []
        for l in self.struct.layers :
            th.append(l.thickness)
            E.append(l.module)
            nu.append(l.poisson)
            z.append(l.z)
        th = th [0:-1]
               
        # points de calculs
        z_points = self.params.z_points
        r_points = self.params.r_points

        
        
        ''' -------------------------------------------------------------------------------------
            Calculs préalables 
        '''    
               
        # calcul de H (hauteur de la structure) 
        H= self.struct.htot()
        
                
        # calcul de c_points (indice de couches pour les z_points)
        c_points = self.params.c_points

        # calcul des valeurs de E et nu pour chaque z_point
        EE = []
        vv = []
        for jj in c_points:
            EE.append(E[jj])
            vv.append(nu[jj])
        EE=np.array(EE) # module pour la couche
        vv=np.array(vv) # nu pour la couche
        
        
        # calcul des valeurs R(i)
        #    on en calcule pas F(i) car dépendant de la valeur de m 
        R_ = self.R()
        
        # calcul de alpha
        alpha = a/H

        ''' ---------------------------------------------------------------------------------
            Boucle sur les conditions d'interface
        '''
        responses =[]
        
        for ii, l_inter in enumerate(l_interface) :
            print (f' CALCUL # {ii+1} ------+++++ taille responses = {len(responses)}')
            ''' ---------------------------------------------------------------------------------
                Boucle sur les valeurs de r_points
            '''
            
            response={'s_z' : [], 's_t' : [], 's_r' : [], 't_rz' : [], 'w' : [], 'u' : [], 'e_z' : [], 'e_t' : [], 'e_r' : [], }
            
            for i , rr in enumerate( r_points) :
                
                # calcul des points d'intégration pour une position r
                l_quad_r=self.params.mValues[i] 
                        
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
                    
                    #print (f'itération n°{k}')
                    m=couple_m[0]
                    poids_m = couple_m[1]
                    
                    ABCD = self.ABCD_ub(m, R_, l_inter) # il va falloir itérer sur L_inetrface si semi-collée
                    rstar =  self.soll_star(ABCD, m, z_points, rr, c_points )
                    
                    # Récupération des valeurs pour itréation - 1           
                    if k == (k_max)-4 : # 4 car les intervalles d'intégrations sont divisés en 4
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
                
                # ajout aux tableaux
                response['s_z'].append(sig_z)
                response['s_t'].append(sig_t)
                response['s_r'].append(sig_r)
                response['t_rz'].append(tau_rz)
                response['w'].append(w)
                response['u'].append(u)
                response['e_z'].append(e_z)
                response['e_t'].append(e_t)
                response['e_r'].append(e_r)
                
            responses.append(response)

            print (f' FIN CALCUL # {ii +1} ------+++++ taille responses = {len(responses)}')


        # responses est donc une liste de 1 à 2 dictionnaires


        
        # moyenne des résulats des un ou deux calculs sur les conditions d'interface
        
        # A FAIRE !!!
        df = self.responses_to_df(responses)
        
        return df


    def responses_to_df(self, responses) :

        a_conv=[]
        print(f'il y a eu {len(responses)} calculs')
        for response in responses :

            l_conv = []
            keys = list(response.keys())

            for key in keys :
                cols = response[key]
                for i, col  in enumerate(cols) :
                    col = list(col)
                    l_conv.append(col)

            a_conv.append(np.array(l_conv).T)

        a_conv_ = sum(a_conv) / len (a_conv)


        columns = pd.MultiIndex.from_product([keys, self.params.r_points], names=["Sollicitations", "r (m)"])
        df = pd.DataFrame(a_conv_, columns = columns)
        df.index = pd.MultiIndex.from_arrays([self.params.c_points, self.params.z_points], names=['couche', 'z (m)'])

        return df



    