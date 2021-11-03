#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 09:18:52 2021

@author: quentin
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import interpolate
import pylab as pl


phi = 10**11
dist1 = 1
dist2 = 1

# Extraction des données
Data = pd.read_excel('eau.xlsx', sheet_name="Feuil1")
Energy = Data['Energy (MeV)'].values
Att = Data['µ/ρ (cm2/g)'].values
En = Data['µen/ρ (cm2/g)'].values

E_int = np.array([0.017, 0.1, 1.25, 10])

# Plot des coefficients d'atténuation
pl.figure(figsize=(10, 10)) 
plt.plot(Energy, Att, color='red', label="Coefficient d'atténuation \u03BC/\u03C1")
plt.plot(Energy, En, color= 'blue', label="Coefficient d'absorption $\u03BC_{en}/\u03C1$")
plt.title("Coefficients d'atténuation des photons dans l'eau")
plt.xlabel("Energie (MeV)")
plt.ylabel("\u03BC/\u03C1 ($cm^2 g^{-1}$)")
plt.yscale('log')
plt.xscale('log')
plt.axvline(x=E_int[0], color='grey', linestyle='--', linewidth=1, label="Energies d'intéret")
plt.axvline(x=E_int[1], color='grey', linestyle='--', linewidth=1)
plt.axvline(x=E_int[2], color='grey', linestyle='--', linewidth=1)
plt.axvline(x=E_int[3], color='grey', linestyle='--', linewidth=1)
plt.legend(loc=1)
plt.show()


# Interpolation linéaire aux valueurs d'énergies d'intérêt
muatt_int = np.interp(E_int, Energy, Att) 
muen_int = np.interp(E_int, Energy, En)


print("Coefficient d'atténuation par interpolation linéaire", muatt_int)
print("Coefficient d'absorption par interpolation linéaire", muen_int, "\n \n")


# Interpolation quadratique 
energyFineEau=np.geomspace(min(Energy), max(Energy),1000)
inter_muatt_quad = interpolate.interp1d(Energy, Att, kind='quadratic') 
inter_muen_quad = interpolate.interp1d(Energy, En, kind='quadratic') 

muatt_int_quad = np.zeros(4)
muen_int_quad = np.zeros(4)
for i in range(0, 4):    
    muatt_int_quad[i] = inter_muatt_quad(E_int[i])
    muen_int_quad[i] = inter_muen_quad(E_int[i])

print("Coefficient d'atténuation par interpolation quadratique", muatt_int_quad)
print("Coefficient d'absorption par interpolation quadratique", muen_int_quad, "\n \n")

 

# Comparaison interpolations linéaire et quadratiques 
for i in range (0, 4):
    print("Ecart relatifs pour atténuation à %4.3f MeV est %4.3f %%"%((E_int[i]), 100*(muatt_int_quad[i]-muatt_int[i])/muatt_int_quad[i]) )
    print("Ecart relatifs pour absorption à %4.3f MeV est %4.3f %%"%((E_int[i]), 100*(muen_int_quad[i]-muen_int[i])/muen_int_quad[i]) )    
 
print("\n \n")


# Calcul de la dose 
Dose_entree = []
for i in range(0, 4):
    Dose_entree.append(phi*E_int[i]*muen_int_quad[i]) # MeV
    Dose_entree [i] = Dose_entree[i]*pow(10, 6)*1.6*pow(10, -19)*1000
    print("Dose absorbée avec l'énergie ", E_int[i], "MeV est %.4f" %(Dose_entree[i]), "Gray")


Prof = np.linspace(1, 1000, 1000)
dose_prof = np.zeros((4, 1000))
dose_prof_norm = np.zeros((4, 1000))
#print(dose_prof)
#print(Prof)

# Rendement en profondeur 
for j in range(0, 4):
    for i in range (0, 1000):
        #print(Dose[j], "\n")
        dose_prof[j][i] = (Dose_entree[j]*np.exp(-(muatt_int_quad[j]/10)*Prof[i])) 
        # Facteur 10^-1 pour passer de cm^2.g^-1 à mm.kg^-1
        dose_prof_norm[j][i] = dose_prof[j][i]/Dose_entree[j]               
 
