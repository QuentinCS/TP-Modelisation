#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 19:38:54 2021

@author: quentin
"""

# Code pour la comparaison des résultats de simulation du profil de dose dans un fantôme
# anthropomorphique: calcul analytique avec python et calcul Monte Carlo sur penelope
# pour différentes énergies: 17 keV, 64 keV, 100 keV, 10 MeV

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
import time
import func as f

E_int = np.array([0.017, 0.064, 0.1, 10])
rho_eau = 1
rho_bone = 1.85
rho_soft = 1.01
rho_lung = 1.05 
rho_lung_air = 0.35
pos_axe = 39
lim = 200
profondeur = [i for i in range(lim)]
profondeur2 = [i for i in range(600)]

start_time = time.time()

#########################################################################################################
# Extraction des données
#########################################################################################################
Soft = pd.read_excel('nist/SoftTissueNIST.xlsx', sheet_name="SoftTissueNIST")
Energy_soft = Soft['Energy (MeV)'].values
soft_att = Soft['μ/ρ (cm2/g)'].values
soft_en = Soft['μen/ρ (cm2/g)'].values

Lung = pd.read_excel('nist/lungNIST.xlsx', sheet_name="lungNIST")
Energy_lung = Lung['Energy (MeV)'].values
lung_att = Lung['μ/ρ (cm2/g)'].values
lung_en = Lung['μen/ρ (cm2/g)'].values

Bone = pd.read_excel('nist/CorticalBoneNIST.xlsx', sheet_name="CorticalBoneNIST")
Energy_bone = Bone['Energy (MeV)'].values
bone_att = Bone['μ/ρ (cm2/g)'].values
bone_en = Bone['μen/ρ (cm2/g)'].values

Air = pd.read_excel('nist/airNISTxmudat.xlsx', sheet_name="airNist")
Energy_air = Air['Energy (MeV)'].values
air_att = Air['μ/ρ (cm2/g)'].values
air_tr = Air['μtr/ρ (cm2/g)'].values
air_en = Air['μen/ρ (cm2/g)'].values

mu_tr_air = f.Interp(Energy_air, air_tr, E_int)
mu_en_air = f.Interp(Energy_air, air_en, E_int)
mu_att_air = f.Interp(Energy_air, air_att, E_int)
mu_en_soft = f.Interp(Energy_soft, soft_en, E_int)
mu_en_lung = f.Interp(Energy_lung, lung_en, E_int)
mu_en_bone = f.Interp(Energy_bone, bone_en, E_int)
mu_att_soft = f.Interp(Energy_soft, soft_att, E_int)
mu_att_lung = f.Interp(Energy_lung, lung_att, E_int)
mu_att_bone = f.Interp(Energy_bone, bone_att, E_int)



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

#####################################################################################
# Calcul numérique (analytique de la dose)
#####################################################################################

dose = np.zeros((4, lim))
dose_real = np.zeros((4, lim))
dose_norm = np.zeros((4, lim))
fluence = np.zeros((4, lim))
fluence_real = np.zeros((4, lim))
fluence_entree = 1e7

for i in range(0, lim):
    if i==0:
        fluence[0][0] = fluence_entree
        fluence[1][0] = fluence_entree
        fluence[2][0] = fluence_entree
        fluence[3][0] = fluence_entree
        
        fluence_real[0][0] = fluence_entree
        fluence_real[1][0] = fluence_entree 
        fluence_real[2][0] = fluence_entree
        fluence_real[3][0] = fluence_entree
        
        dose[0][0] = fluence_entree*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_17kev[pos_axe][0]
        dose[1][0] = fluence_entree*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_64kev[pos_axe][0]
        dose[2][0] = fluence_entree*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_100kev[pos_axe][0]
        dose[3][0] = fluence_entree*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_10mev[pos_axe][0]
        
        dose_real[0][0] = fluence_entree*E_int[0]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_17kev_real[pos_axe][0]
        dose_real[1][0] = fluence_entree*E_int[1]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_64kev_real[pos_axe][0]
        dose_real[2][0] = fluence_entree*E_int[2]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_100kev_real[pos_axe][0]
        dose_real[3][0] = fluence_entree*E_int[3]*pow(10, 6)*1.6*pow(10, -19)*1000*fantome_muen_10mev_real[pos_axe][0]
        
        dose_norm[0][i] = dose[0][i]/dose[0][0]
        dose_norm[1][i] = dose[1][i]/dose[1][0]
        dose_norm[2][i] = dose[2][i]/dose[2][0]
        dose_norm[3][i] = dose[3][i]/dose[3][0]
        
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

        dose_norm[0][i] = dose[0][i]/dose[0][0]
        dose_norm[1][i] = dose[1][i]/dose[1][0]
        dose_norm[2][i] = dose[2][i]/dose[2][0]
        dose_norm[3][i] = dose[3][i]/dose[3][0]

###############################################################################################
# Récupération des données de penelope et normalisation des résultats à la dose à l'entrée 
###############################################################################################

data_fantome = [] 
data_fantome.append(f.Data('fantome_humain/parallele/17_keV', 17e3, '17 keV', milieu='fantome'))
data_fantome.append(f.Data('fantome_humain/parallele/64_keV', 64e3, '64 keV', milieu='fantome'))
data_fantome.append(f.Data('fantome_humain/parallele/100_keV', 100e3, '100 keV', milieu='fantome'))
data_fantome.append(f.Data('fantome_humain/parallele/10_MeV', 10e6, '10 MeV', milieu='fantome'))

data_norm = []
for i in range(len(data_fantome)):
    if i==3:
        data_norm.append(0.006*data_fantome[i].dose/data_fantome[i].dose[0])
    else:
        data_norm.append(data_fantome[i].dose/data_fantome[i].dose[0])

######################################################################################
# Comparaison des profils de dose sur l'axe du faisceau 
######################################################################################

plt.figure(figsize=(20, 15)) 
for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.plot(profondeur, dose_norm[i], label='Calcul analytique')
    
    if i ==3:
        plt.plot(10*data_fantome[i].z, data_norm[i], label='$10^{-2}$Simulation Penelope')
    else:
        plt.plot(10*data_fantome[i].z, data_norm[i], label='Simulation Penelope')
    plt.title(data_fantome[i].get_name())
    plt.xlabel('z (mm)')
    plt.ylabel('Dose normalisée (Gy))')
    plt.legend()



#############################################################################################
# Influence de la taille de champs
#############################################################################################
# Comparaison en fonction de la taille de champs, donc du diffusé patient dans la cuve à eau

cuve_par_5 = [] 
cuve_par_5.append(f.Data('cuve_eau/parallele_5.64/17_keV', 17e3, '17 keV', milieu='cuve'))
cuve_par_5.append(f.Data('cuve_eau/parallele_5.64/64_keV', 64e3, '64 keV', milieu='cuve'))
cuve_par_5.append(f.Data('cuve_eau/parallele_5.64/100_keV', 100e3, '100 keV', milieu='cuve'))
cuve_par_5.append(f.Data('cuve_eau/parallele_5.64/10_MeV', 10e6, '10 MeV', milieu='cuve'))

cuve_par_10 = [] 
cuve_par_10.append(f.Data('cuve_eau/parallele_10/17_keV', 17e3, '17 keV', milieu='cuve'))
cuve_par_10.append(f.Data('cuve_eau/parallele_10/64_keV', 64e3, '64 keV', milieu='cuve'))
cuve_par_10.append(f.Data('cuve_eau/parallele_10/100_keV', 100e3, '100 keV', milieu='cuve'))
cuve_par_10.append(f.Data('cuve_eau/parallele_10/10_MeV', 10e6, '10 MeV', milieu='cuve'))

cuve_par_20 = [] 
cuve_par_20.append(f.Data('cuve_eau/parallele_20/17_keV', 17e3, '17 keV', milieu='cuve'))
cuve_par_20.append(f.Data('cuve_eau/parallele_20/64_keV', 64e3, '64 keV', milieu='cuve'))
cuve_par_20.append(f.Data('cuve_eau/parallele_20/100_keV', 100e3, '100 keV', milieu='cuve'))
cuve_par_20.append(f.Data('cuve_eau/parallele_20/10_MeV', 10e6, '10 MeV', milieu='cuve'))

cuve_par_30 = [] 
cuve_par_30.append(f.Data('cuve_eau/parallele_30/17_keV', 17e3, '17 keV', milieu='cuve'))
cuve_par_30.append(f.Data('cuve_eau/parallele_30/64_keV', 64e3, '64 keV', milieu='cuve'))
cuve_par_30.append(f.Data('cuve_eau/parallele_30/100_keV', 100e3, '100 keV', milieu='cuve'))
cuve_par_30.append(f.Data('cuve_eau/parallele_30/10_MeV', 10e6, '10 MeV', milieu='cuve'))

cuve_par_40 = [] 
cuve_par_40.append(f.Data('cuve_eau/parallele_40/17_keV', 17e3, '17 keV', milieu='cuve'))
cuve_par_40.append(f.Data('cuve_eau/parallele_40/64_keV', 64e3, '64 keV', milieu='cuve'))
cuve_par_40.append(f.Data('cuve_eau/parallele_40/100_keV', 100e3, '100 keV', milieu='cuve'))
cuve_par_40.append(f.Data('cuve_eau/parallele_40/10_MeV', 10e6, '10 MeV', milieu='cuve'))

plt.figure(figsize=(20, 15)) 
for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.plot(cuve_par_5[i].z, cuve_par_5[i].dose_phi, label='%s cm'%(cuve_par_5[i].taille_source))
    plt.plot(cuve_par_10[i].z, cuve_par_10[i].dose_phi, label='%s cm'%(cuve_par_10[i].taille_source))
    plt.plot(cuve_par_20[i].z, cuve_par_20[i].dose_phi, label='%s cm'%(cuve_par_20[i].taille_source))
    plt.plot(cuve_par_30[i].z, cuve_par_30[i].dose_phi, label='%s cm'%(cuve_par_30[i].taille_source))
    plt.plot(cuve_par_40[i].z, cuve_par_40[i].dose_phi, label='%s cm'%(cuve_par_40[i].taille_source))
    plt.title(data_fantome[i].get_name())
    plt.xlabel('z (mm)')
    plt.ylabel('Dose normalisée (Gy))')
    plt.legend()

# Comparaison en fonction de la taille de champs, donc du diffusé patient dans le fantôme
fantome_par_1 = [] 
fantome_par_1.append(f.Data('fantome_humain/parallele_1/17_keV', 17e3, '17 keV', milieu='fantome'))
fantome_par_1.append(f.Data('fantome_humain/parallele_1/64_keV', 64e3, '64 keV', milieu='fantome'))
fantome_par_1.append(f.Data('fantome_humain/parallele_1/100_keV', 100e3, '100 keV', milieu='fantome'))
fantome_par_1.append(f.Data('fantome_humain/parallele_1/10_MeV', 10e6, '10 MeV', milieu='fantome'))

fantome_par_2 = [] 
fantome_par_2.append(f.Data('fantome_humain/parallele_2/17_keV', 17e3, '17 keV', milieu='fantome'))
fantome_par_2.append(f.Data('fantome_humain/parallele_2/64_keV', 64e3, '64 keV', milieu='fantome'))
fantome_par_2.append(f.Data('fantome_humain/parallele_2/100_keV', 100e3, '100 keV', milieu='fantome'))
fantome_par_2.append(f.Data('fantome_humain/parallele_2/10_MeV', 10e6, '10 MeV', milieu='fantome'))

fantome_par_3 = [] 
fantome_par_3.append(f.Data('fantome_humain/parallele_3/17_keV', 17e3, '17 keV', milieu='fantome'))
fantome_par_3.append(f.Data('fantome_humain/parallele_3/64_keV', 64e3, '64 keV', milieu='fantome'))
fantome_par_3.append(f.Data('fantome_humain/parallele_3/100_keV', 100e3, '100 keV', milieu='fantome'))
fantome_par_3.append(f.Data('fantome_humain/parallele_3/10_MeV', 10e6, '10 MeV', milieu='fantome'))
 

plt.figure(figsize=(20, 15)) 
for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.plot(data_fantome[i].z, data_fantome[i].dose_phi, label='%s cm'%(data_fantome[i].taille_source))
    plt.plot(fantome_par_2[i].z, fantome_par_2[i].dose_phi, label='%s cm'%(fantome_par_2[i].taille_source))
    plt.plot(fantome_par_3[i].z, fantome_par_3[i].dose_phi, label='%s cm'%(fantome_par_3[i].taille_source))
    plt.plot(data_fantome[i].z, data_fantome[i].dose_phi, label='%s cm'%(data_fantome[i].taille_source))
    plt.title(data_fantome[i].get_name())
    plt.xlabel('z (mm)')
    plt.ylabel('Dose normalisée (Gy))')
    plt.legend()




#############################################################################################
# Influence de la divergence du faisceau
#############################################################################################
# Comparaison en fonction de la divergence du faisceau dans la cuve à eau

cuve_div = [] 
cuve_div.append(f.Data('cuve_eau/divergent/17_keV', 17e3, '17 keV', milieu='cuve'))
cuve_div.append(f.Data('cuve_eau/divergent/64_keV', 64e3, '64 keV', milieu='cuve'))
cuve_div.append(f.Data('cuve_eau/divergent/100_keV', 100e3, '100 keV', milieu='cuve'))
cuve_div.append(f.Data('cuve_eau/divergent/10_MeV', 10e6, '10 MeV', milieu='cuve'))

cuve_div_5 = [] 
cuve_div_5.append(f.Data('cuve_eau/divergent_5/17_keV', 17e3, '17 keV', milieu='cuve'))
cuve_div_5.append(f.Data('cuve_eau/divergent_5/64_keV', 64e3, '64 keV', milieu='cuve'))
cuve_div_5.append(f.Data('cuve_eau/divergent_5/100_keV', 100e3, '100 keV', milieu='cuve'))
cuve_div_5.append(f.Data('cuve_eau/divergent_5/10_MeV', 10e6, '10 MeV', milieu='cuve'))

cuve_div_20 = [] 
cuve_div_20.append(f.Data('cuve_eau/divergent_20/17_keV', 17e3, '17 keV', milieu='cuve'))
cuve_div_20.append(f.Data('cuve_eau/divergent_20/64_keV', 64e3, '64 keV', milieu='cuve'))
cuve_div_20.append(f.Data('cuve_eau/divergent_20/100_keV', 100e3, '100 keV', milieu='cuve'))
cuve_div_20.append(f.Data('cuve_eau/divergent_20/10_MeV', 10e6, '10 MeV', milieu='cuve'))

cuve_div_30 = [] 
cuve_div_30.append(f.Data('cuve_eau/divergent_30/17_keV', 17e3, '17 keV', milieu='cuve'))
cuve_div_30.append(f.Data('cuve_eau/divergent_30/64_keV', 64e3, '64 keV', milieu='cuve'))
cuve_div_30.append(f.Data('cuve_eau/divergent_30/100_keV', 100e3, '100 keV', milieu='cuve'))
cuve_div_30.append(f.Data('cuve_eau/divergent_30/10_MeV', 10e6, '10 MeV', milieu='cuve'))

plt.figure(figsize=(20, 15)) 
for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.plot(cuve_div_5[i].z, cuve_div_5[i].dose_phi, label='%s°'%(cuve_div_5[i].divergence))
    plt.plot(cuve_div[i].z, cuve_div[i].dose_phi, label='%s°'%(cuve_div[i].divergence))
    plt.plot(cuve_div_20[i].z, cuve_div_20[i].dose_phi, label='%s°'%(cuve_div_20[i].divergence))
    plt.plot(cuve_div_30[i].z, cuve_div_30[i].dose_phi, label='%s°'%(cuve_div_30[i].divergence))
    plt.title(cuve_div[i].get_name())
    plt.xlabel('z (mm)')
    plt.ylabel('Dose normalisée (Gy))')
    plt.legend()


# Comparaison en fonction de la divergence du faisceau dans le fantôme anthropomorphique

fantome_div = [] 
fantome_div.append(f.Data('fantome_humain/divergent_3/17_keV', 17e3, '17 keV', milieu='fantome'))
fantome_div.append(f.Data('fantome_humain/divergent_3/64_keV', 64e3, '64 keV', milieu='fantome'))
fantome_div.append(f.Data('fantome_humain/divergent_3/100_keV', 100e3, '100 keV', milieu='fantome'))
fantome_div.append(f.Data('fantome_humain/divergent_3/10_MeV', 10e6, '10 MeV', milieu='fantome'))

fantome_div_20 = [] 
fantome_div_20.append(f.Data('fantome_humain/divergent_20/17_keV', 17e3, '17 keV', milieu='fantome'))
fantome_div_20.append(f.Data('fantome_humain/divergent_20/64_keV', 64e3, '64 keV', milieu='fantome'))
fantome_div_20.append(f.Data('fantome_humain/divergent_20/100_keV', 100e3, '100 keV', milieu='fantome'))
fantome_div_20.append(f.Data('fantome_humain/divergent_20/10_MeV', 10e6, '10 MeV', milieu='fantome'))

fantome_div_30 = [] 
fantome_div_30.append(f.Data('fantome_humain/divergent_30/17_keV', 17e3, '17 keV', milieu='fantome'))
fantome_div_30.append(f.Data('fantome_humain/divergent_30/64_keV', 64e3, '64 keV', milieu='fantome'))
fantome_div_30.append(f.Data('fantome_humain/divergent_30/100_keV', 100e3, '100 keV', milieu='fantome'))
fantome_div_30.append(f.Data('fantome_humain/divergent_30/10_MeV', 10e6, '10 MeV', milieu='fantome'))


plt.figure(figsize=(20, 15)) 
for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.plot(fantome_par_1[i].z, fantome_par_1[i].dose_norm_e, label='%s°'%(fantome_par_1[i].divergence))
    plt.plot(fantome_div[i].z, fantome_div[i].dose_norm_e, label='%s°'%(fantome_div[i].divergence))
    plt.plot(fantome_div_20[i].z, fantome_div_20[i].dose_norm_e, label='%s°'%(fantome_div_20[i].divergence))
    plt.plot(fantome_div_30[i].z, fantome_div_30[i].dose_norm_e, label='%s°'%(fantome_div_30[i].divergence))
    plt.title(cuve_div[i].get_name())
    plt.xlabel('z (mm)')
    plt.ylabel('Dose normalisée (Gy))')
    plt.legend() 




###################################################################################
# Temps de calcul et mise à l'équilibre électronique
###################################################################################

cuve = [] 
cuve.append(f.Data('cuve_eau/parallele_5.64/17_keV', 17e3, '17 keV', milieu='cuve'))
cuve.append(f.Data('cuve_eau/parallele_5.64/64_keV', 64e3, '64 keV', milieu='cuve'))
cuve.append(f.Data('cuve_eau/parallele_5.64/100_keV', 100e3, '100 keV', milieu='cuve'))
cuve.append(f.Data('cuve_eau/parallele_5.64/500_keV', 500e3, '500 keV', milieu='cuve'))
cuve.append(f.Data('cuve_eau/parallele_5.64/1_MeV', 1e6, '1 MeV', milieu='cuve'))
cuve.append(f.Data('cuve_eau/parallele_5.64/2_MeV', 2e6, '2 MeV', milieu='cuve'))
cuve.append(f.Data('cuve_eau/parallele_5.64/4_MeV', 4e6, '4 MeV', milieu='cuve'))
cuve.append(f.Data('cuve_eau/parallele_5.64/6_MeV', 6e6, '6 MeV', milieu='cuve'))
cuve.append(f.Data('cuve_eau/parallele_5.64/10_MeV', 10e6, '10 MeV', milieu='cuve'))


energie = []
z_max =[]
time_simulation = []

plt.figure(figsize=(20, 15))
for i in range(len(cuve)):
    energie.append(cuve[i].get_energy())
    time_simulation.append(cuve[i].get_time())
    z_max.append(cuve[i].get_zmax())
    
# Fit des courbes de survie cellulaire avec le modèle linéaire quadratique pour alpha
parameters, covariance = curve_fit(f.func_fit, energie, time_simulation)
fit_k = parameters[0]
fit_a = parameters[1]
# Plot fits et data 
fit = f.func_fit(energie, parameters[0], parameters[1])
    


plt.figure(figsize=(20, 15))  
plt.scatter(energie, time_simulation, label='Data', color='navy')
plt.plot(energie, fit, label='fit: t = $%.3fE^{%.3f}$'%(parameters[0], parameters[1]), color='red')
plt.xlabel("Energie(eV)", fontsize=20)
plt.ylabel("Temps de calcul (s)", fontsize=20)
plt.legend(fontsize=20)
plt.xscale('log')
#plt.yscale('log')

plt.figure(figsize=(20, 15))  
plt.scatter(energie, z_max)
plt.xlabel("Energie(eV)", fontsize=20)
plt.ylabel("Distance de mise à l'équilibre électronique (cm)", fontsize=20)
plt.legend()
plt.xscale('log')
#plt.yscale('log')



##################################################################################
# Comparaion paramètre simulation
##################################################################################


fantome_div_1 = [] 
fantome_div_1.append(f.Data('fantome_humain/divergent_3/17_keV', 17e3, '17 keV', milieu='fantome'))
fantome_div_1.append(f.Data('fantome_humain/divergent_3/64_keV', 64e3, '64 keV', milieu='fantome'))
fantome_div_1.append(f.Data('fantome_humain/divergent_3/100_keV', 100e3, '100 keV', milieu='fantome'))
fantome_div_1.append(f.Data('fantome_humain/divergent_3/10_MeV', 10e6, '10 MeV', milieu='fantome'))

fantome_div_2 = [] 
fantome_div_2.append(f.Data('fantome_humain/divergent_4/17_keV', 17e3, '17 keV', milieu='fantome'))
fantome_div_2.append(f.Data('fantome_humain/divergent_4/64_keV', 64e3, '64 keV', milieu='fantome'))
fantome_div_2.append(f.Data('fantome_humain/divergent_4/100_keV', 100e3, '100 keV', milieu='fantome'))
fantome_div_2.append(f.Data('fantome_humain/divergent_4/10_MeV', 10e6, '10 MeV', milieu='fantome'))

fantome_div_3 = [] 
fantome_div_3.append(f.Data('fantome_humain/divergent_5/17_keV', 17e3, '17 keV', milieu='fantome'))
fantome_div_3.append(f.Data('fantome_humain/divergent_5/64_keV', 64e3, '64 keV', milieu='fantome'))
fantome_div_3.append(f.Data('fantome_humain/divergent_5/100_keV', 100e3, '100 keV', milieu='fantome'))
fantome_div_3.append(f.Data('fantome_humain/divergent_5/10_MeV', 10e6, '10 MeV', milieu='fantome'))


plt.figure(figsize=(20, 15))
for i in range(4):
    plt.subplot(2, 2, i+1)
    plt.plot(fantome_div_1[i].get_z(), fantome_div_1[i].get_dose(), label='C1 = 0.1, C2 = 0.1')
    #plt.plot(fantome_div_2[i].get_z(), fantome_div_2[i].get_dose(), label='0.05')
    plt.plot(fantome_div_3[i].get_z(), fantome_div_3[i].get_dose(), label='C1 = 0.01, C2 = 0.01')
    plt.title("%s"%(fantome_div_1[i].get_name()))
    plt.legend()
    plt.yscale('log')
    plt.xlabel("Profondeur z (cm)")
    plt.ylabel("Dose (Gy)")


plt.figure(figsize=(20, 15)) 
plt.plot(fantome_div_1[2].get_z(), fantome_div_1[2].get_dose(), label='C1 = 0.1, C2 = 0.1')
plt.plot(fantome_div_2[2].get_z(), fantome_div_2[2].get_dose(), label='C1 = 0.1, C2 = 0.1')
plt.plot(fantome_div_3[2].get_z(), fantome_div_3[2].get_dose(), label='C1 = 0.1, C2 = 0.1')
plt.legend(fontsize=20)
plt.xlabel("Profondeur z (cm)", fontsize=20)
plt.ylabel("Dose (Gy)", fontsize=20)


plt.figure(figsize=(20, 15))
plt.plot(fantome_div_1[0].get_z(), (fantome_div_1[0].get_dose()-fantome_div_3[0].get_dose())/fantome_div_3[0].get_dose(), label='0.1')
#plt.legend(fontsize=20)
plt.xlabel("Profondeur z (cm)", fontsize=20)
plt.ylabel("Ecart relatif (-)", fontsize=20)


Ecart_rel_17 = (fantome_div_1[0].get_dose()-fantome_div_2[0].get_dose())/fantome_div_2[0].get_dose()
Ecart_rel_64 = (fantome_div_1[1].get_dose()-fantome_div_2[1].get_dose())/fantome_div_2[1].get_dose()
Ecart_rel_100 = (fantome_div_1[2].get_dose()-fantome_div_2[2].get_dose())/fantome_div_2[2].get_dose()
Ecart_rel_10 = (fantome_div_1[3].get_dose()-fantome_div_2[3].get_dose())/fantome_div_2[3].get_dose()

print("Ecar relatif max à 17 keV : %f"%(max(Ecart_rel_17)))
print("Ecar relatif max à 64 keV : %f"%(max(Ecart_rel_64)))
print("Ecar relatif max à 100 keV : %f"%(max(Ecart_rel_100)))
print("Ecar relatif max à 10 MeV : %f"%(max(Ecart_rel_10)))

print("Rapport de temps de calcul à 17 keV %f"%(float(fantome_div_3[0].time)/float(fantome_div_1[0].time)))
print("Rapport de temps de calcul à 64 keV %f"%(float(fantome_div_3[1].time)/float(fantome_div_1[1].time)))
print("Rapport de temps de calcul à 100 keV %f"%(float(fantome_div_3[2].time)/float(fantome_div_1[2].time)))
print("Rapport de temps de calcul à 10 MeV %f"%(float(fantome_div_3[3].time)/float(fantome_div_1[3].time)))








duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)