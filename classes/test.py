from class_struct import *
from class_calculation import *
from class_calc_params import *
from class_load import load


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

params.define_r_points ([0])


print ('---- paramètres de calcul -------')
print ('z_point ' , params.z_points)
print ('c_points ', params.c_points)
print ('r_points ', params.r_points)
print()
print ('valeurs de m')
mm = params.mValues
print (f'il y a {len(mm)} colonnes de calcul')






# Calculs


resultats = calculation(struct, params, load_)
res = resultats.final_results

print (res)

# représentation

import matplotlib.pyplot as plt

solls = ['s_z', 's_t', 's_r', 't_rz', 'w', 'u', 'e_z', 'e_t', 'e_r', 'E']

soll = 's_z'
X = np.hstack(res[soll])

print (X)

Y = params.z_points

fig, ax = plt.subplots(figsize=(6,6))

fig.suptitle (f'sollicitations {soll}')
ax.plot(X, -Y, linewidth=2.0, color='red', alpha = 1)

plt.show()