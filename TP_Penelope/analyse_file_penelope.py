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
    plt.errorbar(data1[i].get_z(), data1[i].get_dose(), yerr=data1[i].get_dose_err(), label='%s' %(data1[i].get_name()), color='navy' )
    plt.suptitle("Rendement en profondeur pour un faisceau de photon dans une cuve à eau \n pour un faisceau parallèle", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Dose (Gy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data1)):
    plt.errorbar(data1[i].get_z(), data1[i].get_dose(), yerr=data1[i].get_dose_err(), label='%s' %(data1[i].get_name()))
plt.suptitle("Rendement en profondeur pour un faisceau de photon dans une cuve à eau \n pour un faisceau parallèle", fontsize=30)
plt.xlabel("z (cm)", fontsize=20)
plt.ylabel("Dose (Gy)", fontsize=20)
plt.legend(prop={'size': 20})
plt.show()
"""
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
"""


###################################################################################
# Cuve à eau faisceau divergent
###################################################################################

# Extraction des données
data2 = []
data2.append(func.Data('cuve_eau/divergent/17_keV', 17, '17 keV', milieu='water', divergence=11.3))
data2.append(func.Data('cuve_eau/divergent/64_keV', 64, '64 keV', milieu='water', divergence=11.3))
data2.append(func.Data('cuve_eau/divergent/100_keV', 100, '100 keV', milieu='water', divergence=11.3))
data2.append(func.Data('cuve_eau/divergent/10_MeV', 1e3, '10 MeV', milieu='water', divergence=11.3))

energy = []
z_max = []

for i in range(len(data2)):
    energy.append(data2[i].get_energy()) 
    z_max.append(data2[i].get_zmax())

    
plt.figure(figsize=(30,15))
for i in range(len(data2)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data2[i].get_z(), data2[i].get_dose(), yerr=data2[i].get_dose_err(), label='%s' %(data2[i].get_name()), color='navy' )
    plt.suptitle("Rendement en profondeur pour un faisceau de photon dans une cuve à eau \n pour un faisceau divergent", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Dose (Gy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data2)):
    plt.errorbar(data2[i].get_z(), data2[i].get_dose(), yerr=data2[i].get_dose_err(), label='%s' %(data2[i].get_name()))
plt.suptitle("Rendement en profondeur pour un faisceau de photon dans une cuve à eau \n pour un faisceau divergent", fontsize=30)
plt.xlabel("z (cm)", fontsize=20)
plt.ylabel("Dose (Gy)", fontsize=20)
plt.legend(prop={'size': 20})
plt.show()

"""
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
"""


###################################################################################
# Fantôme anthropomorphe sans coeur 
###################################################################################
"""
# Extraction des données 
data = []
data.append(func.Data('fantome_humain/sans_coeur/17_keV', 17, '17 keV', milieu='fantome'))
data.append(func.Data('fantome_humain/sans_coeur/64_keV', 64, '64 keV', milieu='fantome'))
data.append(func.Data('fantome_humain/sans_coeur/100_keV', 100, '100 keV', milieu='fantome'))
data.append(func.Data('fantome_humain/sans_coeur/10_MeV', 1e3, '10 MeV', milieu='fantome'))

    
plt.figure(figsize=(30,15))
for i in range(len(data)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data[i].get_z(), data[i].get_dose(), yerr=data[i].get_dose_err(), label='%s' %(data[i].get_name()), color='navy' )
    plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique sans coeur", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Dose (Gy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data)):
    plt.errorbar(data[i].get_z(), data[i].get_dose(), yerr=data[i].get_dose_err(), label='%s' %(data[i].get_name()))
plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique sans coeur", fontsize=30)
plt.xlabel("z (cm)", fontsize=20)
plt.ylabel("Dose (Gy)", fontsize=20)
plt.legend(prop={'size': 20})
plt.show()
"""
"""
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
"""

###################################################################################
# Fantôme anthropomorphe avec coeur 
###################################################################################

# Extraction des données
data3 = []
data3.append(func.Data('fantome_humain/coeur/17_keV', 17, '17 keV', milieu='fantome avec coeur'))
data3.append(func.Data('fantome_humain/coeur/64_keV', 64, '64 keV', milieu='fantome avec coeur'))
data3.append(func.Data('fantome_humain/coeur/100_keV', 100, '100 keV', milieu='fantome avec coeur'))
data3.append(func.Data('fantome_humain/coeur/10_MeV', 1e3, '10 MeV', milieu='fantome avec coeur'))

    
plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].get_z(), data3[i].get_dose(), yerr=data3[i].get_dose_err(), label='%s' %(data3[i].get_name()), color='navy' )
    plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique avec coeur", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Dose (Gy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.errorbar(data3[i].get_z(), data3[i].get_dose(), yerr=data3[i].get_dose_err(), label='%s' %(data3[i].get_name()))
plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique avec coeur", fontsize=30)
plt.xlabel("z (cm)", fontsize=20)
plt.ylabel("Dose (Gy)", fontsize=20)
plt.legend(prop={'size': 20})
plt.show()

"""
plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].theta, data3[i].pdf_theta_elec, yerr=data3[i].pdf_theta_elec_err, label='%s'%(data3[i].get_name()), color='navy')
    plt.suptitle('Distribution angulaire des électrons', fontsize=15)
    plt.xlabel('$\Theta$ (degré)', fontsize=15)
    plt.ylabel('PDF ($sr^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].energy_tr, data3[i].pdf_tr, yerr=data3[i].pdf_tr_err, label='%s'%(data3[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons transmis', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].energy_bck, data3[i].pdf_bck, yerr=data3[i].pdf_bck_err, label='%s'%(data3[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons rétrodiffusés', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()
"""

###################################################################################
# Fantôme anthropomorphe avec coeur faisceau divergent
###################################################################################

# Extraction des données
data4 = []
data4.append(func.Data('fantome_humain/coeur_divergent/17_keV', 17, '17 keV', milieu='fantome avec coeur', divergence=11.3))
data4.append(func.Data('fantome_humain/coeur_divergent/64_keV', 64, '64 keV', milieu='fantome avec coeur', divergence=11.3))
data4.append(func.Data('fantome_humain/coeur_divergent/100_keV', 100, '100 keV', milieu='fantome avec coeur', divergence=11.3))
data4.append(func.Data('fantome_humain/coeur_divergent/10_MeV', 1e3, '10 MeV', milieu='fantome avec coeur', divergence=11.3))

    
plt.figure(figsize=(30,15))
for i in range(len(data4)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data4[i].get_z(), data4[i].get_dose(), yerr=data4[i].get_dose_err(), label='%s' %(data4[i].get_name()), color='navy' )
    plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique avec coeur faisceau divergent", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Dose (Gy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data4)):
    plt.errorbar(data4[i].get_z(), data4[i].get_dose(), yerr=data4[i].get_dose_err(), label='%s' %(data4[i].get_name()))
plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique avec coeur faisceau divergent", fontsize=30)
plt.xlabel("z (cm)", fontsize=20)
plt.ylabel("Dose (Gy)", fontsize=20)
plt.legend(prop={'size': 20})
plt.show()

"""
plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].theta, data3[i].pdf_theta_elec, yerr=data3[i].pdf_theta_elec_err, label='%s'%(data3[i].get_name()), color='navy')
    plt.suptitle('Distribution angulaire des électrons', fontsize=15)
    plt.xlabel('$\Theta$ (degré)', fontsize=15)
    plt.ylabel('PDF ($sr^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].energy_tr, data3[i].pdf_tr, yerr=data3[i].pdf_tr_err, label='%s'%(data3[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons transmis', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].energy_bck, data3[i].pdf_bck, yerr=data3[i].pdf_bck_err, label='%s'%(data3[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons rétrodiffusés', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()
"""



######################################################################################
# Comparaison parralèle/divergent
######################################################################################


