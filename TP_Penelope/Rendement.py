#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 10:39:27 2022

@author: quentin
"""


import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
import time
import func as f




# Comparaison en fonction de la divergence du faisceau dans le fantôme anthropomorphique

fantome_div = [] 
fantome_div.append(f.Data('fantome_humain/divergent_3/17_keV', 17e3, '17 keV', milieu='fantome'))
fantome_div.append(f.Data('fantome_humain/divergent_3/64_keV', 64e3, '64 keV', milieu='fantome'))
fantome_div.append(f.Data('fantome_humain/divergent_3/100_keV', 100e3, '100 keV', milieu='fantome'))
fantome_div.append(f.Data('fantome_humain/divergent_3/10_MeV', 10e6, '10 MeV', milieu='fantome'))


plt.figure(figsize=(50, 30)) 
for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.plot(fantome_div[i].z, fantome_div[i].dose_norm_e, label='%s°'%(fantome_div[i].divergence))
    plt.title(fantome_div[i].get_name())
    plt.xlabel('z (mm)')
    plt.ylabel('Dose normalisée (Gy))')
    plt.legend() 
