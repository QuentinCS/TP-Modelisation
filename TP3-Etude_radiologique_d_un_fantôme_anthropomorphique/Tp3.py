#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 13:10:30 2021

@author: quentin
"""
 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pylab as pl
import function as f
import time

start_time = time.time()
E_int = np.array([0.017, 0.064, 0.1, 10])
KERMA = 0.001
rho_eau = 1
rho_bone = 1.85
rho_soft = 1.01
rho_lung = 1.05 
rho_lung_air = 0.35
pos_axe = 37
profondeur = [i for i in range(200)]
largeur = [i for i in range(75)]
taille_pixel = 0.1

#########################################################################################################
# Extraction des données
#########################################################################################################
Soft = pd.read_excel('SoftTissueNIST.xlsx', sheet_name="SoftTissueNIST")
Energy_soft = Soft['Energy (MeV)'].values
soft_att = Soft['μ/ρ (cm2/g)'].values
soft_en = Soft['μen/ρ (cm2/g)'].values

Lung = pd.read_excel('lungNIST.xlsx', sheet_name="lungNIST")
Energy_lung = Lung['Energy (MeV)'].values
lung_att = Lung['μ/ρ (cm2/g)'].values
lung_en = Lung['μen/ρ (cm2/g)'].values

Bone = pd.read_excel('CorticalBoneNIST.xlsx', sheet_name="CorticalBoneNIST")
Energy_bone = Bone['Energy (MeV)'].values
bone_att = Bone['μ/ρ (cm2/g)'].values
bone_en = Bone['μen/ρ (cm2/g)'].values

Air = pd.read_excel('airNISTxmudat.xlsx', sheet_name="airNist")
Energy_air = Air['Energy (MeV)'].values
air_att = Air['μ/ρ (cm2/g)'].values
air_tr = Air['μtr/ρ (cm2/g)'].values
air_en = Air['μen/ρ (cm2/g)'].values


#########################################################################################################
# Plot des coefficients d'atténuation
#########################################################################################################
pl.figure(figsize=(20, 6))
plt.subplot(1, 3, 1) # 2 divisions en x, 2 en yn et on adresse la 1ère case
plt.plot(Energy_soft, soft_att, color='red',
         label="Coefficient d'atténuation \u03BC/\u03C1")
plt.plot(Energy_soft, soft_en, color='blue',
         label="Coefficient d'absorption $\u03BC_{en}/\u03C1$")
plt.title("Tissus mou ")
plt.xlabel("Energie (MeV)")
plt.ylabel("\u03BC/\u03C1 ($cm^2 g^{-1}$)")
plt.yscale('log')
plt.xscale('log')
#plt.axvline(x=E_int[0], color='grey', linestyle='--', linewidth=1, label="Energies d'intéret")
#plt.axvline(x=E_int[1], color='grey', linestyle='--', linewidth=1)
#plt.axvline(x=E_int[2], color='grey', linestyle='--', linewidth=1)
#plt.axvline(x=E_int[3], color='grey', linestyle='--', linewidth=1)
plt.legend(loc=1)

# Plot des coefficients d'atténuation
plt.subplot(1, 3, 2) # 2 divisions en x, 2 en yn et on adresse la 1ère case
plt.plot(Energy_lung, lung_att, color='red',
         label="Coefficient d'atténuation \u03BC/\u03C1")
plt.plot(Energy_lung, lung_en, color='blue',
         label="Coefficient d'absorption $\u03BC_{en}/\u03C1$")
plt.title("Poumons")
plt.xlabel("Energie (MeV)")
plt.ylabel("\u03BC/\u03C1 ($cm^2 g^{-1}$)")
plt.yscale('log')
plt.xscale('log')
#plt.axvline(x=E_int[0], color='grey', linestyle='--', linewidth=1, label="Energies d'intéret")
#plt.axvline(x=E_int[1], color='grey', linestyle='--', linewidth=1)
#plt.axvline(x=E_int[2], color='grey', linestyle='--', linewidth=1)
#plt.axvline(x=E_int[3], color='grey', linestyle='--', linewidth=1)
plt.legend(loc=1)

# Plot des coefficients d'atténuation
plt.subplot(1, 3, 3) # 2 divisions en x, 2 en yn et on adresse la 1ère case
plt.plot(Energy_bone, bone_att, color='red',
         label="Coefficient d'atténuation \u03BC/\u03C1")
plt.plot(Energy_bone, bone_en, color='blue',
         label="Coefficient d'absorption $\u03BC_{en}/\u03C1$")
plt.title("Os")
plt.xlabel("Energie (MeV)")
plt.ylabel("\u03BC/\u03C1 ($cm^2 g^{-1}$)")
plt.yscale('log')
plt.xscale('log')
#plt.axvline(x=E_int[0], color='grey', linestyle='--', linewidth=1, label="Energies d'intéret")
#plt.axvline(x=E_int[1], color='grey', linestyle='--', linewidth=1)
#plt.axvline(x=E_int[2], color='grey', linestyle='--', linewidth=1)
#plt.axvline(x=E_int[3], color='grey', linestyle='--', linewidth=1)
plt.legend(loc=1)
plt.show()

#########################################################################################################
# Interpolation mu_tr
#########################################################################################################
mu_tr_air = f.Interp(Energy_air, air_tr, E_int)
mu_en_air = f.Interp(Energy_air, air_en, E_int)
mu_att_air = f.Interp(Energy_air, air_att, E_int)
mu_en_soft = f.Interp(Energy_soft, soft_en, E_int)
mu_en_lung = f.Interp(Energy_lung, lung_en, E_int)
mu_en_bone = f.Interp(Energy_bone, bone_en, E_int)
mu_att_soft = f.Interp(Energy_soft, soft_att, E_int)
mu_att_lung = f.Interp(Energy_lung, lung_att, E_int)
mu_att_bone = f.Interp(Energy_bone, bone_att, E_int)
print("Interpolation mu_en_soft :", mu_en_soft)
print("Interpolation mu_en_lung :", mu_en_lung)
print("Interpolation mu_en_bone :", mu_en_bone)
print("\n")
print("Interpolation mu_soft :", mu_att_soft)
print("Interpolation mu_lung :", mu_att_lung)
print("Interpolation mu_bone :", mu_att_bone)
print("\n \n")

print("mu_lung_real :", (1/3)*mu_att_lung+(2/3)*mu_att_air)
print("mu_en_lung_real :", (1/3)*mu_en_lung+(2/3)*mu_en_air)


# Calcul de la fluence et de la dose à l'entrée
fluence_entree = np.zeros(4)
dose_entree = np.zeros(4)
dose_entree1 = np.zeros(4)

for energy in range(0, 4):
    print("Pour une énergie de %4.3f MeV :" % (E_int[energy]))
    fluence_entree[energy] = KERMA//(E_int[energy]*pow(10, 6)*1.6*pow(10, -19)*mu_tr_air[energy]*1000)
    dose_entree1[energy] = fluence_entree[energy]*E_int[energy]*pow(10, 6)*1.6*pow(10, -19)*mu_en_soft[energy]*1000
    dose_entree[energy] = KERMA*(mu_en_soft[energy]/mu_tr_air[energy])
    print("La fluence à l'entrée est %4.3e photon.cm^-2" % (fluence_entree[energy]))
    print("La dose à l'entrée est %4.3e Gy" % (dose_entree[energy]))
    print("La dose à l'entrée v2 est %4.3e Gy \n" % (dose_entree1[energy]))


#########################################################################################################
# Construction des fantômes
#########################################################################################################
fantome_mu_17kev = f.matrice(mu_att_soft[0], mu_att_lung[0], mu_att_bone[0])
fantome_mu_64kev = f.matrice(mu_att_soft[1], mu_att_lung[1], mu_att_bone[1])
fantome_mu_100kev = f.matrice(mu_att_soft[2], mu_att_lung[2], mu_att_bone[2])
fantome_mu_10mev = f.matrice(mu_att_soft[3], mu_att_lung[3], mu_att_bone[3])

fantome_muen_17kev = f.matrice(mu_en_soft[0], mu_en_lung[0], mu_en_bone[0])
fantome_muen_64kev = f.matrice(mu_en_soft[1], mu_en_lung[1], mu_en_bone[1])
fantome_muen_100kev = f.matrice(mu_en_soft[2], mu_en_lung[2], mu_en_bone[2])
fantome_muen_10mev = f.matrice(mu_en_soft[3], mu_en_lung[3], mu_en_bone[3])

fantome_mu_17kev_real = f.matrice(mu_att_soft[0], (1/3)*mu_att_lung[0]+(2/3)*mu_att_air[0], mu_att_bone[0])
fantome_mu_64kev_real = f.matrice(mu_att_soft[1], (1/3)*mu_att_lung[1]+(2/3)*mu_att_air[1], mu_att_bone[1])
fantome_mu_100kev_real = f.matrice(mu_att_soft[2], (1/3)*mu_att_lung[2]+(2/3)*mu_att_air[2], mu_att_bone[2])
fantome_mu_10mev_real = f.matrice(mu_att_soft[3], (1/3)*mu_att_lung[3]+(2/3)*mu_att_air[3], mu_att_bone[3])

fantome_muen_17kev_real = f.matrice(mu_en_soft[0], (1/3)*mu_en_lung[0]+(2/3)*mu_en_air[0], mu_en_bone[0])
fantome_muen_64kev_real = f.matrice(mu_en_soft[1], (1/3)*mu_en_lung[1]+(2/3)*mu_en_air[1], mu_en_bone[1])
fantome_muen_100kev_real = f.matrice(mu_en_soft[2], (1/3)*mu_en_lung[2]+(2/3)*mu_en_air[2], mu_en_bone[2])
fantome_muen_10mev_real = f.matrice(mu_en_soft[3], (1/3)*mu_en_lung[3]+(2/3)*mu_en_air[3], mu_en_bone[3])

fantome_rho = f.matrice(rho_soft, rho_lung, rho_bone)
fantome_rho_real = f.matrice(rho_soft, rho_lung_air, rho_bone)

# Plot fantôme 
f.printmatrice(fantome_mu_17kev, fantome_mu_64kev, fantome_mu_100kev, fantome_mu_10mev, "Fantômes \u03BC/\u03C1")
f.printmatrice(fantome_muen_17kev, fantome_muen_64kev, fantome_muen_100kev, fantome_muen_10mev, "Fantômes \u03BC_en/\u03C1")
f.printmatrice(fantome_mu_17kev_real, fantome_mu_64kev_real, fantome_mu_100kev_real, fantome_mu_10mev_real, "Fantômes réels \u03BC/\u03C1")
f.printmatrice(fantome_muen_17kev_real, fantome_muen_64kev_real, fantome_muen_100kev_real, fantome_muen_10mev_real, "Fantômes réels \u03BC_en/\u03C1")

pl.figure(figsize=(50, 25)) 
plt.imshow(fantome_rho)
plt.colorbar()
plt.title("Fantôme \u03C1", fontsize=100)
plt.xlabel("Longueur (mm)", fontsize=80)
plt.ylabel("Largeur (mm)", fontsize=80)
plt.show()

pl.figure(figsize=(50, 25)) 
plt.imshow(fantome_rho_real)
plt.colorbar()
plt.title("Fantôme réel \u03C1", fontsize=100)
plt.xlabel("Longueur (mm)", fontsize=80)
plt.ylabel("Largeur (mm)", fontsize=80)
plt.show()

#########################################################################################################
# Calcul de la dose en fonction de la profondeur, position de l'axe y=40
#########################################################################################################
dose = np.zeros((4, 200))
dose_real = np.zeros((4, 200))
dose_norm = np.zeros((4, 200))
fluence = np.zeros((4, 200))
fluence_real = np.zeros((4, 200))

for i in range(0, 200):
    if i==0:
        fluence[0][0] = fluence_entree[0]
        fluence[1][0] = fluence_entree[1]
        fluence[2][0] = fluence_entree[2]
        fluence[3][0] = fluence_entree[3]
        
        fluence_real[0][0] = fluence_entree[0]
        fluence_real[1][0] = fluence_entree[1]
        fluence_real[2][0] = fluence_entree[2]
        fluence_real[3][0] = fluence_entree[3]
        
        dose[0][0] = fluence_entree[0]*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_17kev[pos_axe][0]
        dose[1][0] = fluence_entree[1]*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_64kev[pos_axe][0]
        dose[2][0] = fluence_entree[2]*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_100kev[pos_axe][0]
        dose[3][0] = fluence_entree[3]*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_10mev[pos_axe][0]
        
        dose_real[0][0] = fluence_entree[0]*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_17kev_real[pos_axe][0]
        dose_real[1][0] = fluence_entree[1]*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_64kev_real[pos_axe][0]
        dose_real[2][0] = fluence_entree[2]*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_100kev_real[pos_axe][0]
        dose_real[3][0] = fluence_entree[3]*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_10mev_real[pos_axe][0]
        
    else:
        fluence[0][i] = fluence[0][i-1]*np.exp(-(fantome_mu_17kev[pos_axe][i]*fantome_rho[pos_axe][i]/10))
        fluence[1][i] = fluence[1][i-1]*np.exp(-(fantome_mu_64kev[pos_axe][i]*fantome_rho[pos_axe][i]/10))
        fluence[2][i] = fluence[2][i-1]*np.exp(-(fantome_mu_100kev[pos_axe][i]*fantome_rho[pos_axe][i]/10))
        fluence[3][i] = fluence[3][i-1]*np.exp(-(fantome_mu_10mev[pos_axe][i]*fantome_rho[pos_axe][i]/10))

        dose[0][i] = fluence[0][i]*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_17kev[pos_axe][i]
        dose[1][i] = fluence[1][i]*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_64kev[pos_axe][i]
        dose[2][i] = fluence[2][i]*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_100kev[pos_axe][i]
        dose[3][i] = fluence[3][i]*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_10mev[pos_axe][i]

        fluence_real[0][i] = fluence_real[0][i-1]*np.exp(-(fantome_mu_17kev_real[pos_axe][i]*fantome_rho_real[pos_axe][i]/10))
        fluence_real[1][i] = fluence_real[1][i-1]*np.exp(-(fantome_mu_64kev_real[pos_axe][i]*fantome_rho_real[pos_axe][i]/10))
        fluence_real[2][i] = fluence_real[2][i-1]*np.exp(-(fantome_mu_100kev_real[pos_axe][i]*fantome_rho_real[pos_axe][i]/10))
        fluence_real[3][i] = fluence_real[3][i-1]*np.exp(-(fantome_mu_10mev_real[pos_axe][i]*fantome_rho_real[pos_axe][i]/10))

        dose_real[0][i] = fluence_real[0][i]*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_17kev_real[pos_axe][i]
        dose_real[1][i] = fluence_real[1][i]*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_64kev_real[pos_axe][i]
        dose_real[2][i] = fluence_real[2][i]*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_100kev_real[pos_axe][i]
        dose_real[3][i] = fluence_real[3][i]*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_10mev_real[pos_axe][i]

    dose_norm[0][i] = dose[0][i]/dose_entree[0]
    dose_norm[1][i] = dose[1][i]/dose_entree[1]
    dose_norm[2][i] = dose[2][i]/dose_entree[2]
    dose_norm[3][i] = dose[3][i]/dose_entree[3]
    


#########################################################################################################
# Plot des doses sur l'axe 
#########################################################################################################
pl.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)  
plt.suptitle("Dose absorbée", fontsize=25)
plt.plot(profondeur, dose[0], label="17 keV")
plt.plot(profondeur, dose[1], label="64 keV")
plt.plot(profondeur, dose[2], label="100 keV")
plt.plot(profondeur, dose[3], label="10 MeV")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose (Gy)")
#plt.yscale('log')
# plt.legend(loc=1)
plt.legend()
plt.subplot(1, 2, 2)  
plt.plot(profondeur, dose[0], label="17 keV")
plt.plot(profondeur, dose[1], label="64 keV")
plt.plot(profondeur, dose[2], label="100 keV")
plt.plot(profondeur, dose[3], label="10 MeV")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose (Gy)")
plt.yscale('log')
# plt.legend(loc=1)
plt.legend()
plt.show()

pl.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)  
plt.suptitle("Dose absorbée poumon réel", fontsize=25)
plt.plot(profondeur, dose_real[0], label="17 keV")
plt.plot(profondeur, dose_real[1], label="64 keV")
plt.plot(profondeur, dose_real[2], label="100 keV")
plt.plot(profondeur, dose_real[3], label="10 MeV")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose (Gy)")
#plt.yscale('log')
# plt.legend(loc=1)
plt.legend()
plt.subplot(1, 2, 2)  
plt.plot(profondeur, dose_real[0], label="17 keV")
plt.plot(profondeur, dose_real[1], label="64 keV")
plt.plot(profondeur, dose_real[2], label="100 keV")
plt.plot(profondeur, dose_real[3], label="10 MeV")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose (Gy)")
plt.yscale('log')
# plt.legend(loc=1)
plt.legend()
plt.show()

#########################################################################################################
# Calcul de carte de dose
#########################################################################################################
dose_map = np.zeros((4, 75, 200))
dose_map_real = np.zeros((4, 75, 200))
fluence_map = np.zeros((4, 75, 200))
fluence_map_real = np.zeros((4, 75, 200))

for j in range(0, 75):
    for energy in range (0, 4):
        dose_map[energy][j][0] = dose_entree[energy]    
        fluence_map[energy][j][0] = fluence_entree[energy]
        dose_map_real[energy][j][0] = dose_entree[energy]
        fluence_map_real[energy][j][0] = fluence_entree[energy]


for j in range(0, 75):
    for i in range(1, 200):

        fluence_map[0][j][i] = fluence_map[0][j][i-1]*np.exp(-(fantome_mu_17kev[j][i]*fantome_rho[j][i]/10))
        fluence_map[1][j][i] = fluence_map[1][j][i-1]*np.exp(-(fantome_mu_64kev[j][i]*fantome_rho[j][i]/10))
        fluence_map[2][j][i] = fluence_map[2][j][i-1]*np.exp(-(fantome_mu_100kev[j][i]*fantome_rho[j][i]/10))
        fluence_map[3][j][i] = fluence_map[3][j][i-1]*np.exp(-(fantome_mu_10mev[j][i]*fantome_rho[j][i]/10))

        dose_map[0][j][i] = fluence_map[0][j][i]*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_17kev[j][i]
        dose_map[1][j][i] = fluence_map[1][j][i]*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_64kev[j][i]
        dose_map[2][j][i] = fluence_map[2][j][i]*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_100kev[j][i]
        dose_map[3][j][i] = fluence_map[3][j][i]*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_10mev[j][i]


        fluence_map_real[0][j][i] = fluence_map_real[0][j][i-1]*np.exp(-(fantome_mu_17kev_real[j][i]*fantome_rho_real[j][i]/10))
        fluence_map_real[1][j][i] = fluence_map_real[1][j][i-1]*np.exp(-(fantome_mu_64kev_real[j][i]*fantome_rho_real[j][i]/10))
        fluence_map_real[2][j][i] = fluence_map_real[2][j][i-1]*np.exp(-(fantome_mu_100kev_real[j][i]*fantome_rho_real[j][i]/10))
        fluence_map_real[3][j][i] = fluence_map_real[3][j][i-1]*np.exp(-(fantome_mu_10mev_real[j][i]*fantome_rho_real[j][i]/10))

        dose_map_real[0][j][i] = fluence_map_real[0][j][i]*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_17kev_real[j][i]
        dose_map_real[1][j][i] = fluence_map_real[1][j][i]*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_64kev_real[j][i]
        dose_map_real[2][j][i] = fluence_map_real[2][j][i]*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_100kev_real[j][i]
        dose_map_real[3][j][i] = fluence_map_real[3][j][i]*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_10mev_real[j][i]

dose_map_1 = np.zeros((75, 200))
dose_map_1 = dose_map[2]

# Affichage des cartes de dose 
f.printmatrice(dose_map[0], dose_map[1], dose_map[2], dose_map[3], "Cartes de doses dans le fantôme")
f.printmatrice(dose_map_real[0], dose_map_real[1], dose_map_real[2], dose_map_real[3], "Cartes de doses dans le fantôme réel")
f.printmatrice(fluence_map[0], fluence_map[1], fluence_map[2], fluence_map[3], "Carte de fluence dans le fantôme")
f.printmatrice(fluence_map_real[0], fluence_map_real[1], fluence_map_real[2], fluence_map_real[3], "Carte de fluence réelle dans le fantôme")


#########################################################################################################
# Calcul de la fluence et de la dose à l'entrée avec une fluence en sortie de 100000
#########################################################################################################
fluence_sortie = 100000
fluence_axe_2 = np.zeros((4, 200))
fluence_axe_real_2 = np.zeros((4, 200))
fluence_map_2 = np.zeros((4, 75, 200))
fluence_map_real_2 = np.zeros((4, 75, 200))
dose_entree2 = np.zeros((4, 75))
dose_entree_real_2 = np.zeros((4, 75))
dose_map_2 = np.zeros((4, 75, 200))
dose_map_real_2 = np.zeros((4, 75, 200))

#for i in range(0, 200):
fluence_axe_2[0][199] = fluence_sortie
fluence_axe_2[1][199] = fluence_sortie
fluence_axe_2[2][199] = fluence_sortie
fluence_axe_2[3][199] = fluence_sortie

fluence_axe_real_2[0][199] = fluence_sortie
fluence_axe_real_2[1][199] = fluence_sortie
fluence_axe_real_2[2][199] = fluence_sortie
fluence_axe_real_2[3][199] = fluence_sortie

for i in range(198, -1, -1):
    fluence_axe_2[0][i] = fluence_axe_2[0][i+1]/(np.exp(-fantome_mu_17kev[pos_axe][i]*fantome_rho[pos_axe][i]*0.1))
    fluence_axe_2[1][i] = fluence_axe_2[1][i+1]/(np.exp(-fantome_mu_64kev[pos_axe][i]*fantome_rho[pos_axe][i]*0.1))
    fluence_axe_2[2][i] = fluence_axe_2[2][i+1]/(np.exp(-fantome_mu_100kev[pos_axe][i]*fantome_rho[pos_axe][i]*0.1))
    fluence_axe_2[3][i] = fluence_axe_2[3][i+1]/(np.exp(-fantome_mu_10mev[pos_axe][i]*fantome_rho[pos_axe][i]*0.1))
    
    fluence_axe_real_2[0][i] = fluence_axe_real_2[0][i+1]/(np.exp(-fantome_mu_17kev_real[pos_axe][i]*fantome_rho_real[pos_axe][i]*0.1))
    fluence_axe_real_2[1][i] = fluence_axe_real_2[1][i+1]/(np.exp(-fantome_mu_64kev_real[pos_axe][i]*fantome_rho_real[pos_axe][i]*0.1))
    fluence_axe_real_2[2][i] = fluence_axe_real_2[2][i+1]/(np.exp(-fantome_mu_100kev_real[pos_axe][i]*fantome_rho_real[pos_axe][i]*0.1))
    fluence_axe_real_2[3][i] = fluence_axe_real_2[3][i+1]/(np.exp(-fantome_mu_10mev_real[pos_axe][i]*fantome_rho_real[pos_axe][i]*0.1))

for i in range(0, 75):
    dose_entree2[0][i] = fluence_axe_2[0][0]*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_17kev[i][0]*1000
    dose_entree2[1][i] = fluence_axe_2[1][0]*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_64kev[i][0]*1000
    dose_entree2[2][i] = fluence_axe_2[2][0]*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_100kev[i][0]*1000
    dose_entree2[3][i] = fluence_axe_2[3][0]*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_10mev[i][0]*1000
    
    dose_entree_real_2[0][i] = fluence_axe_real_2[0][0]*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_17kev_real[i][0]*1000
    dose_entree_real_2[1][i] = fluence_axe_real_2[1][0]*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_64kev_real[i][0]*1000
    dose_entree_real_2[2][i] = fluence_axe_real_2[2][0]*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_100kev_real[i][0]*1000
    dose_entree_real_2[3][i] = fluence_axe_real_2[3][0]*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_10mev_real[i][0]*1000
 
for j in range(0, 75):
    for i in range(0, 200):
        if i==0:
            fluence_map_2[0][j][0] = fluence_axe_2[0][0]
            fluence_map_2[1][j][0] = fluence_axe_2[1][0]
            fluence_map_2[2][j][0] = fluence_axe_2[2][0]
            fluence_map_2[3][j][0] = fluence_axe_2[3][0]
            
            dose_map_2[0][j][0] = dose_entree2[0][j]
            dose_map_2[1][j][0] = dose_entree2[1][j]
            dose_map_2[2][j][0] = dose_entree2[2][j]
            dose_map_2[3][j][0] = dose_entree2[3][j] 

            fluence_map_real_2[0][j][0] = fluence_axe_real_2[0][0]
            fluence_map_real_2[1][j][0] = fluence_axe_real_2[1][0]
            fluence_map_real_2[2][j][0] = fluence_axe_real_2[2][0]
            fluence_map_real_2[3][j][0] = fluence_axe_real_2[3][0]
            
            dose_map_real_2[0][j][0] = dose_entree_real_2[0][j]
            dose_map_real_2[1][j][0] = dose_entree_real_2[1][j]
            dose_map_real_2[2][j][0] = dose_entree_real_2[2][j]
            dose_map_real_2[3][j][0] = dose_entree_real_2[3][j] 

        else:
            fluence_map_2[0][j][i] = fluence_map_2[0][j][i-1]*np.exp(-(fantome_mu_17kev[j][i]*fantome_rho[j][i]/10))
            fluence_map_2[1][j][i] = fluence_map_2[1][j][i-1]*np.exp(-(fantome_mu_64kev[j][i]*fantome_rho[j][i]/10))
            fluence_map_2[2][j][i] = fluence_map_2[2][j][i-1]*np.exp(-(fantome_mu_100kev[j][i]*fantome_rho[j][i]/10))
            fluence_map_2[3][j][i] = fluence_map_2[3][j][i-1]*np.exp(-(fantome_mu_10mev[j][i]*fantome_rho[j][i]/10))
            
            dose_map_2[0][j][i] = fluence_map_2[0][j][i]*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_17kev[j][i]*1000
            dose_map_2[1][j][i] = fluence_map_2[1][j][i]*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_64kev[j][i]*1000
            dose_map_2[2][j][i] = fluence_map_2[2][j][i]*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_100kev[j][i]*1000
            dose_map_2[3][j][i] = fluence_map_2[3][j][i]*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_10mev[j][i]*1000

            fluence_map_real_2[0][j][i] = fluence_map_real_2[0][j][i-1]*np.exp(-(fantome_mu_17kev_real[j][i]*fantome_rho_real[j][i]/10))
            fluence_map_real_2[1][j][i] = fluence_map_real_2[1][j][i-1]*np.exp(-(fantome_mu_64kev_real[j][i]*fantome_rho_real[j][i]/10))
            fluence_map_real_2[2][j][i] = fluence_map_real_2[2][j][i-1]*np.exp(-(fantome_mu_100kev_real[j][i]*fantome_rho_real[j][i]/10))
            fluence_map_real_2[3][j][i] = fluence_map_real_2[3][j][i-1]*np.exp(-(fantome_mu_10mev_real[j][i]*fantome_rho_real[j][i]/10))
            
            dose_map_real_2[0][j][i] = fluence_map_real_2[0][j][i]*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_17kev_real[j][i]*1000
            dose_map_real_2[1][j][i] = fluence_map_real_2[1][j][i]*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_64kev_real[j][i]*1000
            dose_map_real_2[2][j][i] = fluence_map_real_2[2][j][i]*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_100kev_real[j][i]*1000
            dose_map_real_2[3][j][i] = fluence_map_real_2[3][j][i]*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*fantome_muen_10mev_real[j][i]*1000


f.printmatrice(fluence_map_2[0], fluence_map_2[1], fluence_map_2[2], fluence_map_2[3], "Carte de fluence avec une fluence en sortie de 1000 $photon.mm^{-2} sur l'axe$")
f.printmatrice(dose_map_2[0], dose_map_2[1], dose_map_2[2], dose_map_2[3], "Carte de dose avec une fluence en sortie de 1000 $photon.mm^{-2}$ sur l'axe")
f.printmatrice(fluence_map_real_2[0], fluence_map_real_2[1], fluence_map_real_2[2], fluence_map_real_2[3], "Carte de fluence avec poumon réel avec une fluence en sortie de 1000 $photon.mm^{-2} sur l'axe$")
f.printmatrice(dose_map_real_2[0], dose_map_real_2[1], dose_map_real_2[2], dose_map_real_2[3], "Carte de dose avec poumon réel avec une fluence en sortie \n de 1000 $photon.mm^{-2}$ sur l'axe")


for energy in range(0, 4):
    print("La fluence en entrée pour une fluence de 1000 photon $mm^-2$ en sortie à %3.4f MeV sur l'axe en sortie du patient est %4.3e photon.cm^{-2}"%(E_int[energy], fluence_axe_2[energy][pos_axe]))
    print("La dose en entrée pour une fluence de 1000 photon $mm^-2$ en sortie à %3.4f MeV sur l'axe en sortie du patient est %4.3e Gy"%(E_int[energy], dose_entree2[energy][pos_axe]))
    print("La fluence réelle en entrée pour une fluence de 1000 photon $mm^-2$ en sortie à %3.4f MeV sur l'axe en sortie du patient est %4.3e photon.cm^{-2}"%(E_int[energy], fluence_axe_real_2[energy][pos_axe]))
    print("La dose en entrée réelle pour une fluence de 1000 photon $mm^-2$ en sortie à %3.4f MeV sur l'axe en sortie du patient est %4.3e Gy"%(E_int[energy], dose_entree_real_2[energy][pos_axe]))

print("\n \n")

pl.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)        
plt.suptitle("Dose absorbée pour une fluence en sortie de 100000", fontsize=20)
#plt.plot(profondeur, dose_map_2[0][pos_axe], label="17 keV")
plt.plot(profondeur, dose_map_2[1][pos_axe], label="64 keV")
plt.plot(profondeur, dose_map_2[2][pos_axe], label="100 keV")
plt.plot(profondeur, dose_map_2[3][pos_axe], label="10 MeV")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose (Gy)") 
#plt.yscale('log')
# plt.legend(loc=1)
plt.legend()
plt.subplot(1, 2, 2)        
plt.plot(profondeur, dose_map_2[0][pos_axe], label="17 keV")
plt.plot(profondeur, dose_map_2[1][pos_axe], label="64 keV")
plt.plot(profondeur, dose_map_2[2][pos_axe], label="100 keV")
plt.plot(profondeur, dose_map_2[3][pos_axe], label="10 MeV")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose (Gy)")
plt.yscale('log')
# plt.legend(loc=1)
plt.legend()
plt.show()

pl.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)        
plt.suptitle("Dose absorbée pour une fluence en sortie de 1000 photon.mm^{-2} \n sur l'axe pour un poumon réel", fontsize=20)
#plt.plot(profondeur, dose_map_2[0][pos_axe], label="17 keV")
plt.plot(profondeur, dose_map_real_2[1][pos_axe], label="64 keV")
plt.plot(profondeur, dose_map_real_2[2][pos_axe], label="100 keV")
plt.plot(profondeur, dose_map_real_2[3][pos_axe], label="10 MeV")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose (Gy)") 
#plt.yscale('log')
# plt.legend(loc=1)
plt.legend()
plt.subplot(1, 2, 2)        
plt.plot(profondeur, dose_map_real_2[0][pos_axe], label="17 keV")
plt.plot(profondeur, dose_map_real_2[1][pos_axe], label="64 keV")
plt.plot(profondeur, dose_map_real_2[2][pos_axe], label="100 keV")
plt.plot(profondeur, dose_map_real_2[3][pos_axe], label="10 MeV")
plt.xlabel("Profondeur (mm)")
plt.ylabel("Dose (Gy)")
plt.yscale('log')
# plt.legend(loc=1)
plt.legend()
plt.show()




#########################################################################################################
# Calcul de la dose moyenne au coeur sur le long de l'axe
#########################################################################################################
coeur = range(36, 66, 1)
dose_coeur = np.zeros(4)
dose_moyenne_coeur = np.zeros(4)
for energy in range(0, 4):
    for i in coeur:
        dose_coeur[energy] += dose_map_2[energy][pos_axe][i]

for energy in range(0, 4):
    dose_moyenne_coeur[energy] = dose_coeur[energy]/30
    print("La dose moyenne dans le coeurs sur l'axe à %4.3f MeV est %4.3e Gy" %
          (E_int[energy], dose_moyenne_coeur[energy]))
print("\n")


#########################################################################################################
# Calcul de la dose moyenne dans tout le coeur
#########################################################################################################
coeur_y = range(36, 66, 1)
coeur_x = range(16, 66, 1)
dose_coeur_tot = np.zeros(4)
dose_moyenne_coeur_tot = np.zeros(4)
for energy in range(0, 4):
    for i in coeur_y:
        for k in coeur_x:            
            dose_coeur_tot[energy] += dose_map[energy][i][k]

for energy in range(0, 4):
    dose_moyenne_coeur_tot[energy] = dose_coeur_tot[energy]/(30*50)
    print("La dose moyenne dans le coeur à %4.3f MeV est %4.3e Gy" %
          (E_int[energy], dose_moyenne_coeur_tot[energy]))
print("\n")


#########################################################################################################
# Calcul de la dose moyenne dans tout le coeur réel
#########################################################################################################
coeur_y = range(36, 66, 1)
coeur_x = range(16, 66, 1)
dose_coeur_tot = np.zeros(4)
dose_coeur_tot_fluencesortie = np.zeros(4)
dose_moyenne_coeur_tot = np.zeros(4)
dose_moyenne_coeur_tot_fluencesortie = np.zeros(4)
for energy in range(0, 4):
    for j in coeur_y:
        for k in coeur_x:            
            dose_coeur_tot[energy] += dose_map_real[energy][j][k]
            dose_coeur_tot_fluencesortie[energy] += dose_map_2[energy][j][k]

for energy in range(0, 4):
    dose_moyenne_coeur_tot[energy] = dose_coeur_tot[energy]/(30*50)
    dose_moyenne_coeur_tot_fluencesortie[energy] = dose_coeur_tot_fluencesortie[energy]/(30*50)
    print("La dose moyenne dans le coeur réel à %4.3f MeV est %4.3e Gy" %
          (E_int[energy], dose_moyenne_coeur_tot[energy]))
    print("La dose moyenne dans le coeur avec une fluence en sortie de 1000 photon mm^-2 à %4.3f MeV est %4.3e Gy" %
          (E_int[energy], dose_moyenne_coeur_tot_fluencesortie[energy]))

print("\n \n")

#########################################################################################################
# Calcul de la dose totale et de la dose moyenne 
#########################################################################################################

dose_tot = np.zeros(4)

for energy in range(0, 4):
    for y in range(0, 75):
        for x in range(0, 200):
            dose_tot[energy] += dose_map[energy][y][x]

    print("La dose totale dans le fantôme a un énerie de %4.3f MeV est de %4.3f Gy"%(E_int[energy], dose_tot[energy]))
    print("La dose moyenne dans le fantôme a un énerie de %4.3f MeV est de %4.3e Gy \n"%(E_int[energy], dose_tot[energy]/(75+200)))




#########################################################################################################
# Profil d'intensité en sortie
#########################################################################################################

fluence_sortie_2 = np.zeros((4, 75))
dose_sortie_2 = np.zeros((4, 75))

for energy in range(0, 4):
    for j in range (0, 75):
        fluence_sortie_2[energy][j] = 0.01*fluence_map_2[energy][j][198]
        dose_sortie_2[energy][j] = dose_map_2[energy][j][198]
        #print(fluence_sortie_2[energy][j])


pl.figure(figsize=(10, 4)) 
plt.subplot(1, 2, 1)    
plt.suptitle("Profil d'intensité en sortie", fontsize=20)
#plt.plot(largeur, fluence_sortie_2[0], label="17 keV")
plt.plot(largeur, fluence_sortie_2[1], label="64 keV")
plt.plot(largeur, fluence_sortie_2[2], label="100 keV")
plt.plot(largeur, fluence_sortie_2[3], label="10 MeV")
plt.xlabel("Largeur (mm)")
plt.ylabel("Intensité ($photon.pixel^{-1}$)") 
plt.yscale('log')
plt.legend(loc=1)
plt.legend()
plt.subplot(1, 2, 2)  
plt.plot(largeur, fluence_sortie_2[0], label="17 keV")
plt.xlabel("Largeur (mm)")
#plt.ylabel("Dose (Gy)") 
plt.yscale('log')
# plt.legend(loc=1)
plt.legend()
plt.show()


#########################################################################################################
# Calcul du contraste 
#########################################################################################################
intensite_axe = np.zeros(4)
intensite = np.zeros((4, 75))
contraste = np.zeros(4)
contraste_profil = np.zeros((4, 75)) # Profil de contraste par rapport à l'axe 

surface_pixel = taille_pixel*taille_pixel

for energy in range(0, 4):
    for y in range(0, 75):
        intensite[energy][y] = fluence_map_real[energy][y][199]
    for y in range(0, 75):
        contraste_profil[energy][y] = abs((intensite[energy][y]-intensite[energy][pos_axe])/(intensite[energy][y]+intensite[energy][pos_axe]))
        
    intensite_axe[energy] = fluence_map[energy][pos_axe][199]*surface_pixel
    contraste[energy] = abs((intensite[energy][pos_axe+1]-intensite[energy][pos_axe-1])/(intensite[energy][pos_axe-1]+intensite[energy][pos_axe+1]))
    print("Contraste à %4.3f MeV : %4.3f"%(E_int[energy], contraste[energy]))

pl.figure(figsize=(10, 6)) 
plt.plot(largeur, contraste_profil[0], label="17 keV")
plt.plot(largeur, contraste_profil[1], label="64 keV")
plt.plot(largeur, contraste_profil[2], label="100 keV")
plt.plot(largeur, contraste_profil[3], label="10 MeV")
plt.title("Profil de contraste")
plt.xlabel("Largeur (mm)")
plt.ylabel("Contraste (-)") 
#plt.yscale('log')
# plt.legend(loc=1)
plt.legend()
plt.show()



duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)








