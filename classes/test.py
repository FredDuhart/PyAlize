from class_struct import *
from class_calculation import *
from class_calc_params import *
from class_load import load

from tabulate import tabulate
from IPython.display import display

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

a_layer = layer()
b_layer = layer()
c_layer = layer()
d_layer = layer()
a_layer.define('BB' , 0.06, 7000, 0.35, True, 0)
b_layer.define('GB3', 0.10, 10000   , 0.35, True, 1)
c_layer.define('GB4', 0.12, 12000, 0.35, True, 2)
d_layer.define('CdF', None, 50, 0.35, True,3)
struct = structure()
struct.add_layer(a_layer)
struct.add_layer(b_layer)
struct.add_layer(c_layer)
struct.add_layer(d_layer)

print (struct.htot())
for l in struct.layers :
    print (f'{l.order}  {l.name}   {l.thickness} m    {l.module} Mpa  {l.poisson} Collée = {l.interface}    z = {l.z}   lambda = {l.lb}')


# chargement

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

params.define_r_points ([0,0.2])


#print ('---- paramètres de calcul -------')
#print ('z_point ' , params.z_points)
#print ('c_points ', params.c_points)
#print ('r_points ', params.r_points)
#print()
#print ('valeurs de m')
mm = params.mValues
#print (f'il y a {len(mm)} colonnes de calcul')


# fonction pour générér un DataFRame par position radiale

'''Colonnes
    couche
    nom de la couche
    profondeur de calcul
    E
    nu
    si couche suivante != interface sinon ""
    sollicitations

index des rows
 (couche, nom de la couche, profondeur)

'''









# Calculs


resultats = calculation(struct, params, load_)
res  = resultats.final_results


# uniquement pour le r=0

r = 0
res_0 = res.xs(r, axis=1, level=1)

print('display')
print(res_0.head(res_0.shape[0]))


a = res_0.index.get_level_values("z (m)")





def df_for_tabulate_print(df):
    df_print = df.reset_index()
    prev_level = [None] * df.index.nlevels
    for irow, (idx, row) in enumerate(df.iterrows()):
        for ilevel, level in enumerate(idx):
            if prev_level[ilevel] == level:
                df_print.iat[irow, ilevel] = ''
            prev_level[ilevel] = level
    return df_print

res_0_tab = df_for_tabulate_print(res_0)

print (res_0_tab.dtypes)
print()
print(tabulate(res_0_tab, headers='keys',  tablefmt='rounded_grid',
               showindex=False,
                numalign="right",
                floatfmt=" .6f",
                intfmt =","
                
               ))



# swap
print()
df_swapped = res.copy()
df_swapped.columns = df_swapped.columns.swaplevel(0, 1)
df_swapped = df_swapped.sort_index(axis=1, level=0)

#print(df_swapped)



'''
print()

import pandas as pd


nb_col = len (params.r_points)


l_conv = []
keys = list(res.keys())

for key in keys :
    cols = res[key]
    for i, col  in enumerate(cols) :
        col = list(col)
        col.insert(0,key)
        col.insert(1,params.r_points[i])
        l_conv.append(col)

l_conv_T = list(map(list, zip(*l_conv)))
columns = pd.MultiIndex.from_arrays(l_conv_T[:2], names=["Sollicitations", "r (m)"])
values = l_conv_T[2:]
df = pd.DataFrame(values, columns=columns)
df.index = pd.MultiIndex.from_arrays([params.c_points, params.z_points], names=['couche', 'z (m)'])


print(df.head())






   
    



print()

plotthis  = 0 

solls = ['s_z', 's_t', 's_r', 't_rz', 'w', 'u', 'e_z', 'e_t', 'e_r', 'E']
soll = 's_z'

r =0

df_part = df[(soll, r)]



if plotthis !=0 :
        

    # représentation

    import matplotlib.pyplot as plt

    
    X = df_part

    print (X)

    Y = df.index

    fig, ax = plt.subplots(figsize=(6,6))

    fig.suptitle (f'sollicitations {soll}')
    ax.plot(X, -Y, linewidth=2.0, color='red', alpha = 1)

    plt.show()
    '''