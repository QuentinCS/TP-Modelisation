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
data1.append(func.Data('cuve_eau/parallele_5.64/17_keV', 17, '17 keV', milieu='cuve'))
data1.append(func.Data('cuve_eau/parallele_5.64/64_keV', 64, '64 keV', milieu='cuve'))
data1.append(func.Data('cuve_eau/parallele_5.64/100_keV', 100, '100 keV', milieu='cuve'))
data1.append(func.Data('cuve_eau/parallele_5.64/10_MeV', 1e3, '10 MeV', milieu='cuve'))


plt.figure(figsize=(30,15))
for i in range(len(data1)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data1[i].get_z(), data1[i].get_dose(), yerr=data1[i].get_dose_err(), label='%s' %(data1[i].get_name()), color='navy' )
    #plt.suptitle("Rendement en profondeur pour un faisceau de photon dans une cuve à eau \n pour un faisceau parallèle", fontsize=30)
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
data2.append(func.Data('cuve_eau/divergent/17_keV', 17, '17 keV', milieu='cuve'))
data2.append(func.Data('cuve_eau/divergent/64_keV', 64, '64 keV', milieu='cuve'))
data2.append(func.Data('cuve_eau/divergent/100_keV', 100, '100 keV', milieu='cuve'))
data2.append(func.Data('cuve_eau/divergent/10_MeV', 1e3, '10 MeV', milieu='cuve'))

energy = []
z_max = []

for i in range(len(data2)):
    energy.append(data2[i].get_energy()) 
    z_max.append(data2[i].get_zmax())

    
plt.figure(figsize=(30,15))
for i in range(len(data2)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data2[i].get_z(), data2[i].get_dose(), yerr=data2[i].get_dose_err(), label='%s' %(data2[i].get_name()), color='navy' )
    #plt.suptitle("Rendement en profondeur pour un faisceau de photon dans une cuve à eau \n pour un faisceau divergent", fontsize=30)
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
# Fantôme anthropomorphe avec faisceau parallèle
###################################################################################

# Extraction des données
data3 = []
data3.append(func.Data('fantome_humain/parallele/17_keV', 17, '17 keV', milieu='fantome'))
data3.append(func.Data('fantome_humain/parallele/64_keV', 64, '64 keV', milieu='fantome'))
data3.append(func.Data('fantome_humain/parallele/100_keV', 100, '100 keV', milieu='fantome'))
data3.append(func.Data('fantome_humain/parallele/10_MeV', 1e3, '10 MeV', milieu='fantome'))

    
plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].get_z(), data3[i].get_dose(), yerr=data3[i].get_dose_err(), label='%s' %(data3[i].get_name()), color='navy' )
    #plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique avec faisceau parallèle", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Dose (Gy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.errorbar(data3[i].get_z(), data3[i].get_dose(), yerr=data3[i].get_dose_err(), label='%s' %(data3[i].get_name()))
plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique avec faisceau parallèle", fontsize=30)
plt.xlabel("z (cm)", fontsize=20)
plt.ylabel("Dose (Gy)", fontsize=20)
plt.legend(prop={'size': 20})
plt.show()


plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].theta, data3[i].pdf_theta_elec, yerr=data3[i].pdf_theta_elec_err, label='%s'%(data3[i].get_name()), color='navy')
    #plt.suptitle('Distribution angulaire des électrons fantôme', fontsize=15)
    plt.xlabel('$\Theta$ (degré)', fontsize=15)
    plt.ylabel('PDF ($sr^{-1}.particle^{-1}$)', fontsize=15)
    plt.ylim(0, 1.2*max(data3[i].pdf_theta_elec))
    #if i == 3 or i == 2 or i ==1:
    #    plt.ylim(0, 1.2*max(data3[i].pdf_theta_elec))
    #plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].energy_tr, data3[i].pdf_tr, yerr=data3[i].pdf_tr_err, label='%s'%(data3[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons transmis fantôme', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()

