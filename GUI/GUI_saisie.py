# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 07:59:17 2023

@author: f.duhart
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 11:11:42 2023

@author: frede
"""

from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

##### import des modules spécifiques
import sys

sys.path.append('./../files/')
sys.path.append('./../calc/')
sys.path.append("C:/Users/f.duhart/OneDrive - Département de la Gironde/Documents/06-Git/PyAlize/files")
sys.path.append("C:/Users\f.duhart\OneDrive - Département de la Gironde\Documents\06-Git\PyAlize\calc")


from cal_alize_func import calc_alize_jum, calc_alize_rouesimple

from RW_pad import read_pad, write_pad


##########################################


class Saisie :
    def __init__(self):
        self.w = Tk ()
        self.w.title("PyAlize v0.1")
        self.w.geometry("750x350")
        self.w.minsize(850, 320)
        self.w.iconbitmap("logo.ico")
        self.create_menu_bar()
        self.w.config(background='#41B77F')
        
        # variables
        self.listeInter=["Collée", "Glissante"]
        self.file = None
        self.tp=10 # taille de la police
        self.data= None


    ''' ---------- Défintion de la barre de menu ----------- '''
    def create_menu_bar(self):
        menu_bar = Menu(self.w)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="New", command=self.init_new)
        menu_file.add_command(label="Open", command=self.init_open)
        menu_file.add_command(label="Save", command=self.init_save)
        menu_file.add_command(label="Save as...", command=self.init_saveas)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.exit_app)
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_calc = Menu(menu_bar, tearoff=0)
        menu_calc.add_command(label="Lancer le calcul (jumelage)", command=self.calcul)
        menu_calc.add_command(label="Lancer le calcul (roue simple)", command=self.calcul_roue_simple)
        menu_bar.add_cascade(label="Calcul", menu=menu_calc)
        

        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="About", command=self.func_poubelle)
        menu_bar.add_cascade(label="Help", menu=menu_help)

        self.w.config(menu=menu_bar)

    ''' ------------- Défintion du contenu de la fenetre (avec n couches) ---------- '''  

    ''' frame de gauche (n couches) '''  
    def init_saisie(self,n):            
        
        # n = nombre de couches
        
        ncouche= n
        
        # initialization des composants
        self.frame_title = Frame(self.w, highlightbackground="#676767", highlightthickness=1, padx=5, pady=5)
        self.frame_l = Frame(self.w, highlightbackground="#676767", highlightthickness=1, padx=5, pady=5)
        self.frame_e = Frame(self.w, highlightbackground="#676767", highlightthickness=1, padx=5, pady=5)
        
        # titre du projet
        
        
        self.l_nproj = Label (self.frame_title,
                         text='Nom du projet',
                         font=("Courrier", self.tp))
            
        self.l_nproj.grid(column=0, row=0, )        
        
        self.e_nproj = Entry(self.frame_title,
                        width =70,
                        font=("Courrier", self.tp))
        self.e_nproj.grid(column=1, row=0, padx=10)  
        
        
        
        # creation des composants de structure
        self.create_titles()
        self.init_entries(ncouche)
        
        # menu de droite
        self.menu_droite()
       
        # empaquetage
        #self.frame_l.pack(expand=YES)
        #self.frame_e.pack(expand=YES)
        
        self.frame_title.grid(column =0 , row = 0, columnspan=2, sticky='nw', pady=10, padx = 10)
        self.frame_l.grid(column =0 , row = 1, sticky='nw', padx= 10, pady = 5)
        self.frame_e.grid(column =1 , row = 1, sticky='ne', pady= 5, padx = 10)
       
       
    
    ''' frame de droite - ajout suppression de couches '''    
    def menu_droite(self):
        #bouton d'ajout
        b_add = Button(self.frame_e, text='ajoute une\bcouche après...', command = self.add_func)
        b_add.grid(column = 0 , row = 0)
        
        # bouton de supression
        b_supp = Button(self.frame_e, text='supprime une couche ...', command = self.supp_func, width = 20)
        b_supp.grid(column = 0 , row = 1)
        
        
        nb=len(self.e_)
        
        # combobox ajout
        
        self.l_ajout=self.liste_ajout(nb)
        
        self.cb_ajout= Combobox(self.frame_e, width = 12, values=self.l_ajout, font=("arial", 10),
                                postcommand=lambda: self.cb_ajout.configure(values=self.l_ajout))
                
        self.cb_ajout.current(0)
        self.cb_ajout.grid(column = 1 , row = 0, padx=3)
        
        # combobox suppression
        
        self.l_supp=self.liste_supp(nb)
        
        self.cb_supp= Combobox(self.frame_e, width = 12, values=self.l_supp, font=("arial", 10),
                               postcommand=lambda: self.cb_supp.configure(values=self.l_supp))
        self.cb_supp.current(0)
        self.cb_supp.grid(column = 1 , row = 1)
   
    ''' frame de gauche - défintion des titres '''
    def create_titles(self) :
        
        
        
        l_name=['couche','Nom', 'Epaisseur (m)', 'E (MPa)', 'Coef. Poisson', 'Interface']
        
        l_=[]
        
        for i, nom in enumerate(l_name) :
            l__ = Label(self.frame_l,
                         text=nom,
                         font=("Courrier", self.tp))
            l_.append(l__)
            l_[i].grid(column=i, row=0)        
    
    ''' frame de gauche - défintion des entries '''    
    def init_entries(self, n) :
        
        # Ajouter une couche après la couche n => déplace les couches situées après....
        
                      
        self.e_=None
        self.e_=[]
        
        
        self.vcmd = (self.w.register(self.validate_entries), '%P')
        
        
        for lig in range (n) :
            er_=None
            er_=[]
            
            # numéro de couche
            er__ = Label(self.frame_l,
                         text=lig+1,
                         font=("Courrier", self.tp))
            er_.append(er__)
            er_[0].grid(column=0, row=lig+1)
            
            # aurtes données
            

            
            
            
            # nom de la couche 
            
            er__ = Entry(self.frame_l,
                         width =10,
                         font=("Courrier", self.tp))
            er_.append(er__)
            er_[1].grid(column=1, row=lig+1)
            
            
            # données numériques
          
                                  
            
            for col in range (3) :
                er__ = Entry(self.frame_l,
                             width =10,
                             font=("Courrier", self.tp),
                             validate = 'key', validatecommand = self.vcmd)
                er_.append(er__)
                er_[col+2].grid(column=col+2, row=lig+1)  
    
                       
            # interface
            
            
            
            er__ = Combobox(self.frame_l, width = 12, values=self.listeInter)
            er__.current(0)
            er_.append(er__)
            er_[5].grid(column=5, row=lig+1)


            self.e_.append(er_)
            
        self.masque_derlig()
        
        
    def validate_entries(self, P):
        
        if P == '':
            return True
                       
        try :
            float(P)
            return True
        except:
            return False            
        

    ''' gestion des changements (supp, add) '''

        
    def add_func (self):
        
        n = self.cb_ajout.get()
        
        if n =='' :
            return
        elif n=='Au début':
            mess = 'Voulez-vous vraiment ajouter une couche au début ?'
            n = 0
        else:
            n=int(n)
            mess = f'Voulez-vous vraiment ajouter une couche après la couche {n} ?'
            
        messagebox.showwarning("showwarning", mess)
        
        self.add_entry(n)
               
   
        
    def supp_func (self):
        
        n = self.cb_supp.get()
        
        if n =='' :
            mess = 'rien à faire!!!'
            messagebox.showwarning("showwarning", mess)
            return
        else:
            n=int(n)
            mess = f'Voulez-vous vraiment supprimer la couche {n} ?'
            
        messagebox.showwarning("showwarning", mess)
        
        self.supp_entry(n)    

    def add_entry(self, pos) :
            
        
        er_=None
        er_=[]
        
        #nombre de couche existantes
        n_couches=len(self.e_)
        
        if pos > n_couches :
            pos = n_couches
        elif pos < 0 :
            pos = 0
        
        #lmite le nombre de couche
        if n_couches >= 8 :
            mess = "Nombre de couches minimum = 8 \n Impossible d'ajouter la couche"
            messagebox.showwarning("showwarning", mess)
            
            return
        
        #### ajoute d'une couche vierge à la fin
        
        # numéro de couche
        er__ = Label(self.frame_l,
                     text=n_couches+1,
                     font=("Courrier", self.tp))
        er_.append(er__)
        er_[0].grid(column=0, row=n_couches+1)
        
        #### aurtes données
        
        # nom de la couche
        
        er__ = Entry(self.frame_l,
                     width = 10,
                     font=("Courrier", self.tp))
        er_.append(er__)
        er_[1].grid(column=1, row=n_couches+1)  
        
        # données numériques
        
        for col in range (3) :
            er__ = Entry(self.frame_l,
                         width = 10,
                         font=("Courrier", self.tp),
                         validate = 'key', validatecommand = self.vcmd)
            er_.append(er__)
            er_[col+2].grid(column=col+2, row=n_couches+1)  
        
           
                          
        # interface
        
        er__ = Combobox(self.frame_l, width = 12,  values=self.listeInter)
        er__.current(0)
        er_.append(er__)
        er_[5].grid(column=5, row=n_couches+1)
        
        self.e_.append(er_)

        #### copie des valeurs vers le bas pour les couches situés aprsè pos
        
        for i in reversed(range (pos, n_couches+1) ):
            
            
            # traitement des entry box et de la combobox
            
            for j in range (1,6):
                text = self.e_[i-1][j].get()
                
                er__ = self.e_[i][j]
                er__.delete(0,END)
                er__.insert(0,text)
                


        # effacement de la ligne insérée
        for j in range (1,5) :
            er__ = self.e_[pos][j]
            er__.delete(0,END)
        
        er__ = self.e_[pos][5]    
        er__.current(0)
        
        self.masque_derlig()
        
             
        # mise à jour de la liste d'ajout
        
        self.l_ajout.append (n_couches)
        self.l_supp.append (n_couches)

    def supp_entry(self, pos) :
        
        # supprime la couche pos
        
        er_=None
        er_=[]
        
        #nombre de couche existantes
        n_couches=len(self.e_)
        
        if n_couches <= 2 :
            mess = "Nombre de couches minimum = 2 \n Impossible de supprimer la couche"
            messagebox.showwarning("showwarning", mess)
            
            return
        
        if pos >= n_couches :
            mess = "On ne peut pas supprimer la dernière couche !"
            messagebox.showwarning("showwarning", mess)
            
            return
        
        
        #### copie des valeurs vers le haut pour les couches situés après pos
        
        if pos != n_couches :
            
            for i in (pos-1, n_couches-2):
                #print(f'couche {i} déplacée')
                
                # traitement des entry box et de la combobox
                
                for j in range (1,6):
                    text = self.e_[i+1][j].get()
                    
                    er__ = self.e_[i][j]
                    er__.delete(0,END)
                    er__.insert(0,text)
        
        ### suppression de la derniere ligne
        
        for i in range (6) :
            self.e_[n_couches-1][i].destroy()
        
        # mise à jour de la liste
        self.e_.pop(n_couches-1)
        
        self.masque_derlig()
        
        

    
        # mise à jour de la liste d'ajout
        self.l_supp.pop()
        self.l_ajout.pop()
        
      
    def liste_ajout (self, n):
        # créé la liste des couches pour ajouter une couche parès la couche x
        # le premier item sera 'au début'
        # on ne peut pas ajouter d'etm après la dernière couche 
        # n = nombre de couche avant ajout
        
        l_ajout=[]
        l_ajout.append('')
        l_ajout.append('Au début')
        
        for i in range (n-1):
            l_ajout.append(i+1)
        
        return l_ajout
            
    def liste_supp (self, n):
        # créé la liste des couches qiu peuvent être supprimées
        # on ne peut pas supprimer la dernière couche
        # n = nombre de couche avant ajout
        
        l_supp=[]
        l_supp.append('')
                
        for i in range (n-1):
            l_supp.append(i+1)
        
        return l_supp    
            

    
    def masque_derlig(self):
        
        n_couches = len(self.e_)        
        
        
        
        er__=self.e_[n_couches-2][2]
        er__.config({'bg' : 'white', 'bd' :'1', 'fg': 'black'})
        
        er__=self.e_[n_couches-1][2]
        er__.config({'bg' : '#F0F0F0', 'bd' :'0', 'fg': '#F0F0F0'})
        


    '''----------------------------------------------------- '''
    ''' ----------- gestion des enregistrements ------------ '''    
    '''----------------------------------------------------- '''
    
    ''' appel fonction nouvelle structure '''
    def init_new(self):
        n=3 ##nombre de couche d'une nouvelle structure
        
        
        
        
        r= self.verif_change()
        
        if r == 'stand':
            return
        elif r == 'first' :
            self.init_saisie(n)
            self.data = self.collecte_data()
            self.file = None
        else :
            self.frame_e.destroy()
            self.frame_l.destroy()
            self.frame_title.destroy()
            self.init_saisie(n)
            self.data = self.collecte_data()
            self.file = None




    ''' appel fonction ouvre structure existante '''
    def init_open(self):
        
        r= self.verif_change()
        
        if r == 'stand':
            return
                  
    
       
        new_file = askopenfilename(title="Choose the file to open",
                               filetypes=[("PyAlizeData", ".pad")])
                    
        # récuperer les données
        data=read_pad(new_file)
        #print (data)
        
        if data == 'error' :
            mess = 'Le fichier de données semble contenir des erreurs !'
            messagebox.showwarning("showwarning", mess)
            return
        
        self.file = new_file
        
        if r == 'replace':
            self.frame_e.destroy()
            self.frame_l.destroy()
            self.frame_title.destroy()
        
        
        # récupérer le nombre de couche
        n=data['n_couches']
            
        self.init_saisie(n)
        self.data = self.collecte_data()
        
        
        # écrire les données dans la fenetre
        
        text = data['nom']
        er__ = self.e_nproj
        er__.delete(0,END)
        er__.insert(0,text)

        
        for i in range (n):
            # nom des couches
            text = data['noms_couches'][i]
            er__ = self.e_[i][1]
            er__.delete(0,END)
            er__.insert(0,text)
            
            # épaisseur
            if i <= (n-2):
                text = data['th'][i]
                er__ = self.e_[i][2]
                er__.delete(0,END)
                er__.insert(0,text)
            
            # module
            text = data['E'][i]
            er__ = self.e_[i][3]
            er__.delete(0,END)
            er__.insert(0,text)
            
            # nu
            text = data['nu'][i]
            er__ = self.e_[i][4]
            er__.delete(0,END)
            er__.insert(0,text)
            
            # épaisseur
            if i <= (n-2):
                if data['inter'][i] == 1 :
                    text = self.listeInter[0]  
                else :
                    text = self.listeInter[1]
                er__ = self.e_[i][5]
                er__.delete(0,END)
                er__.insert(0,text)            
        
        self.data = self.collecte_data()

    ''' fonction save '''
    
    def init_save(self):
        
        if self.file is None :
            self.init_saveas()
        else:
            data_n = self.collecte_data()  
            
            if data_n['nom']=='' :
                
                data_n['nom'] = self.nom_fic() 
                self.e_nproj.delete(0,END)
                self.e_nproj.insert(0,data_n['nom']) 
                
                       
            
            write_pad (data_n, self.file) # sauvegarde
            self.data = data_n   
        return
    
    def init_saveas (self):
        
        self.file = asksaveasfilename(title="Save as",
                               filetypes=[("PyAlizeData", ".pad")])
        
        # ajout autimatique de l'extension si elle manque
        if len(self.file)>=5 and self.file[-4::1] != '.pad' :
            #print (f'les derniers caratéres === {self.file[-5::1]}')
            self.file=self.file + '.pad'
        elif len(self.file)<5 :
            #print('Moins de 5 caracteres')
            self.file=self.file + '.pad'
        
        
        
        
        data_n = self.collecte_data()
        
        if data_n['nom']=='' :
            
            data_n['nom'] = self.nom_fic() 
            self.e_nproj.delete(0,END)
            self.e_nproj.insert(0,data_n['nom'])
        
        
        write_pad (data_n, self.file) # sauvegarde
        self.data = data_n
        return
    
    
    ''' y a t'il eu des changements dans les données ? '''
    ''' à documenter '''
     
    def verif_change(self):
        # test sur modifs
        
        if self.data is None :
            test_changement = False
        else :
            data_n = self.collecte_data()
            if data_n == self.data:
                test_changement = False
            else :
                test_changement = True
    
        if self.file and test_changement:       # cas d'un fichier ouvert avec des modifs
            mess = 'Un fichier est ouvert.\nVoulez-vous enregistrer les modifications ?'
            r= messagebox.askyesnocancel(title=None, message=mess)
            
            if r == True: 
                 # sauvegarder la structure
                 
                 self.init_save()
                 
                 retour = 'replace'
                 
            elif r == False:
                 #print ('Il ne faut pas sauvegarder la structure')
                 retour = 'replace'
                 
            elif r is None :
                #print ('Je ne fais rien')
                retour = 'stand'
                
            
        elif self.file and not(test_changement):        # cas d'un fichier ouvert sans modifs
            #print ('Pas de modifs => pas de sauvegarde')
            
            retour ='replace'
            
            
            
            
        elif not(self.file) and test_changement:       # cas d'absence de fichier avec modifs
            mess = 'Vos données ont été modifiées.\nVoulez-vous enregistrer les modifications ?'
            r= messagebox.askyesnocancel(title=None, message=mess)
            
            if r == True: 
                 # sauvegarder la structure
                 #print ('Il faut sauvegarder la structure')
                 
                 self.init_saveas()
                 
                 retour = 'replace'
                 
            elif r == False:
                 #print ('Il ne faut pas sauvegarder la structure')
                 retour = 'replace'
                 
            elif r is None :
                #print ('Je ne fais rien')
                retour = 'stand'
                 
        elif not(self.file) and not test_changement :   # cas d'absence de fichier sans modifs
            retour = 'first'
        
        #print (f'self.fil = {self.file} /// test changement = {test_changement}')  
        #print (f'retour = {retour}')
        return retour
        

    ''' collecte les valeurs des entrées pour les mettre sous forme de dictionnaire '''   
    def collecte_data(self):
        #cette fonction rccupere les données de structure et les ranges dans un dictionnaire
        # self.data
        
        data = {"nom":'', "n_couches" : 0, 'noms_couches': [],
                'th' : [],
                'E' : [],
                'nu' : [],
                'inter' : []}
        
        data['nom'] = self.e_nproj.get()
        
        n_c = len(self.e_)
        data['n_couches'] = n_c
        
        for i in range (n_c):
            
            data['noms_couches'].append(self.e_[i][1].get())
            
            th = self.e_[i][2].get()
            if th == '' :
                th='0'
            data['th'].append(th)
            
            E = self.e_[i][3].get()
            if E == '' :
                E='0'
            data['E'].append(E)
            
            nu = self.e_[i][4].get()
            if nu == '' :
                nu='0'
            data['nu'].append(nu)
            
            if self.e_[i][5].get() == self.listeInter[0]:
                data['inter'].append(1)
            else :
                data['inter'].append(0)
                
               
        # enleve les dernieres valeurs de th et inter
        data['th'].pop(-1)   
        data['inter'].pop(-1)
        
        # convert to float
        #print ('collecte des données')
        #print (data)
        #print ('________')
        
        data['th'] = [float(i) for i in data['th']]
        data['E'] = [float(i) for i in data['E']]
        data['nu'] = [float(i) for i in data['nu']]
        
        
        return data
    
    
    def nom_fic(self):
        
        if self.file is not None :        
            deb = self.file.rfind("/", 0, len(self.file))
            
            nom_fichier = self.file[deb+1:len(self.file)]
            
            
            return nom_fichier
                

    
    def func_poubelle (self) :
        return
    

        
    def exit_app(self):
        self.w.destroy()
    
    

        
    '''----------------------------------------------------- '''
    ''' ----------- Calculs -------------------------------- '''    
    '''----------------------------------------------------- '''
    
    def calcul (self) :
        
        messagebox.showwarning("verif chemin", f"Le chemin est : {self.file}")
        
        if self.file is None :
            messagebox.showwarning("Données non enregistrées", "Enregistre vos données avant de la lancer un calcul!")
            return
        
        data = self.collecte_data()
        
        mess = calc_alize_jum (data, self.file)
        
        messagebox.showwarning("Résultat", mess)
        
    def calcul_roue_simple (self) :
        
        messagebox.showwarning("verif chemin", f"Le chemin est : {self.file}")
        
        if self.file is None :
            messagebox.showwarning("Données non enregistrées", "Enregistre vos données avant de la lancer un calcul!")
            return
        
        data = self.collecte_data()
        
        mess = calc_alize_rouesimple (data, self.file)
        
        messagebox.showwarning("Résultat", mess)        



# # afficher
# app = Saisie()
# app.w.mainloop()