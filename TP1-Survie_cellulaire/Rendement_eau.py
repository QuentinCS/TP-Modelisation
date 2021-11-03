#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 09:18:52 2021

@author: quentin
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


phi = 10**11
dist1 = 1
dist2 = 1

# Extraction des données
Data = pd.read_excel('eau.xlsx', sheet_name="Feuil1")
Energy = Data['Energy (MeV)'].values
Att = Data['µ/ρ (cm2/g)'].values
En = Data['µen/ρ (cm2/g)'].values

# Plot des coefficients d'atténuation
plt.plot(Energy, Att, color='red', label='\u03BC/\u03C1')
plt.plot(Energy, En, color= 'blue', label='$\u03BC_{en}/\u03C1$')
plt.title("Coefficients d'atténuation")
plt.xlabel("Energie (MeV)")
plt.ylabel("\u03BC/\u03C1 ($cm^2 g^{-1}$)")
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.show()


# Interpolation aux valueurs d'énergies d'intérêt
E_int = np.array([0.017, 0.1, 1.25, 10])
muatt_int = np.interp(E_int, Energy, Att) 
muen_int = np.interp(E_int, Energy, En)
print(muatt_int)
print(muen_int, "\n \n")

# Calcul de la dose 
Dose_entree = []
for i in range(0, 4):
    Dose_entree.append(phi*E_int[i]*muen_int[i]) # MeV
    Dose_entree [i] = Dose_entree[i]*pow(10, 6)*1.6*pow(10, -19)*1000
    print("Dose absorbée avec l'énergie ", E_int[i], "MeV est ", Dose_entree[i], "Gray")


Prof = np.linspace(1, 1000, 1000)
dose_prof = np.zeros((4, 1000))
dose_prof_norm = np.zeros((4, 1000))
#print(dose_prof)
#print(Prof)

# Rendement en profondeur 
for j in range(0, 4):
    for i in range (0, 1000):
        #print(Dose[j], "\n")
        dose_prof[j][i] = (Dose_entree[j]*np.exp(-(muatt_int[j]/10)*Prof[i]))
        dose_prof_norm[j][i] = dose_prof[j][i]/Dose_entree[j]
        
# Plot des coefficients d'atténuation
plt.plot(Prof, dose_prof_norm[0], color='red', label='17 keV')
plt.plot(Prof, dose_prof_norm[1], color='blue', label='100 keV')
plt.plot(Prof, dose_prof_norm[2], color='green', label='1.25 MeV')
plt.plot(Prof, dose_prof_norm[3], color='yellow', label='10 MeV')
plt.title("Dose")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose (Gy)")
plt.yscale('log')
plt.legend()
plt.show()      


##########################################################
# Prise en compte de la dispersion
##########################################################

dose_prof_disp = np.zeros((4, 1000))
dose_prof_disp_norm = np.zeros((4, 1000))

# Rendement en profondeur 
for j in range(0, 4):
    for i in range (0, 1000):
        #print(Dose[j], "\n")
        dose_prof_disp[j][i] = dose_prof[j][i]*pow(1000/(1000+Prof[i]), 2)
        dose_prof_disp_norm[j][i] = dose_prof_disp[j][i]/Dose_entree[j]
        
# Plot des coefficients d'atténuationplt.plot(Prof, dose_prof_disp[0], color='red', label='17 keV')
plt.plot(Prof, dose_prof_disp_norm[0], color='red', label='17 keV')
plt.plot(Prof, dose_prof_disp_norm[1], color='blue', label='100 keV')
plt.plot(Prof, dose_prof_disp_norm[2], color='green', label='1.25 MeV')
plt.plot(Prof, dose_prof_disp_norm[3], color='yellow', label='10 MeV')
plt.title("Dose avec dispersion")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose (Gy)")
plt.yscale('log')
plt.legend()
plt.show()    


print("\n \n")
phi_sortie = 100
phi_entree = np.zeros((4))
for i in range (0, 4):
    phi_entree[i] = phi_sortie/(pow(0.5, 2)*np.exp(-(muatt_int[i]/10)*1000)) 
    print("Fluence à l'entrée ", E_int[i], "MeV est  ", phi_entree[i])












