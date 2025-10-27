# -*- coding: utf-8 -*-
"""

@author: f.duhart
"""
'''

détermine pour une structure donnée les points à calculer
et la charge


'''
import numpy as np
from class_struct import structure, layer
from class_load import load

class calc_params :
    def __init__(self, structure : structure, load : load):
        
        
        self.struct = structure
        self.layers = self.struct.layers

        self.load = load
        
        # points de calcul
        self.z_points=self.gen_z_points()
        self.c_points=self.gen_c_points()
        self.r_points=None

        # points d'intégration
        self.mValues = None

    def define_r_points (self, r_points) :
        self.r_points=r_points

        # points d'intégration
        self.mValues = self.list_quad_m()
        
        


    # --------------------------------------
    #  METHODES POUR DETERMINATION DES POINTS DE CALCULS
    # --------------------------------------

    def gen_z_points (self) :
        z = []
        for l in self.layers :
            z.append(l.z)
        
        z = z[0:-1] # on enleve la dernier couche (substratum)
        
        c = 0.000001

        zp1=np.array(z)    
        zp2=np.array(z) + c
        zp0=np.array([0])
        
        zp = np.hstack ((zp1, zp2, zp0))
        zp=np.sort(zp)

        return zp
    
          

    def gen_c_points(self) :
        if self.z_points is not None :
        
            
            z = []
            for l in self.layers :
                z.append(l.z)
            z = z[0:-1] # on enleve la dernier couche (substratum)
            
            z=np.array(z)


            # calcul de c_points (indice de couches pour les z_points)
                        
            znp=np.hstack(([-0.0001],z))
            
            c_points=[]

            for i, zz in enumerate(self.z_points):
                couche = len(np.where(zz > znp)[0])-1
                c_points.append(couche)

            return  c_points



    ################################################################
    #  calcul des m
    ################################################################
 
    def list_m(self,  r, iteration = 25):

        a = self.load.radius
        
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

        
        
            
        return  mValue
    
    

    def quad_int (self, x1, x2):
        
        ''' 
        cette focntion renvoie les positions des points de calcul d'intgération en 4 points
        et leur poids respectifs
        
        x1, x2  : "abscisses" des points
        
        renvoie : un tableau 
            colonne 1 => les abscisses des points de calcul
            colonne 2 => les poids
            
            ''' 
        
        inter = abs(x2 - x1)    
        moy = (x2 + x1) /2
        
        tab = np.zeros((4,2))
        
        x_2=0.86114
        x_1=0.33998

        tab[0,0]=moy-x_2*inter/2
        tab[1,0]=moy-x_1*inter/2
        tab[2,0]=moy+x_1*inter/2
        tab[3,0]=moy+x_2*inter/2

        p_1=0.34786
        p_2=0.65215

        tab[0,1]= p_1 * inter/2
        tab[1,1]= p_2 * inter/2
        tab[2,1]= p_2 * inter/2
        tab[3,1]= p_1 * inter/2
        
        return tab
            

    def quad_list (self, liste) :
        '''
        Depuis une liste d'intervalle, cette focntion retourne la liste des points de calculs avec leurs poids respectifs
        '''
        
        n_inter=len(liste)-1
        
        tab=[0, 0]
        tab=np.array(tab)
        
        
        for i in range (n_inter) :
            t=self.quad_int(liste[i], liste[i+1])
            
            
            tab = np.vstack((tab,t))
            
        tab=tab[1:]    

        return tab


    def list_quad_m (self, iteration = 25):
        
                
        '''
        
        Cette focntion renvoie pour une position radiale donnée du point de calcul
        la liste des points d'intégration avec leur poids repsectifs
        
        Données d'entrée :
            a           : rayon de la charge (en m)
            r           : position radiale du point de calcul
            Htot        : hauteur totale de la structure
            iteration   : nombre d'intervalles en plus des deux premiers qui seront décomposés
            
        renvoie : un tableau 
            colonne 1 => les abscisses des points de calcul
            colonne 2 => les poids
        
                
    
        '''  

        lmq_r_points = []

        for r in self.r_points :  

            lm = self.list_m(r, iteration)
            
            lmq = self.quad_list(lm)

            lmq_r_points.append(lmq)
        
        return lmq_r_points