from tabulate import tabulate
import textwrap

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

    l_champ = ['couche', 'E', 'z (m)', 's_z', 's_t', 's_r', 'w', 'u', 'e_z', 'e_t', 'e_r',]

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
                df_print.iat[irow, ilevel] = ''
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


    table = tabulate(df, headers=headers_wrapped, maxcolwidths=[larg]*len(l_fmt), tablefmt='rounded_grid', showindex=False, numalign="center", floatfmt=l_fmt, intfmt ="_")
    
    return table

if __name__ == "__main__" :
    pass