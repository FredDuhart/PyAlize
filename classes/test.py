from class_struct import *
from class_calculation import *
from class_calc_params import *
from class_load import load

from tabulate import tabulate
from IPython.display import display

from export_results import res_to_tabulate

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

print(' ----------------- STRUCTURE ----------------')
for l in struct.layers :
    print (f'{l.order}  {l.name}   {l.thickness} m    {l.module} Mpa  {l.poisson} Collée = {l.interface}    z = {l.z}   lambda = {l.lb}')


# chargement ****************************

load_ = load()
print ('---- paramètres de charge -------')
type = 'roue simple'
if load_.disj >0 : type ='jumelage'
print (f'type = {type}')
print ('q (MPa) = ', load_.load)
print ('rayon (m) = ', load_.radius)



# paramètres de calcul

params = calc_params(struct, load_)

params.add_z_points(0.02)


disj =0.375 # distance entre les deux roues du jumelage
rp=[0, disj/2, disj]#, disj/2]#, disj]
params.define_r_points (rp)

# Calculs *****************************************************


resultats = calculation(struct, params, load_)
res  = resultats.final_results


def res_jum (res, rr) :
    
    solls = ['s_z','s_t','s_r','t_rz','w','u','e_z','e_t','e_r']
    
    for soll in solls :
        for i, r in enumerate(rr) :
            res[soll, r] = res[soll, r] + res[soll, rr[-1-i]]
        
    res = res.drop(rr[-1], level = 1, axis=1)
    return res
    





#extraction des valeurs d'une seule solicitation 


table_res = res_to_tabulate(res)
res_jumelage = res_jum(res, params.r_points)
table_res_jum = res_to_tabulate(res_jumelage)


for r in params.r_points :
    
    res_r = res.xs(r, axis=1, level=1)
    table_res = res_to_tabulate(res_r)
    print(f'ROUE SIMPLE --------- r ={r} ---------------------------------------------------------')
    table_res = table_res.replace('nan', '   ')
    print(table_res)

for r in params.r_points[:-1] :
    
    res_r = res_jumelage.xs(r, axis=1, level=1)
    table_res_jum = res_to_tabulate(res_r)
    print(f'JUMELAGE --------- r ={r} ---------------------------------------------------------')
    table_res_jum = table_res_jum.replace('nan', '   ')
    table_res_jum = table_res_jum.replace('_', ' ')
    print(table_res_jum)









'''

# uniquement pour le r=0
r = 0
res_0 = res.xs(r, axis=1, level=1)


# export en tabulate

res_0_table = res_to_tabulate(res_0)
print(res_0_table)

# Exporter le tableau formaté dans un fichier texte
output_path = "C:/Users/f.duhart/OneDrive - Département de la Gironde/Documents/06-Git/PyAlize/classes/resultat.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(res_0_table)
print(f"Fichier exporté sous : {output_path}")

'''