plt.figure(figsize=(30,15))
for i in range(len(data3)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data3[i].energy_bck, data3[i].pdf_bck, yerr=data3[i].pdf_bck_err, label='%s'%(data3[i].get_name()), color='navy')
    plt.suptitle('Distribution en énergie des électrons rétrodiffusés fantôme', fontsize=15)
    plt.xlabel('E (MeV)', fontsize=15)
    plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
    plt.xscale('log')
    plt.legend(prop={'size': 20})
plt.legend()


###################################################################################
# Fantôme anthropomorphe avec faisceau divergent
###################################################################################

# Extraction des données
data4 = []
data4.append(func.Data('fantome_humain/divergent_3/17_keV', 17, '17 keV', milieu='fantome'))
data4.append(func.Data('fantome_humain/divergent_3/64_keV', 64, '64 keV', milieu='fantome'))
data4.append(func.Data('fantome_humain/divergent_3/100_keV', 100, '100 keV', milieu='fantome'))
data4.append(func.Data('fantome_humain/divergent_3/10_MeV', 1e3, '10 MeV', milieu='fantome'))

    
plt.figure(figsize=(30,15))
for i in range(len(data4)):
    plt.subplot(2, 2, i+1)
    plt.errorbar(data4[i].get_z(), data4[i].get_dose(), yerr=data4[i].get_dose_err(), label='%s' %(data4[i].get_name()), color='navy' )
    #plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique faisceau divergent", fontsize=30)
    plt.xlabel("z (cm)", fontsize=20)
    plt.ylabel("Dose (Gy)", fontsize=20)
    plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(30,15))
for i in range(len(data4)):
    plt.errorbar(data4[i].get_z(), data4[i].get_dose(), yerr=data4[i].get_dose_err(), label='%s' %(data4[i].get_name()))
plt.suptitle("Rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique faisceau divergent", fontsize=30)
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
#    plt.errorbar(data3[i].get_z(), data3[i].get_dose(), yerr=data3[i].get_dose_err(), label='%s' %(data3[i].get_faisceau()))
    plt.suptitle("Comparaison rendement en profondeur pour un faisceau de photon dans un fantôme \nanthropomorphique", fontsize=30)
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
data_cuve.append(func.Data('cuve_eau/parallele_5.64/17_keV', 17, '17 keV', milieu='cuve'))
data_cuve.append(func.Data('cuve_eau/parallele_5.64/64_keV', 64, '64 keV', milieu='cuve'))
data_cuve.append(func.Data('cuve_eau/parallele_5.64/100_keV', 100, '100 keV', milieu='cuve'))
data_cuve.append(func.Data('cuve_eau/parallele_5.64/10_MeV', 1e3, '10 MeV', milieu='cuve'))

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
#plt.suptitle('Carte de dose dans une cuve à eau \n avec un faisceau parallèle', fontsize=30)

# Cuve à eau divergent
data_cuve_div = [] 
data_cuve_div.append(func.Data('cuve_eau/divergent/17_keV', 17, '17 keV', milieu='cuve'))
data_cuve_div.append(func.Data('cuve_eau/divergent/64_keV', 64, '64 keV', milieu='cuve'))
data_cuve_div.append(func.Data('cuve_eau/divergent/100_keV', 100, '100 keV', milieu='cuve'))
data_cuve_div.append(func.Data('cuve_eau/divergent/10_MeV', 1e3, '10 MeV', milieu='cuve'))

