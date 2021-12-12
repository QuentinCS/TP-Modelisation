#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 17:10:32 2021

@author: quentin
"""

# Code analyse fichier résultats de penelope 
# Faisceau de photons parallèle dans une cuve à eau cylindrique avec 5 cylindres
# Faisceau de photons divergent dans une cuve à eau cylindrique aevc 5 cylindres 
# Faisceau de photons dans un fantôme anthropomorphique sans coeur
# Faisceau de photons dans un fantôme anthropomorphique avec coeur


import matplotlib.pyplot as plt
import time
import func

start_time = time.time()

###################################################################################
# Cuve à eau faisceau parallèle 
###################################################################################

# Extraction des données  
data1 = []
data1.append(func.Data('cuve_eau/parallele_1metre/17_keV', 17, '17 keV', milieu='water'))
data1.append(func.Data('cuve_eau/parallele_1metre/64_keV', 64, '64 keV', milieu='water'))
data1.append(func.Data('cuve_eau/parallele_1metre/100_keV', 100, '100 keV', milieu='water'))
data1.append(func.Data('cuve_eau/parallele_1metre/10_MeV', 1e3, '10 MeV', milieu='water'))

energy = [] 
z_max = []

for i in range(len(data1)):
    energy.append(data1[i].get_energy()) 
    z_max.append(data1[i].get_zmax())

    
plt.figure(figsize=(30,15))
for i in range(len(data1)):
    plt.subplot(2, 2, i+1)
    plt.plot(data1[i].get_z(), data1[i].get_dose(), label='%s' %(data1[i].get_name()), color='navy' )
    plt.suptitle("Rendement en profondeur pour un faisceau de photon dans une cuve à eau \n pour un faisceau parallèle", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Dose (mGy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data1)):
    plt.errorbar(data1[i].get_z(), data1[i].get_dose(), yerr=data1[i].get_dose_err(), label='%s' %(data1[i].get_name()))
plt.suptitle("Rendement en profondeur pour un faisceau de photon dans une cuve à eau \n pour un faisceau parallèle", fontsize=30)
plt.xlabel("z (cm)", fontsize=20)
plt.ylabel("Dose (mGy)", fontsize=20)
plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(10,6))
for i in range(len(data1)):
    plt.scatter(energy, z_max, label=data1[i].get_name(), color='navy')
plt.title("Distance de mise à l'équilibre électronique \n pour un faisceau parallèle", fontsize=20)
plt.xlabel("Energie (eV)", fontsize=15)
plt.ylabel("$z_{max} (cm)$", fontsize=15)
plt.legend(prop={'size': 10})
plt.xscale('log')
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data1)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data1[i].theta, data1[i].pdf_theta_elec, yerr=data1[i].pdf_theta_elec_err, label='%s'%(data1[i].get_name()), color='navy')
    plt.suptitle('Distribution angulaire des électrons cuve à eau \n pour un faisceau parallèle', fontsize=15)
    plt.xlabel('$\Theta$ (degré)', fontsize=15)
    plt.ylabel('PDF ($sr^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data1)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data1[i].energy_tr, data1[i].pdf_tr, yerr=data1[i].pdf_tr_err, label='%s'%(data1[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons transmis cuve à eau \n pour un faisceau parallèle', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data1)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data1[i].energy_bck, data1[i].pdf_bck, yerr=data1[i].pdf_bck_err, label='%s'%(data1[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons rétrodiffusés cuve à eau \n pour un faisceau parallèle', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()



###################################################################################
# Cuve à eau faisceau divergent
###################################################################################

# Extraction des données
data2 = []
data2.append(func.Data('cuve_eau/divergent/17_keV', 17, '17 keV', milieu='water'))
data2.append(func.Data('cuve_eau/divergent/64_keV', 64, '64 keV', milieu='water'))
data2.append(func.Data('cuve_eau/divergent/100_keV', 100, '100 keV', milieu='water'))
data2.append(func.Data('cuve_eau/divergent/10_MeV', 1e3, '10 MeV', milieu='water'))

energy = []
z_max = []

for i in range(len(data2)):
    energy.append(data2[i].get_energy()) 
    z_max.append(data2[i].get_zmax())

    
plt.figure(figsize=(30,15))
for i in range(len(data2)):
    plt.subplot(2, 2, i+1)
    plt.plot(data2[i].get_z(), data2[i].get_dose(), label='%s' %(data2[i].get_name()), color='navy' )
    plt.suptitle("Rendement en profondeur pour un faisceau de photon dans une cuve à eau \n pour un faisceau divergent", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Dose (mGy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data2)):
    plt.errorbar(data2[i].get_z(), data2[i].get_dose(), yerr=data2[i].get_dose_err(), label='%s' %(data2[i].get_name()))
plt.suptitle("Rendement en profondeur pour un faisceau de photon dans une cuve à eau \n pour un faisceau divergent", fontsize=30)
plt.xlabel("z (cm)", fontsize=20)
plt.ylabel("Dose (mGy)", fontsize=20)
plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(10,6))
for i in range(len(data2)):
    plt.scatter(energy, z_max, label=data2[i].get_name(), color='navy')
plt.title("Distance de mise à l'équilibre électronique \n pour un faisceau divergent", fontsize=20)
plt.xlabel("Energie (eV)", fontsize=15)
plt.ylabel("$z_{max} (cm)$", fontsize=15)
plt.legend(prop={'size': 10})
plt.xscale('log')
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data2)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data2[i].theta, data2[i].pdf_theta_elec, yerr=data2[i].pdf_theta_elec_err, label='%s'%(data2[i].get_name()), color='navy')
    plt.suptitle('Distribution angulaire des électrons cuve à eau \n pour un faisceau divergent', fontsize=15)
    plt.xlabel('$\Theta$ (degré)', fontsize=15)
    plt.ylabel('PDF ($sr^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data2)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data2[i].energy_tr, data2[i].pdf_tr, yerr=data2[i].pdf_tr_err, label='%s'%(data2[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons transmis cuve à eau \n pour un faisceau divergent', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data2)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data2[i].energy_bck, data2[i].pdf_bck, yerr=data2[i].pdf_bck_err, label='%s'%(data2[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons rétrodiffusés cuve à eau \n pour un faisceau divergent', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()







###################################################################################
# Fantôme anthropomorphe sans coeur 
###################################################################################

# Extraction des données
data = []
data.append(func.Data('fantome_humain/fantome_patient_sans_coeur/17_keV', 17, '17 keV', milieu='fantome'))
data.append(func.Data('fantome_humain/fantome_patient_sans_coeur/64_keV', 64, '64 keV', milieu='fantome'))
data.append(func.Data('fantome_humain/fantome_patient_sans_coeur/100_keV', 100, '100 keV', milieu='fantome'))
data.append(func.Data('fantome_humain/fantome_patient_sans_coeur/10_MeV', 1e3, '10 MeV', milieu='fantome'))

    
plt.figure(figsize=(30,15))
for i in range(len(data)):
    plt.subplot(2, 2, i+1)
    plt.plot(data[i].get_z(), data[i].get_dose(), label='%s' %(data[i].get_name()), color='navy' )
    plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique sans coeur", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Dose (mGy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data)):
    plt.errorbar(data[i].get_z(), data[i].get_dose(), yerr=data[i].get_dose_err(), label='%s' %(data[i].get_name()))
plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique sans coeur", fontsize=30)
plt.xlabel("z (cm)", fontsize=20)
plt.ylabel("Dose (mGy)", fontsize=20)
plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data[i].theta, data[i].pdf_theta_elec, yerr=data[i].pdf_theta_elec_err, label='%s'%(data[i].get_name()), color='navy')
    plt.suptitle('Distribution angulaire des électrons', fontsize=15)
    plt.xlabel('$\Theta$ (degré)', fontsize=15)
    plt.ylabel('PDF ($sr^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data[i].energy_tr, data[i].pdf_tr, yerr=data[i].pdf_tr_err, label='%s'%(data[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons transmis', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data[i].energy_bck, data[i].pdf_bck, yerr=data[i].pdf_bck_err, label='%s'%(data[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons rétrodiffusés', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()



















duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)