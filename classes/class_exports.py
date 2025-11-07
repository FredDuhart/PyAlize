import os
import sys
sys.path.append(os.getcwd())

from tabulate import tabulate
from classes.class_struct import structure
from classes.class_load import load
import textwrap
import pandas as pd



# dict_mep : nom de la couche : [traduction en claire, coef_multi, format tabulate]
coef_epsilon = 1000000
coef_sigma = 1
coef_dep = 1000

f_epsilon = '.1f'
f_sigma = '.4f'
f_dep = '.4f'


dict_mep = {'couche' : ['Couche', 1, ''],
                'z (m)' : ['Prof. (m)' , 1, '.2f'],
                's_z' : [f'{chr(963)}z (MPa)', coef_sigma, f_sigma],
                's_t' : [f'{chr(963)}t (MPa)', coef_sigma, f_sigma],
                's_r' : [f'{chr(963)}r (MPa)', coef_sigma, f_sigma],
                'w' : ['Dép. vert. (mm)', coef_dep, f_dep],
                'u' : ['Dép. rad. (mm)', coef_dep, f_dep],
                'e_z' : [f'{chr(949)}z ({chr(956)}def)', coef_epsilon, f_epsilon],
                'e_t' : [f'{chr(949)}t ({chr(956)}def)', coef_epsilon, f_epsilon],
                'e_r' : [f'{chr(949)}r ({chr(956)}def)', coef_epsilon, f_epsilon],
                'E' : ['Module (MPa)', 1, '_'],
                }

def mise_en_page (df) :

    df = df_for_tabulate_print (df)

    l_champ = ['couche', 'E', 'z (m)', 's_z', 's_t', 's_r', 'w', 'u', 'e_z', 'e_t', 'e_r',]
    l_champ = ['couche', 'z (m)', 's_z', 's_t', 'e_z', 'e_t']

    df = df.reindex(l_champ, axis=1)

    l_fmt = []

    for col in l_champ :
        
        nom = dict_mep[col][0]
        c = dict_mep[col][1]
        fmt = dict_mep[col][2]

        df = df.rename(columns={col : nom})
        df[nom] = df[nom] * c
        l_fmt.append(fmt)


    df_modif = df


    return df_modif , l_fmt



def df_for_tabulate_print(df):
    df_print = df.reset_index()
    prev_level = [None] * df.index.nlevels
    for irow, (idx, row) in enumerate(df.iterrows()):
        for ilevel, level in enumerate(idx):
            if prev_level[ilevel] == level:
                df_print.iat[irow, ilevel] = None
            prev_level[ilevel] = level
    return df_print


def wrap_cell(value, width=5):
    text = str(value)
    return "\n".join(textwrap.wrap(text, width=width))



def res_to_tabulate(df) : 

    df , l_fmt = mise_en_page(df)

    larg = 6 # largeur max de colonne

    # traitement des headers
    headers  = df.columns.to_list()
    headers_wrapped = [wrap_cell(h, larg) for h in headers]

    #df = df.replace(np.nan, None)
    #print(df.head(20))
    table = tabulate(df,
                     headers=headers_wrapped, 
                     maxcolwidths=[larg]*len(l_fmt), 
                     tablefmt='rounded_grid', 
                     showindex=False, 
                     numalign="center", 
                     floatfmt=l_fmt, intfmt ="_",
                     missingval='tot')
    
    table = table.replace('nan', '   ') # trautement des valeurs nullles
    table = table.replace('_', ' ') # traitement du séparateur des milliers
    
    return table

def titre (texte) :
    nb_col = 80
    ligne_supinf = "-" * nb_col + "\n"
    n1 = int((nb_col - 2 - len(texte))/2)
    n2 = nb_col - 2 - len(texte) - n1
    ligne_t = "|" + n1 * ' ' + texte + n2 * ' ' + '|' + '\n'

    return ligne_supinf + ligne_t + ligne_supinf


def export_results (resultats,  charge : load, struct : structure, file_name) :
    
    '''
    resultats : DataFrame issu de la class Calculation
    
    charge : objet de la classe Load
    struct : objet de la classe Structure
    file_name : emplacement et nom du fichier de sortie (txt)

    '''



    # 
    r_points = list(resultats.columns.levels [1])
    
    # élements à imprimer
    # structure
    t_struct = titre('DEFINTION DE LA STRUCTURE')
    e_struct = struct.export_tab()

    # chargement
    dico_load =[['Type' , 'Rayon (m)', 'P (MPA)'],
                [charge.type, charge.radius, charge.load]
               ]
    if charge.disj !=0 :
        dico_load[0].append('Ecart (m)')
        dico_load[1].append(charge.disj)
    table_l = tabulate(dico_load,
                     tablefmt='rounded_grid',
                     showindex=False, 
                     numalign="center", 
        )
    t_load = titre('DEFINTION DE LA CHARGE')
    e_load = table_l

    # résultats
    t_res = titre('RESULTATS')
    e_res = []

    
    for r in r_points :
        res_r = resultats.xs(r, axis=1, level=1)
        e_res.append(res_to_tabulate(res_r))
        

    with open(file_name, 'w', encoding = "utf-8") as f:


        f.write(t_struct)
        f.write(e_struct)
        
        f.write('\n')

        f.write(t_load)
        f.write(e_load)

        f.write('\n')

        f.write(t_res)
        for i, e in enumerate(e_res) :
            f.write (f'Position radiale = {r_points[i]} m\n')
            f.write(e)
            f.write('\n')
