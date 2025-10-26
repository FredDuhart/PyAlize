# -*- coding: utf-8 -*-
"""

@author: f.duhart
"""
'''

à documenter

'''
import numpy as np
import math
from scipy.special import j0
from scipy.special import j1

from class_struct import structure, layer
from class_calc_params import calc_params
from class_load import load

class calculation :
    def __init__(self, structure : structure, params : calc_params, load : load , iteration = 25):
        self.name : str = None
        
        self.struct = structure
        self.layers = self.struct.layers

        self.params = params
        self.load = load

        self.mValues = self.list_m(iteration)


    ################################################################
    #  calcul des m
    ################################################################
 
    def list_m(self,  iteration = 25):

        a = self.load.radius
        r_list = self.params.r_points 
        Htot = self.struct.htot()

        '''
        
        Cette focntion renvoie pour une position radiale donnée du poitn de calcul
        la liste des points m  constituant les intervalles d'intégration
        
        Données d'entrée :
            a           : rayon de la charge (en m)
            r           : position radiale du point de calcul
            Htot        : hauteur totale de la structure
            iteration   : nombre d'intervalles en plus des deux premiers qui seront décomposés
            
        Renvoie : liste des intervalles m
        
        '''
        mValues = []
        
        for r in r_list : 

            # dans pymastic x== 0 est transformé en x = 1e-16 ---- > à voir plus tard si utile
            
            if r ==0 :
                r = 1e-16
            if a == 0 :
                a = 1e-16
            
            #liste des 0 pour bessel_j0 et bessel_j1
            
            firstKindFirstOrder = np.array([3.83170597020751,7.01558666981562,10.1734681350627,13.3236919363142,16.4706300508776,19.6158585104682,22.7600843805928, 25.9036720876184,29.0468285349169,32.1896799109744,35.3323075500839,38.4747662347716,41.6170942128145,44.759318997652, 47.9014608871855,51.0435351835715,54.1855536410613,57.3275254379010,60.4694578453475,63.6113566984812,66.7532267340985, 69.8950718374958,73.0368952255738,76.1786995846415,79.3204871754763,82.4622599143736,85.6040194363502,88.7457671449263, 91.8875042516950,95.0292318080447,98.1709507307908,101.312661823039,104.454365791283,107.596063259509,110.737754780899,113.879440847595,117.021121898892,120.162798328149,123.304470488636,126.446138698517,129.587803245104,132.729464388510,135.871122364789,139.012777388660,142.154429655859,145.296079345196,148.437726620342,151.579371631401,154.721014516286,157.862655401930,161.004294405362,164.145931634650,167.287567189744,170.429201163227,173.570833640976,176.712464702764,179.854094422788,182.995722870153,186.137350109296,189.278976200376,192.420601199626,195.562225159663,198.703848129777,201.845470156191,204.987091282292,208.128711548850,211.270330994208,214.411949654462,217.553567563624,220.695184753769,223.836801255172,226.978417096429,230.120032304579,233.261646905201,236.403260922514,239.544874379470,242.686487297829,245.828099698240,248.969711600310,252.111323022669,255.252933983028,258.394544498240,261.536154584344,264.677764256622,267.819373529635,270.960982417271,274.102590932781,277.244199088815,280.385806897456,283.527414370251,286.669021518243,289.810628351994,292.952234881614,296.093841116782,299.235447066774,302.377052740478,305.518658146416,308.660263292764, 311.801868187371,314.943472837767])
            firstKindZeroOrder = np.array([2.40482555769577,5.52007811028631,8.65372791291101,11.7915344390143,14.9309177084878,18.0710639679109, 21.2116366298793,24.3524715307493,27.4934791320403,30.6346064684320,33.7758202135736,36.9170983536640,40.0584257646282, 43.1997917131767,46.3411883716618,49.4826098973978,52.6240518411150,55.7655107550200,58.9069839260809,62.0484691902272, 65.1899648002069,68.3314693298568,71.4729816035937,74.6145006437018,77.7560256303881,80.8975558711376,84.0390907769382, 87.1806298436412,90.3221726372105,93.4637187819448,96.6052679509963,99.7468198586806,102.888374254195,106.029930916452, 109.171489649805,112.313050280495,115.454612653667,118.596176630873,121.737742087951,124.879308913233,128.020877006008, 131.162446275214,134.304016638305,137.445588020284,140.587160352854,143.728733573690,146.870307625797,150.011882456955, 153.153458019228,156.295034268534,159.436611164263,162.578188668947,165.719766747955,168.861345369236,172.002924503078, 175.144504121903,178.286084200074,181.427664713731,184.569245640639,187.710826960049,190.852408652582,193.993990700109, 197.135573085661,200.277155793332,203.418738808199,206.560322116244,209.701905704294,212.843489559950,215.985073671534, 219.126658028041,222.268242619084,225.409827434859,228.551412466099,231.692997704039,234.834583140383,237.976168767276, 241.117754577268,244.259340563296,247.400926718653,250.542513036970,253.684099512193,256.825686138564,259.967272910605, 263.108859823096,266.250446871066,269.392034049776,272.533621354705,275.675208781537,278.816796326153,281.958383984615, 285.099971753160,288.241559628188,291.383147606255,294.524735684065,297.666323858459,300.807912126411,303.949500485021, 307.091088931505,310.232677463195,313.374266077528])
            
            rho = r/Htot
            alpha = a/Htot   
            
            firstKindZeroOrder = firstKindZeroOrder / rho
            firstKindFirstOrder = firstKindFirstOrder / alpha
            
            BesselZeros = np.hstack(([0], firstKindZeroOrder,firstKindFirstOrder))
            BesselZeros = np.sort(BesselZeros)
            
            D1 = (BesselZeros[1]-BesselZeros[0]) / 6 #- 0.00001
            D2 = (BesselZeros[2]-BesselZeros[1]) / 2 #- 0.00001
            
            AUX1 = np.arange(BesselZeros[0], BesselZeros[1], D1)
            AUX2 = np.arange(BesselZeros[1], BesselZeros[2], D2)
            
            mValue = np.hstack((AUX1, AUX2, BesselZeros[3:iteration+1]))
            mValue = np.sort(mValue)

            mValues.append(mValue) # pour une position radiale
        
            
        return  mValues

  


    def R(self) :
        # calcul des valeurs R(i)
        
        n = len(self.layers)

        R=[]
        
        # R[0] -  equations B.12a et B.12b 
        
        #R0=(E[0]/E[1])*(1+nu[1])/(1+nu[0])
        R0=(self.layers[0].module/self.layers[1].module)*(1+self.layers[1].poisson)/(1+self.layers[0].poisson)
        R.append(R0)
        
        # R[i] pour i=1 to n-1-1  -  equations B.12a et B.12b 
        
        for i in range (n-2):
            
            #Ri = (E[i+1]/E[i+2])*(1+nu[i+2])/(1+nu[i+1])
            Ri = (self.layers[i+1].module/self.layers[i+2].module)*(1+self.layers[i+2].poisson)/(1+self.layers[i+1].poisson)
            R.append(Ri)

        return R

    def F_m(self,  m):
                     
        n = len (self.layers)
                        
        ''' --------------------------------------- '''
        ''' calcul des valeurs F(i)  '''

        F=[]

        ''' F[0] '''
        ''' equations B.12a et B.12b '''
   
        #F0=math.exp(-m* (lb[0]-0))
        F0=math.exp(-m* (self.layers[0].lb-0))
        F.append(F0)
        
        
        ''' F[i]  pour i=1 to n-1-1 '''
        ''' equations B.12a et B.12b '''
        
        for i in range (n-2):
            Fi = math.exp(-m* (self.layers[i+1].lb-self.layers[i].lb))
            F.append(Fi)
                

        return F
       
    def MMMM (self, R, F, m) : #all bonded
            
        n = len (self.layers)
        ''' --------------------------------------- '''
        ''' calcul des matrices de l'équation B.11 '''

        MM1=[]
        MM2=[]
        M=[]
        
        for couche in range(n-2): # toutes les couches sauf le substratum

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
            
            M1[0,2] = -(1 - 2 * self.layers[couche].poisson - m * self.layers[couche].lb)
            M1[1,2] = (2 * self.layers[couche].poisson + m * self.layers[couche].lb)
            M1[2,2] = 1 + m * self.layers[couche].lb
            M1[3,2] = -(2 - 4 * self.layers[couche].poisson - m * self.layers[couche].lb)

            M1[0,3] = (1 - 2 * self.layers[couche].poisson + m * self.layers[couche].lb) * F[couche]              
            M1[1,3] = (2 * self.layers[couche].poisson - m * self.layers[couche].lb) * F[couche]
            M1[2,3] = -(1 - m * self.layers[couche].lb )* F[couche]
            M1[3,3] = -(2 - 4 * self.layers[couche].poisson + m * self.layers[couche].lb) * F[couche]
            
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

            M2[0,2] = -(1 - 2 * self.layers[couche+1].poisson - m * self.layers[couche].lb) * F[couche+1]
            M2[1,2] = (2 * self.layers[couche+1].poisson + m * self.layers[couche].lb) * F[couche+1]
            M2[2,2] = (1 + m * self.layers[couche].lb) * R[couche] * F[couche+1]
            M2[3,2] = -(2 - 4 * self.layers[couche+1].poisson - m * self.layers[couche].lb) * R[couche] * F[couche+1]
            
            M2[0,3] = 1 - 2 * self.layers[couche+1].poisson + m * self.layers[couche].lb
            M2[1,3] = (2 * self.layers[couche+1].poisson - m * self.layers[couche].lb)
            M2[2,3] = -(1 - m * self.layers[couche].lb) * R[couche]
            M2[3,3] = -(2 - 4 *self.layers[couche+1].poisson + m * self.layers[couche].lb) * R[couche]
            
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
            
        for i in range (n-2):
            if type(M[i])=='string':
                pass
            MM=np.dot(MM, M[i])

        # MM est une matrice 4x4, il faut la réduire à une 4x2 pour trouver celle de l'équation B.15
        # toutes les lignes mais uniquement les colonnes 2(1 pour np) et 4 (3 pour np)

        ixgrid = np.ix_([0,1,2,3], [1, 3])
        MM=MM[ixgrid] # récupère le tableau 4x2 avec toutes les lignes et les colonnes 2 et 4



        return M, MM

    def ABCD (self, M, MM, m) :

        n = len(self.layers)
        ''' --------------------------------------- '''
        ''' calcul des valeurs An, Bn, Cn et Dn '''
        
        
        
        b11 = math.exp(-self.layers[0].lb * m)
        b21 = math.exp(-self.layers[0].lb * m)
        b12 = 1
        b22 = -1

        
        
        c11 = -(1 - 2 * self.layers[0].poisson) * math.exp(-m * self.layers[0].lb)
        c21 = 2 * self.layers[0].poisson * math.exp(-m * self.layers[0].lb)
        c12 = 1 - 2 * self.layers[0].poisson
        c22 = 2 * self.layers[0].poisson
        
        
        
        
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

        

        A[n-2] = 0
        B[n-2] = k22 / (k11 * k22 - k12 * k21) * (1/p_)
        C[n-2] = 0
        D[n-2] = 1 / (k12 - k22 * k11 / k21) * (1/p_)
        
        for i in reversed(range(n-2)):
            
                
            vnp = np.vstack((A[i+1], B[i+1], C[i+1], D[i+1]))

            print ('Class')
            print (f'couche {i}')
            print (vnp)
            print (M[i])
            print()

                  
            BC = np.dot(M[i], vnp)
            
                
            A[i]=BC[0]
            B[i]=BC[1]
            C[i]=BC[2]
            D[i]=BC[3]

        ABCD = []
        ABCD.append(A)
        ABCD.append(B)
        ABCD.append(C)
        ABCD.append(D)
        

        return ABCD
    
    def soll_star(self, ABCD, m, z_points, r_point, c_points ) :
        #initialisation de la variable de rendu
        # la variable de rendu est un dictionnaire
        
        A = ABCD[0]
        B = ABCD[1]
        C = ABCD[2]
        D = ABCD[3]


        response = {'s_z*' : [], 's_t*' : [], 's_r*' : [], 't_rz*' : [], 'w*' : [], 'u*' : []}
        

        H = self.htot()
        rho=r_point/H
        
        for i, zz in enumerate(z_points): # boucle sur les z
            
            n = len (self.layers)

            lmm = zz/H
            ii = c_points[i]
        
            # ajout d'uen couche virtuelle en fin de structure pour éviter
            # les erreurs sur la première couche => lb (i-1) = lb (-1) = 0
            #lb.append(0) # permet d'éviter les erreurs sur la première couche => lb (i-1) = lb (-1) = 0

            virtual_l = layer()
            virtual_l.define('virtual', None, None, None, None, n)
            virtual_l.lb = 0
            self.layers.append(virtual_l)
            


            # pour gérer rho = 0 pour sigma t et sigma r            

            if rho == 0 :
                COEF1 = m/2 # reste à vérifier car vu nulle part !
            else :
                COEF1 = j1(m * rho) / rho            


            # sigma z
            
                
            sigma_z = -m * j0(m * rho) * ((A[ii] - C[ii] * (1 - 2 * self.layers[ii].poisson - m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) 
                                        + (B[ii] + D[ii] * (1 - 2 * self.layers[ii].poisson + m * lmm)) * math.exp(-m * (lmm - self.layers[ii - 1].lb))) 

            # sigma t
                        
                        
            sigma_t = COEF1 * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - self.layers[ii - 1].lb))) + 2 * self.layers[ii].poisson * m * j0(m * rho) * (C[ii] * math.exp(-m * (self.layers[ii].lb - lmm)) - D[ii] * math.exp(-m * (lmm - self.layers[ii - 1].lb)))
            
                
            # sigma r
            
            sigma_r = (m * j0( m * rho) - COEF1) * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - self.layers[ii-1].lb))) + 2 * self.layers[ii].poisson * m * j0( m * rho) * (C[ii] * math.exp(-m * (self.layers[ii].lb - lmm)) - D[ii] * math.exp(-m * (lmm - self.layers[ii - 1].lb)))

            
            
            
            # tau rz
            
            tau_rz = m * j1( m * rho) * ((A[ii] + C[ii] * (2 * self.layers[ii].poisson + m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) - (B[ii] - D[ii] * (2 * self.layers[ii].poisson - m * lmm)) * math.exp(-m * (lmm - self.layers[ii - 1].lb)))
            
            # w 
            
            w = -H*(1 + self.layers[ii].poisson) / self.layers[ii].module * j0( m * rho) * ((A[ii] - C[ii] * (2 - 4 * self.layers[ii].poisson - m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) - (B[ii] + D[ii] * (2 - 4 * self.layers[ii].poisson + m * lmm)) * math.exp(-m * (lmm - self.layers[ii - 1].lb)))         
            
            # u 
            
            u = H*(1 + self.layers[ii].poisson) / self.layers[ii].module * j1( m * rho) * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - self.layers[ii - 1].lb)))

            response['s_z*'].append(sigma_z)
            response['s_t*'].append(sigma_t)
            response['s_r*'].append(sigma_r)
            response['t_rz*'].append(tau_rz)
            response['w*'].append(w)
            response['u*'].append(u)

                
        # fin de boucle z

        
        return response
        
        
        
    def soll_star_unique(self, ABCD, m, z_point, c_point, rho) :
        # args
        #   ABCD = coefficent A B C et D pour les n couches et ue valeur de m (i.e. de r)
        #   m = borne d'intégration
        #   z_point = profondeur du point calculé
        #   c_point = indice de la couche dans laquelle se situe z_point
        #   rho = r_point / H 
        # return
        #   dictionnaire des sollicitations* pour un r et un z donné, et une valeur de m
        #   {'s_z*' : [], 's_t*' : [], 's_r*' : [], 't_rz*' : [], 'w*' : [], 'u*' : []}



        #initialisation de la variable de rendu
        # la variable de rendu est un dictionnaire
        
        A = ABCD[0]
        B = ABCD[1]
        C = ABCD[2]
        D = ABCD[3]


        response = {'s_z*' : [], 's_t*' : [], 's_r*' : [], 't_rz*' : [], 'w*' : [], 'u*' : []}
        

        H = self.htot()
        #rho=r_point/H # à passer en argument
                       
        n = len (self.layers)

        lmm = z_point/H
        ii = c_point
    
        # ajout d'uen couche virtuelle en fin de structure pour éviter
        # les erreurs sur la première couche => lb (i-1) = lb (-1) = 0
        if ii == 0 :
            virtual_l = layer()
            virtual_l.define('virtual', None, None, None, None, n)
            virtual_l.lb = 0
            self.layers.append(virtual_l)
        


        # pour gérer rho = 0 pour sigma t et sigma r            

        if rho == 0 :
            COEF1 = m/2 # reste à vérifier car vu nulle part !
        else :
            COEF1 = j1(m * rho) / rho            


        # sigma z
        
            
        sigma_z = -m * j0(m * rho) * ((A[ii] - C[ii] * (1 - 2 * self.layers[ii].poisson - m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) 
                                    + (B[ii] + D[ii] * (1 - 2 * self.layers[ii].poisson + m * lmm)) * math.exp(-m * (lmm - self.layers[ii - 1].lb))) 

        # sigma t
                    
                    
        sigma_t = COEF1 * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - self.layers[ii - 1].lb))) + 2 * self.layers[ii].poisson * m * j0(m * rho) * (C[ii] * math.exp(-m * (self.layers[ii].lb - lmm)) - D[ii] * math.exp(-m * (lmm - self.layers[ii - 1].lb)))
        
            
        # sigma r
        
        sigma_r = (m * j0( m * rho) - COEF1) * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - self.layers[ii-1].lb))) + 2 * self.layers[ii].poisson * m * j0( m * rho) * (C[ii] * math.exp(-m * (self.layers[ii].lb - lmm)) - D[ii] * math.exp(-m * (lmm - self.layers[ii - 1].lb)))

        
        
        
        # tau rz
        
        tau_rz = m * j1( m * rho) * ((A[ii] + C[ii] * (2 * self.layers[ii].poisson + m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) - (B[ii] - D[ii] * (2 * self.layers[ii].poisson - m * lmm)) * math.exp(-m * (lmm - self.layers[ii - 1].lb)))
        
        # w 
        
        w = -H*(1 + self.layers[ii].poisson) / self.layers[ii].module * j0( m * rho) * ((A[ii] - C[ii] * (2 - 4 * self.layers[ii].poisson - m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) - (B[ii] + D[ii] * (2 - 4 * self.layers[ii].poisson + m * lmm)) * math.exp(-m * (lmm - self.layers[ii - 1].lb)))         
        
        # u 
        
        u = H*(1 + self.layers[ii].poisson) / self.layers[ii].module * j1( m * rho) * ((A[ii] + C[ii] * (1 + m * lmm)) * math.exp(-m * (self.layers[ii].lb - lmm)) + (B[ii] - D[ii] * (1 - m * lmm)) * math.exp(-m * (lmm - self.layers[ii - 1].lb)))

        response['s_z*'].append(sigma_z)
        response['s_t*'].append(sigma_t)
        response['s_r*'].append(sigma_r)
        response['t_rz*'].append(tau_rz)
        response['w*'].append(w)
        response['u*'].append(u)

        if ii == 0 :
            del self.layers[-1]
            virtual_l = None  
        
        return response
    
    # --------------------------------------
    #  METHODES POUR DETERMINATION DES POINTS DE CALCULS
    # --------------------------------------

    def gen_z_points (self) :
        th = []
        for l in self.layers :
            th.append(l.thickness)
        th = th[0:-1] # on enleve l'apaisseur de la dernier couche (substratum)
        
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

        self.z_points = zp    

    def gen_c_points(self, z_points) :
        th = []
        for l in self.layers :
            th.append(l.thickness)
        th = th[0:-1] # on enleve l'apaisseur de la dernier couche (substratum)
        
        # calcul de z(i) 

        th=np.array(th)    
        z=[]
        for i, e in enumerate(th) :

            z.append(np.sum(th[0:i+1]))
        
        z=np.array(z)


        # calcul de c_points (indice de couches pour les z_points)
                    
        znp=np.hstack(([-0.0001],z))
        
        c_points=[]

        for i, zz in enumerate(z_points):
            couche = len(np.where(zz > znp)[0])-1
            c_points.append(couche)

        self.c_points =  c_points

    # --------------------------------------
    #  METHODE FINALE
    # --------------------------------------



    def R_final (self, iteration = 25) :
        # charge
        q = self.load.load
        a = self.load.radius

        # structure
        th = []
        E = []
        nu = []
        isbonded =[]
        z = []
        for l in self.layers :
            th.append(l.thickness)
            E.append(l.module)
            nu.append(l.poisson)
            isbonded.append(l.interface)
            z.append(l.z)
        th = th [0:-1]
        isbonded = isbonded [0:-1]
        
        # points de calculs
        z_points = self.params.z_points
        r_points = self.params.r_points

        '''
        Données d'entrées :
            q          : charge (en MPa)
            a          : rayon de la charge (en m)
            
            th         : épaisseurs des couches (en m) - liste de taille (n-1) - la dernière couche est semi-infinie
            E          : Modules des n couches (en MPa) - liste de taille (n)
            nu         : Coefficient de poisson (sans unité) - liste de taille (n)
            isbonded   : True si interface collée - False si interface glissante
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
        
        
        # calcul de H (hauteur de la structure) 

        H= self.struct.htot()
        
        # toutes les couches sont elles collées ?
        
        isb = np.array(isbonded)
        # if isb.sum() == len (isb)  :
        #     all_bonded = True
        
        # if all_bonded :
        #     print ('toutes les couches sont collées ! ')
        # else :
        #     print ('au moins une glissante')
        
        
        # calcul de c_points (indice de couches pour les z_points)
                    
        c_points = self.params.c_points

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
        lb=self.struct.lb
                    
        
        # calcul des valeurs R(i)
        #    on en calcule pas F(i) car dépendant de la valeur de m 
        
        R = self.R()
        
        # calcul de alpha
        
        alpha = a/H
         
        ''' ---------------------------------------------------------------------------------
            Boucle sur les valeurs de r_points
        '''
        

        ############################################ ON EST ICI #######################################
        # il faut revoir la liste des m !!!!!!



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
                        
                if isb.sum() != len (isb) : # cas ou toutes les interfaces ne sont pas collées
                                
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
