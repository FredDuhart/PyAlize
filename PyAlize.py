# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:36:28 2023

@author: f.duhart
"""

from tkinter import *

##### import des modules spécifiques

import sys
#sys.path.append('./GUI/')
#sys.path.insert(1, './GUI')
sys.path.append('./GUI/')
from GUI_saisie import *

# afficher
app = Saisie()
app.w.mainloop()
