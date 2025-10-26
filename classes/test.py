from class_struct import *
from class_calculation import *


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
    print (f'{l.order}  {l.name}   {l.thickness} cm    {l.module} Mpa  {l.poisson} Collée = {l.interface}   lambda = {l.lb}')



# soll *



c_points = gen_c_points(struct, z_points)


print (f'z_points = {z_points}')
print (f'c_points = {c_points}')



m=1
r_point = 0