plt.figure(figsize=(30,15))
for i in range(len(data4)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data4[i].get_z(), data4[i].get_dose(), yerr=data4[i].get_dose_err(), label='%s' %(data4[i].get_faisceau()))
    plt.errorbar(data3[i].get_z(), data3[i].get_dose(), yerr=data3[i].get_dose_err(), label='%s' %(data3[i].get_faisceau()))
    plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique avec coeur", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    #plt.yscale('log')
    plt.ylabel("Dose (Gy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()






#########################################################################################
# Cartes de dose 
#########################################################################################
# Traçage des cartes de dose dans la cuve à eau 


data_cuve = [] 
data_cuve.append(func.Data('cuve_eau/divergent/17_keV', 17, '17 keV', milieu='cuve'))
data_cuve.append(func.Data('cuve_eau/divergent/64_keV', 64, '64 keV', milieu='cuve'))
data_cuve.append(func.Data('cuve_eau/divergent/100_keV', 100, '100 keV', milieu='cuve'))
data_cuve.append(func.Data('cuve_eau/divergent/10_MeV', 1e3, '10 MeV', milieu='cuve'))

plt.figure(figsize=(20, 15))
plt.subplot(2, 2, 1)
plt.ylabel("Rayon r (cm)")
plt.xlabel("Profondeur z (cm)")
plt.title('17 keV')
plt.imshow(data_cuve[0].Dose2D, extent=[data_cuve[0].z_scale[0], data_cuve[0].z_scale[1], data_cuve[0].r_scale[0], data_cuve[0].r_scale[1]])
plt.subplot(2, 2, 2)
plt.title('64 keV')
plt.ylabel("Rayon r (cm)")
plt.xlabel("Profondeur z (cm)")
plt.imshow(data_cuve[1].Dose2D, extent=[data_cuve[1].z_scale[0], data_cuve[1].z_scale[1], data_cuve[1].r_scale[0], data_cuve[1].r_scale[1]])
plt.subplot(2, 2, 3)
plt.title('100 keV')
plt.ylabel("Rayon r (cm)")
plt.xlabel("Profondeur z (cm)")
plt.imshow(data_cuve[2].Dose2D, extent=[data_cuve[2].z_scale[0], data_cuve[2].z_scale[1], data_cuve[2].r_scale[0], data_cuve[2].r_scale[1]])
plt.subplot(2, 2, 4)
plt.title('10 MeV')
plt.ylabel("Rayon r (cm)")
plt.xlabel("Profondeur z (cm)")
plt.imshow(data_cuve[3].Dose2D, extent=[data_cuve[3].z_scale[0], data_cuve[3].z_scale[1], data_cuve[3].r_scale[0], data_cuve[3].r_scale[1]])
#plt.colorbar(shrink=0.5) 
plt.suptitle('Carte de dose dans une cuve à eau')

#Traçage des cartes de dose dans le fantôme 
data_fantome = [] 
data_fantome.append(func.Data('fantome_humain/coeur_divergent_3/17_keV', 17e3, '17 keV', milieu='fantome'))
data_fantome.append(func.Data('fantome_humain/coeur_divergent_3/64_keV', 64e3, '64 keV', milieu='fantome'))
data_fantome.append(func.Data('fantome_humain/coeur_divergent_3/100_keV', 100e3, '100 keV', milieu='fantome'))
data_fantome.append(func.Data('fantome_humain/coeur_divergent_3/10_MeV', 10e6, '10 MeV', milieu='fantome'))

plt.figure(figsize=(20, 15))
plt.subplot(4, 1, 1)
plt.title('17 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome[0].Dose2D, extent=[data_fantome[0].z_scale[0], data_fantome[0].z_scale[1], data_fantome[0].r_scale[0], data_fantome[0].r_scale[1]])
plt.subplot(4, 1, 2)
plt.title('64 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome[1].Dose2D, extent=[data_fantome[1].z_scale[0], data_fantome[1].z_scale[1], data_fantome[1].r_scale[0], data_fantome[1].r_scale[1]])
plt.subplot(4, 1, 3)
plt.title('100 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome[2].Dose2D, extent=[data_fantome[2].z_scale[0], data_fantome[2].z_scale[1], data_fantome[2].r_scale[0], data_fantome[2].r_scale[1]])
plt.subplot(4, 1, 4)
plt.title('10 MeV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome[3].Dose2D, extent=[data_fantome[3].z_scale[0], data_fantome[3].z_scale[1], data_fantome[3].r_scale[0], data_fantome[3].r_scale[1]])
#plt.colorbar(shrink=0.5) 
plt.suptitle('Carte de dose dans un fantôme anthropomorphique')
plt.xlabel("Profondeur z (cm)")


#test = func.matrice_revolution(data_test[0].Dose2d)
"""
plt.figure(figsize=(50, 25))
plt.imshow(data_test[0].Dose2D, extent=[data_test[0].z_scale[0], data_test[0].z_scale[1], data_test[0].r_scale[0], data_test[0].r_scale[1]])
plt.xlabel("Profondeur z (cm)")
plt.ylabel("Rayon r (cm)")


plt.figure(figsize=(50, 25))
plt.imshow(data_test[1].Dose2D, extent=[data_test[1].z_scale[0], data_test[1].z_scale[1], data_test[1].r_scale[0], data_test[1].r_scale[1]])
plt.xlabel("Profondeur z (cm)")
plt.ylabel("Rayon r (cm)")
"""
"""
plt.figure(figsize=(50, 25))
plt.imshow(data_test[2].Dose2D, extent=[data_test[2].z_scale[0], data_test[2].z_scale[1], data_test[2].r_scale[0], data_test[2].r_scale[1]])
plt.xlabel("Profondeur z (cm)")
plt.ylabel("Rayon r (cm)")

plt.figure(figsize=(50, 25))
plt.imshow(data_test[2].dose2d_cuve[0], extent=[data_test[2].z_scale[0], data_test[2].z_scale[1], data_test[2].r_scale[0], data_test[2].r_scale[1]])
plt.xlabel("Profondeur z (cm)")
plt.ylabel("Rayon r (cm)")
"""




duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)