plt.figure(figsize=(20, 15))
plt.subplot(2, 2, 1)
plt.ylabel("Rayon r (cm)")
plt.xlabel("Profondeur z (cm)")
plt.title('17 keV')
plt.imshow(data_cuve_div[0].Dose2D, extent=[data_cuve_div[0].z_scale[0], data_cuve_div[0].z_scale[1], data_cuve_div[0].r_scale[0], data_cuve_div[0].r_scale[1]])
plt.subplot(2, 2, 2)
plt.title('64 keV')
plt.ylabel("Rayon r (cm)")
plt.xlabel("Profondeur z (cm)")
plt.imshow(data_cuve_div[1].Dose2D, extent=[data_cuve_div[1].z_scale[0], data_cuve_div[1].z_scale[1], data_cuve_div[1].r_scale[0], data_cuve_div[1].r_scale[1]])
plt.subplot(2, 2, 3)
plt.title('100 keV')
plt.ylabel("Rayon r (cm)")
plt.xlabel("Profondeur z (cm)")
plt.imshow(data_cuve_div[2].Dose2D, extent=[data_cuve_div[2].z_scale[0], data_cuve_div[2].z_scale[1], data_cuve_div[2].r_scale[0], data_cuve_div[2].r_scale[1]])
plt.subplot(2, 2, 4)
plt.title('10 MeV')
plt.ylabel("Rayon r (cm)")
plt.xlabel("Profondeur z (cm)")
plt.imshow(data_cuve_div[3].Dose2D, extent=[data_cuve_div[3].z_scale[0], data_cuve_div[3].z_scale[1], data_cuve_div[3].r_scale[0], data_cuve_div[3].r_scale[1]])
#plt.colorbar(shrink=0.5) 
#plt.suptitle('Carte de dose dans une cuve à eau \n avec un faisceau divergent', fontsize=30)


#Traçage des cartes de dose dans le fantôme 
data_fantome = [] 
data_fantome.append(func.Data('fantome_humain/parallele/17_keV', 17e3, '17 keV', milieu='fantome'))
data_fantome.append(func.Data('fantome_humain/parallele/64_keV', 64e3, '64 keV', milieu='fantome'))
data_fantome.append(func.Data('fantome_humain/parallele/100_keV', 100e3, '100 keV', milieu='fantome'))
data_fantome.append(func.Data('fantome_humain/parallele/10_MeV', 10e6, '10 MeV', milieu='fantome'))

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
plt.suptitle('Carte de dose dans un fantôme \nanthropomorphique', fontsize=30)
plt.xlabel("Profondeur z (cm)")

 
for energy in range(4):
    print("A %s :"%(data_fantome[energy].get_name()))
    print("La dose moyenne au coeur est %.4e Gy"%(data_fantome[energy].get_dose_moyenne_coeur()))
    print("La dose max au coeur est %.4e Gy"%(data_fantome[energy].get_dose_max_coeur()))
    print("La dose moyenne dans le fantôme est %.4e Gy"%(data_fantome[energy].get_dose_moyenne()))
    print("La dose max dans la fantôme est %.4e Gy"%(data_fantome[energy].get_dose_max()))
    print("La dose max à la peau est %.4e Gy "%(data_fantome[energy].get_dose_peau()))
    print("-----------------------------------------------\n")




"""
#Traçage des cartes de dose dans le fantôme 
data_fantome2 = [] 
data_fantome2.append(func.Data('fantome_humain/divergent_4/17_keV', 17e3, '17 keV', milieu='fantome'))
data_fantome2.append(func.Data('fantome_humain/divergent_4/64_keV', 64e3, '64 keV', milieu='fantome'))
data_fantome2.append(func.Data('fantome_humain/divergent_4/100_keV', 100e3, '100 keV', milieu='fantome'))
data_fantome2.append(func.Data('fantome_humain/divergent_4/10_MeV', 10e6, '10 MeV', milieu='fantome'))

plt.figure(figsize=(20, 15))
plt.subplot(4, 1, 1)
plt.title('17 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome2[0].Dose2D, extent=[data_fantome2[0].z_scale[0], data_fantome2[0].z_scale[1], data_fantome2[0].r_scale[0], data_fantome2[0].r_scale[1]])
plt.subplot(4, 1, 2)
plt.title('64 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome2[1].Dose2D, extent=[data_fantome2[1].z_scale[0], data_fantome2[1].z_scale[1], data_fantome2[1].r_scale[0], data_fantome2[1].r_scale[1]])
plt.subplot(4, 1, 3)
plt.title('100 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome2[2].Dose2D, extent=[data_fantome2[2].z_scale[0], data_fantome2[2].z_scale[1], data_fantome2[2].r_scale[0], data_fantome2[2].r_scale[1]])
plt.subplot(4, 1, 4)
plt.title('10 MeV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome2[3].Dose2D, extent=[data_fantome2[3].z_scale[0], data_fantome2[3].z_scale[1], data_fantome2[3].r_scale[0], data_fantome2[3].r_scale[1]])
#plt.colorbar(shrink=0.5) 
plt.suptitle('Carte de dose dans un fantôme \nanthropomorphique test paramètres \n(c1 =0.1, c2 =0.1)', fontsize=30)
plt.xlabel("Profondeur z (cm)")
"""


