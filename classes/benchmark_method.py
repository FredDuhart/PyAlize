from class_struct import *
from class_calculation import *
from class_calc_params import *
from class_load import load

from tabulate import tabulate
from IPython.display import display

from class_exports import res_to_tabulate, export_results

import os

'''
n=3
H=0.28
z=[0.06, 0.16, 0.28]



lb=[0.21428571428571425, 0.5714285714285714, 1.0, np.inf]
R=[0.7, 0.8333333333333335, 239.99999999999997]
E=[7000, 10000, 12000, 50]
nu=[0.35, 0.35, 0.35, 0.35]
isbonded= 1
'''
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



# chargement ****************************
disj = 0.375
#disj = 0 
load_ = load(disj = disj)


# paramètres de calcul ***********************

params = calc_params(struct, load_)

#params.add_z_points(0.02)


# distance entre les deux roues du jumelage
rp=[0] 
if load_.type == 'jumelage' :
    rp = [0, disj/2, disj]

#, disj/2, disj]#, disj/2]#, disj]
params.define_r_points (rp)

# benchmark *****************************************************


import time
it = 500

t_m1 =[]
t_m2 = []

for i in range (it) :

    t0 = time.perf_counter()
    resultats = calculation(struct, params, load_, forced = False)
    t1 =time.perf_counter()
    del resultats

    t_m1.append(t1 - t0)

    t0 = time.perf_counter()
    resultats = calculation(struct, params, load_, forced = True)
    t1 =time.perf_counter()
    del resultats

    t_m2.append(t1-t0)

print (f'La méthode optimisée a mis {sum(t_m1)/len(t_m1)*1000} ms en moyenne sur {it} itérations.')
print (f'La méthode complète  a mis {sum(t_m2)/len(t_m2)*1000} ms en moyenne sur {it} itérations.')

