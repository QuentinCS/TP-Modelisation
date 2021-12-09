#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 17:10:32 2021

@author: quentin
"""

# Code analyse fichier depth-dose.dat de penelope 
# Faisceau de photons dans une cuve à eau cylindrique avec 3 cylindres d'eau 

import matplotlib.pyplot as plt
import time
import func

start_time = time.time()


###################################################################################
# Comparaison dans l'eau avec différentes énergies
###################################################################################

# Extraction des données
data = []
data.append(func.Data('10_MeV_water', 10e3, '10 MeV', milieu='water'))
data.append(func.Data('6_MeV_water', 6e3, '6 MeV', milieu='water'))
data.append(func.Data('4_MeV_water', 4e3, '4 MeV', milieu='water'))
data.append(func.Data('2_MeV_water', 2e3, '2 MeV', milieu='water'))
data.append(func.Data('1_MeV_water', 1e3, '1 MeV', milieu='water'))
data.append(func.Data('500_keV_water', 500, '500 keV', milieu='water'))
data.append(func.Data('100_keV_water', 100, '100 keV', milieu='water'))
data.append(func.Data('64_keV_water', 64, '64 keV', milieu='water'))
data.append(func.Data('17_keV_water', 17, '17 keV', milieu='water'))

energy = []
z_max = []

for i in range(len(data)):
    #data[i].set_data()
    energy.append(data[i].get_energy())
    z_max.append(data[i].get_zmax())
    
plt.figure(figsize=(15,8))
for i in range(len(data)):
    plt.plot(data[i].get_z(), data[i].get_dose(), label='%s' %(data[i].get_name()))
plt.title("Rendement en profondeur pour un faisceau de photon", fontsize=20)
plt.xlabel("z (cm)", fontsize=15)
plt.ylabel("Dose ($MeV.cm^{2}.g^{-1}$)", fontsize=15)
#plt.legend(loc=1, prop={'size': 12})
plt.legend()
plt.show()

plt.figure(figsize=(15,8))
for i in range(len(data)):
    plt.scatter(energy, z_max, label=data[i].get_name(), color='navy')
plt.title("Distance de mise à l'équilibre électronique", fontsize=20)
plt.xlabel("Energie (eV)", fontsize=15)
plt.ylabel("$z_{max} (cm)$", fontsize=15)
plt.xscale('log')
plt.show()

plt.figure(figsize=(15,8))
for i in range(len(data)):
    plt.errorbar(data[i].theta, data[i].pdf_theta_elec, yerr=data[i].pdf_theta_elec_err, label='%s'%(data[i].get_name()))
plt.title('Distribution angulaire des électrons', fontsize=15)
plt.xlabel('$\Theta$ (degré)', fontsize=15)
plt.ylabel('PDF ($sr^{-1}.particle^{-1}$)', fontsize=15)
plt.xscale('log')
plt.legend()

plt.figure(figsize=(15,8))
for i in range(len(data)):
    plt.errorbar(data[i].energy_tr, data[i].pdf_tr, yerr=data[i].pdf_tr_err, label='%s'%(data[i].get_name()))
plt.title('Distribution en énergie des électrons transmis', fontsize=15)
plt.xlabel('E (MeV)', fontsize=15)
plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
plt.xscale('log')
plt.legend()

plt.figure(figsize=(15,8))
for i in range(len(data)):
    plt.errorbar(data[i].energy_bck, data[i].pdf_bck, yerr=data[i].pdf_bck_err, label='%s'%(data[i].get_name()))
plt.title('Distribution en énergie des électrons rétrodiffusés', fontsize=15)
plt.xlabel('E (MeV)', fontsize=15)
plt.ylabel('PDF ($eV^{-1}.particle^{-1}$)', fontsize=15)
plt.xscale('log')
plt.legend()

########################################################################################
# Comparaison dans plusieurs matériaux 
########################################################################################


data_comp = []

data_comp.append(func.Data('1_MeV_air', 1e6, '1 MeV', milieu='Air'))
data_comp.append(func.Data('1_MeV_water', 1e6, '1 MeV', milieu='Water'))

plt.figure(figsize=(15,8))
for i in range(len(data_comp)):
    plt.plot(data_comp[i].get_z(), data_comp[i].get_dose(), label='%s' %(data_comp[i].get_milieu()))
plt.title("Rendement en profondeur pour un faisceau de photon", fontsize=20)
plt.xlabel("z (cm)", fontsize=15)
plt.ylabel("Dose ($MeV.cm^{2}.g^{-1}$)", fontsize=15)
#plt.legend(loc=1, prop={'size': 12})
plt.legend()
plt.show()











##################################################################################
# Test
##################################################################################


"""
data_test = []
data_test.append(func2.Data('1_MeV_water', 1e6, '1 MeV', milieu='Air'))

plt.figure(figsize=(15,8))
plt.plot(data_test[0].get_z(), data_test[0].get_dose(), label='%s' %(data_test[0].get_name()))
"""

"""

f = open('pencyl-res.dat', 'r')
test = f.read()
lines = test.splitlines()


trash, trash, trash, trash, particles = lines[14].split() 
"""
































duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)