pl.figure(figsize=(10, 5)) 
plt.subplot(1, 2, 1)        
# Plot des doses en fonction de la profondeur 
plt.plot(Prof, dose_prof_norm[0], label='17 keV')
plt.plot(Prof, dose_prof_norm[1], label='100 keV')
plt.plot(Prof, dose_prof_norm[2], label='1.25 MeV')
plt.plot(Prof, dose_prof_norm[3], label='10 MeV')
#plt.title("Dose")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose normalisée (Gy)")
#plt.yscale('log')
plt.legend()
#plt.show()    

plt.subplot(1, 2, 2)  
# Same en normalisé 
plt.plot(Prof, dose_prof_norm[0], label='17 keV')
plt.plot(Prof, dose_prof_norm[1], label='100 keV')
plt.plot(Prof, dose_prof_norm[2], label='1.25 MeV')
plt.plot(Prof, dose_prof_norm[3], label='10 MeV')
#plt.title("Dose")
plt.xlabel("Profondeur (mm)")
#plt.ylabel("Dose (Gy)")
plt.yscale('log')
plt.legend()
#plt.show()    

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
pl.figure(figsize=(10, 5)) 
plt.subplot(1, 2, 1)
plt.plot(Prof, dose_prof_disp_norm[0], color='tab:blue', label='17 keV')
plt.plot(Prof, dose_prof_disp_norm[1], color='tab:red', label='100 keV')
plt.plot(Prof, dose_prof_disp_norm[2], color='tab:green', label='1.25 MeV')
plt.plot(Prof, dose_prof_disp_norm[3], color='tab:orange', label='10 MeV')
#plt.title("Prise en compte de la dispersion")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose normalisée (Gy)")
#plt.yscale('log')
plt.plot(Prof, dose_prof_norm[0], color='tab:blue', linestyle="--", label='17 keV (sans dispersion)')
plt.plot(Prof, dose_prof_norm[1], color='tab:red', linestyle="--", label='100 keV (sans dispersion)')
plt.plot(Prof, dose_prof_norm[2], color='tab:green', linestyle="--", label='1.25 MeV (sans dispersion)')
plt.plot(Prof, dose_prof_norm[3], color='tab:orange', linestyle="--", label='10 MeV (sans dispersion)')
#plt.yscale('log')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(Prof, dose_prof_disp_norm[0], color='tab:blue', label='17 keV')
plt.plot(Prof, dose_prof_disp_norm[1], color='tab:red', label='100 keV')
plt.plot(Prof, dose_prof_disp_norm[2], color='tab:green', label='1.25 MeV')
plt.plot(Prof, dose_prof_disp_norm[3], color='tab:orange', label='10 MeV')
#plt.title("Prise en compte de la dispersion")
plt.xlabel("Profondeur (mm)")
#plt.ylabel("Dose normalisée (Gy)")
plt.yscale('log')
plt.plot(Prof, dose_prof_norm[0], color='tab:blue', linestyle="--", label='17 keV (sans dispersion)')
plt.plot(Prof, dose_prof_norm[1], color='tab:red', linestyle="--", label='100 keV (sans dispersion)')
plt.plot(Prof, dose_prof_norm[2], color='tab:green', linestyle="--", label='1.25 MeV (sans dispersion)')
plt.plot(Prof, dose_prof_norm[3], color='tab:orange', linestyle="--", label='10 MeV (sans dispersion)')
#plt.yscale('log')
plt.legend()

print("\n \n")
phi_sortie = 100
phi_entree = np.zeros((4))
dose_entree = np.zeros((4))
dose_10cm = np.zeros((4))
dose_10cm_disp = np.zeros((4))

for i in range (0, 4):
    phi_entree[i] = phi_sortie/(pow(0.5, 2)*np.exp(-(muatt_int_quad[i]/10)*1000))
    dose_entree[i] = phi_entree[i]*E_int[i]*muen_int_quad[i]*pow(10, 6)*1.6*pow(10, -19)*1000
    dose_10cm[i] = dose_entree[i]*np.exp(-(muatt_int_quad[i]/10)*100)
    dose_10cm_disp[i] = dose_10cm[i]*pow(1000/(1000+100), 2)
    print("Fluence à l'entrée pour", E_int[i], "MeV est %.4e"%(phi_entree[i]), "$photons.cm^{-2}$")
    print("Dose à l'entrée pour", E_int[i], "MeV est %.4e"%(dose_entree[i]), "Gy")
    print("Dose à 10 cm pour", E_int[i], "MeV est %.4e"%(dose_10cm[i]), "Gy ")
    print("Dose à 10 cm avec dispersion pour", E_int[i], "MeV est %.4e"%(dose_10cm_disp[i]), "Gy \n")

