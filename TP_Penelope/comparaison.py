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
data_fantome.append(f.Data('fantome_humain/coeur_parallele/17_keV', 17e3, '17 keV', milieu='fantome', divergence=11.3))
data_fantome.append(f.Data('fantome_humain/coeur_parallele/64_keV', 64e3, '64 keV', milieu='fantome', divergence=11.3))
data_fantome.append(f.Data('fantome_humain/coeur_parallele/100_keV', 100e3, '100 keV', milieu='fantome', divergence=11.3))
data_fantome.append(f.Data('fantome_humain/coeur_parallele/10_MeV', 10e6, '10 MeV', milieu='fantome', divergence=11.3))

data_norm = []
for i in range(len(data_fantome)):
    if i==3:
        data_norm.append(0.01*data_fantome[i].dose/data_fantome[i].dose[0])
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





duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)