#Traçage des cartes de dose dans le fantôme 
data_fantome3 = [] 
data_fantome3.append(func.Data('fantome_humain/parallele_1/17_keV', 17e3, '17 keV', milieu='fantome'))
data_fantome3.append(func.Data('fantome_humain/parallele_1/64_keV', 64e3, '64 keV', milieu='fantome'))
data_fantome3.append(func.Data('fantome_humain/parallele_1/100_keV', 100e3, '100 keV', milieu='fantome'))
data_fantome3.append(func.Data('fantome_humain/parallele_1/10_MeV', 10e6, '10 MeV', milieu='fantome'))

plt.figure(figsize=(20, 15))
plt.subplot(4, 1, 1)
plt.title('17 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome3[0].Dose2D, extent=[data_fantome3[0].z_scale[0], data_fantome3[0].z_scale[1], data_fantome3[0].r_scale[0], data_fantome3[0].r_scale[1]])
plt.subplot(4, 1, 2)
plt.title('64 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome3[1].Dose2D, extent=[data_fantome3[1].z_scale[0], data_fantome3[1].z_scale[1], data_fantome3[1].r_scale[0], data_fantome3[1].r_scale[1]])
plt.subplot(4, 1, 3)
plt.title('100 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome3[2].Dose2D, extent=[data_fantome3[2].z_scale[0], data_fantome3[2].z_scale[1], data_fantome3[2].r_scale[0], data_fantome3[2].r_scale[1]])
plt.subplot(4, 1, 4)
plt.title('10 MeV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome3[3].Dose2D, extent=[data_fantome3[3].z_scale[0], data_fantome3[3].z_scale[1], data_fantome3[3].r_scale[0], data_fantome3[3].r_scale[1]])
#plt.colorbar(shrink=0.5) 
#plt.suptitle('Carte de dose dans un fantôme \nanthropomorphique avec faisceau parallèle de 1cm', fontsize=30)
plt.xlabel("Profondeur z (cm)")
 


data_fantome4 = [] 
data_fantome4.append(func.Data('fantome_humain/parallele/17_keV', 17e3, '17 keV', milieu='fantome'))
data_fantome4.append(func.Data('fantome_humain/parallele/64_keV', 64e3, '64 keV', milieu='fantome'))
data_fantome4.append(func.Data('fantome_humain/parallele/100_keV', 100e3, '100 keV', milieu='fantome'))
data_fantome4.append(func.Data('fantome_humain/parallele/10_MeV', 10e6, '10 MeV', milieu='fantome'))
plt.figure(figsize=(20, 15))
plt.subplot(4, 1, 1)
plt.title('17 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome4[0].Dose2D, extent=[data_fantome4[0].z_scale[0], data_fantome4[0].z_scale[1], data_fantome4[0].r_scale[0], data_fantome4[0].r_scale[1]])
plt.subplot(4, 1, 2)
plt.title('64 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome4[1].Dose2D, extent=[data_fantome4[1].z_scale[0], data_fantome4[1].z_scale[1], data_fantome4[1].r_scale[0], data_fantome4[1].r_scale[1]])
plt.subplot(4, 1, 3)
plt.title('100 keV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome4[2].Dose2D, extent=[data_fantome4[2].z_scale[0], data_fantome4[2].z_scale[1], data_fantome4[2].r_scale[0], data_fantome4[2].r_scale[1]])
plt.subplot(4, 1, 4)
plt.title('10 MeV')
plt.ylabel("Rayon r (cm)")
plt.imshow(data_fantome4[3].Dose2D, extent=[data_fantome4[3].z_scale[0], data_fantome4[3].z_scale[1], data_fantome4[3].r_scale[0], data_fantome4[3].r_scale[1]])
#plt.suptitle('Carte de dose dans un fantôme \nanthropomorphique avec faisceau parallèle de 3.75cm', fontsize=30)





duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)