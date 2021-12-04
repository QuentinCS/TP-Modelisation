#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 12:06:40 2021
@author: quentin
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from random import uniform
import time
import func
    
start_time = time.time()

# Extraction des données
Data = pd.read_excel('eau.xlsx', sheet_name="Feuil1")
Energy = Data['Energy (MeV)'].values
Att = Data['µ/ρ (cm2/g)'].values
En = Data['µen/ρ (cm2/g)'].values

# Interpolation aux valueurs d'énergies d'intérêt
E_int = np.array([0.017, 0.064, 0.1, 10])
E_int_name = np.array(["17 keV", "64 keV", "100 keV", "10 MeV"])
muatt_int = np.interp(E_int, Energy, Att) 
muen_int = np.interp(E_int, Energy, En)

print(muatt_int)

#####################################################################################
# Calcul de la distance d'interaction par la méthode de la fonction de répartition
#####################################################################################
t1 = time.time()

print("Calcul avec la méthode d'inversion de la fonction de répartition\n------------------------------------")
Nb = 100000

distance_int = np.zeros((4, Nb))
R = np.zeros((4, Nb))
rho_eau = 1

t1 = time.time()
for energy in range(0, 4):
    for i in range(Nb):
        R[energy][i] = uniform(0, 1)
        distance_int[energy][i] = -(rho_eau/muatt_int[energy]) * np.log(R[energy][i]) 
t1f = time.time()

data1 = func.Set_data(energy=0.017, energy_name='17 keV')
data1.set_distance_int(distance_int[0])
data1.fit()
data2 = func.Set_data(energy=0.064, energy_name='64 keV')
data2.set_distance_int(distance_int[1])
data2.fit()
data3 = func.Set_data(energy=0.1, energy_name='100 keV')
data3.set_distance_int(distance_int[2])
data3.fit()
data4 = func.Set_data(energy=10, energy_name='10 MeV')
data4.set_distance_int(distance_int[3])
data4.fit()

plt.figure(figsize=(20, 14))
plt.subplot(2, 2, 1)
plt.suptitle("Distance d'interaction dans la cuve à \n eau à différentes énergies pour la méthode par inversion de la fonction de répartition", fontsize=20)
data1.plot()
plt.subplot(2, 2, 2)  
data2.plot()
plt.subplot(2, 2, 3)  
data3.plot()
plt.subplot(2, 2, 4)  
data4.plot()
plt.show()

print("Ecart valeur réelle: ", 100*abs(muatt_int[0]-data1.get_mu())/muatt_int[0], "%")
print("Ecart valeur réelle: ", 100*abs(muatt_int[1]-data2.get_mu())/muatt_int[1], "%")
print("Ecart valeur réelle: ", 100*abs(muatt_int[2]-data3.get_mu())/muatt_int[2], "%")
print("Ecart valeur réelle: ", 100*abs(muatt_int[3]-data4.get_mu())/muatt_int[3], "%")
print ('\n \nTemps de calcul : %5.3g s \n \n' % (t1f - t1))

#################################################################################
# Calcul de la distance d'interaction par la méthode élémentaire
#################################################################################

print("Calcul avec la méthode élémentaire\n------------------------------------")

Nb = 1000
distance_int_1 = np.zeros((4, Nb))
Nb_calcul = np.zeros((4, Nb))
R_1 = np.zeros((4, Nb))
rho_eau = 1
dx = 1
step = 0.01  # en cm

t2 = time.time()
for energy in range(0, 4):
    for i in range(Nb):
         interaction = False
         dx = 0
         while (interaction == False):
             R_1 = uniform(0, 1)
             dx += step
             Nb_calcul[energy][i] += 1
             #print(dx)
             if (R_1 <= muatt_int[energy]*step):
                 distance_int_1[energy][i] = dx

                 interaction = True
t2f = time.time()        

data_1 = func.Set_data(energy=0.017, energy_name='17 keV')
data_1.set_distance_int(distance_int_1[0])
data_1.fit()
data_2 = func.Set_data(energy=0.064, energy_name='64 keV')
data_2.set_distance_int(distance_int_1[1])
data_2.fit()
data_3 = func.Set_data(energy=0.1, energy_name='100 keV')
data_3.set_distance_int(distance_int_1[2])
data_3.fit()
data_4 = func.Set_data(energy=10, energy_name='10 MeV')
data_4.set_distance_int(distance_int_1[3])
data_4.fit()

plt.figure(figsize=(20, 14))
plt.subplot(2, 2, 1)
plt.suptitle("Distance d'interaction dans la cuve à \n eau à différentes énergies pour la méthode élémentaire", fontsize=20)
data_1.plot()
plt.subplot(2, 2, 2)  
data_2.plot()
plt.subplot(2, 2, 3)  
data_3.plot()
plt.subplot(2, 2, 4)  
data_4.plot()
plt.show()

plt.figure(figsize=(20, 14))
plt.subplot(2, 2, 1)
plt.suptitle("Nombre de calcul/pas par photons", fontsize=20)
plt.hist(Nb_calcul[0], bins=int(np.sqrt(Nb)), label="%s\nmean = %4.1f"%(E_int_name[0], Nb_calcul[0].mean()))
plt.xlabel("Nb de pas (-)")
plt.ylabel("Nb d'occurence")
plt.legend()
plt.subplot(2, 2, 2)  
plt.hist(Nb_calcul[1], bins=int(np.sqrt(Nb)), label="%s\nmean = %4.1f"%(E_int_name[1], Nb_calcul[1].mean()))
plt.xlabel("Nb de pas (-)")
plt.ylabel("Nb d'occurence")
plt.legend()
plt.subplot(2, 2, 3)  
plt.hist(Nb_calcul[2], bins=int(np.sqrt(Nb)), label="%s\nmean = %4.1f"%(E_int_name[2], Nb_calcul[2].mean()))
plt.xlabel("Nb de pas (-)")
plt.ylabel("Nb d'occurence")
plt.legend()
plt.subplot(2, 2, 4)  
plt.hist(Nb_calcul[3], bins=int(np.sqrt(Nb)), label="%s\nmean = %4.1f"%(E_int_name[3], Nb_calcul[3].mean()))
plt.xlabel("Nb de pas (-)")
plt.ylabel("Nb d'occurence")
plt.legend()
plt.show()


print("Nombre de calcul moyen par photons %4.3f +- %4.3f"%(Nb_calcul[0].mean(), Nb_calcul[0].std()))

print("Ecart valeur réelle: ", 100*abs(muatt_int[0]-data_1.get_mu())/muatt_int[0], "%")
print("Ecart valeur réelle: ", 100*abs(muatt_int[1]-data_2.get_mu())/muatt_int[1], "%")
print("Ecart valeur réelle: ", 100*abs(muatt_int[2]-data_3.get_mu())/muatt_int[2], "%")
print("Ecart valeur réelle: ", 100*abs(muatt_int[3]-data_4.get_mu())/muatt_int[3], "%")

print('\n \nTemps de calcul méthode par inversion de la fonction de répartition: %5.3g s' % (t1f - t1))
print('Temps de calcul méthode élémentaire : %5.3g s' % (t2f - t2))
print("Rapport des temps de calcul: %4.3d"%((t2f - t2)/(t1f - t1)))

#################################################################################
# Détermination du type d'interaction 
#################################################################################

Nb = 100000
mu_rho_Rayleigh = [0.1134, 0.01236, 0.005338, 0.000000561]
mu_rho_photo_elec = [0.9144, 0.01206, 0.002762, 0.0000001386]
mu_rho_compton = [0.1733, 0.1752, 0.1625, 0.01704]
mu_rho_pair = [0, 0, 0, 0.004699]
mu_rho_tot = [mu_rho_Rayleigh[i] + mu_rho_compton[i] + mu_rho_pair[i] + mu_rho_photo_elec[i] for i in range(4)]

Nb_photo = np.zeros(4)
Nb_compton = np.zeros(4)
Nb_paire = np.zeros(4)
Nb_Ray = np.zeros(4)
R_1 = np.zeros(4)


for energy in range(4):
    for i in range(Nb):  
        #R_1[energy] = uniform(0, 1)
        R_2 = uniform(0, 1)
        if (R_2 < mu_rho_Rayleigh[energy]/mu_rho_tot[energy]):
            Nb_Ray[energy] += 1
        if (R_2 > mu_rho_Rayleigh[energy]/mu_rho_tot[energy] and R_2 < (mu_rho_Rayleigh[energy]+mu_rho_photo_elec[energy])/mu_rho_tot[energy]):
            Nb_photo[energy] += 1
        if (R_2 > (mu_rho_Rayleigh[energy]+mu_rho_photo_elec[energy])/mu_rho_tot[energy] and R_2 < (mu_rho_compton[energy]+mu_rho_photo_elec[energy])/mu_rho_tot[energy]):
            Nb_compton[energy] += 1
        if (R_2 > (mu_rho_compton[energy]+mu_rho_photo_elec[energy]+mu_rho_Rayleigh[energy])/mu_rho_tot[energy] and E_int[energy] > 1.022):
            Nb_paire[energy] += 1

plt.style.use('ggplot')
x = ['Photo électrique', 'Compton', 'Paire', 'Rayleigh']
x_pos = np.arange(len(x))
y1 = [Nb_photo[0], Nb_compton[0], Nb_paire[0], Nb_Ray[0]]
y2 = [Nb_photo[1], Nb_compton[1], Nb_paire[1], Nb_Ray[1]]
y3 = [Nb_photo[2], Nb_compton[2], Nb_paire[2], Nb_Ray[2]]
y4 = [Nb_photo[3], Nb_compton[3], Nb_paire[3], Nb_Ray[3]]

plt.figure(figsize=(20, 16))
plt.subplot(2, 2, 1)
plt.bar(x_pos, y1)
plt.xticks(x_pos, x)
plt.title("17 keV")
plt.ylabel("Nombre d'interactions")
plt.subplot(2, 2, 2)
plt.bar(x_pos, y2)
plt.xticks(x_pos, x)
plt.title("64 keV")
plt.ylabel("Nombre d'interactions")
plt.subplot(2, 2, 3)
plt.bar(x_pos, y3)
plt.xticks(x_pos, x)
plt.title("100 keV")
plt.ylabel("Nombre d'interactions")
plt.subplot(2, 2, 4)
plt.bar(x_pos, y4)
plt.xticks(x_pos, x)
plt.title("10 MeV")
plt.ylabel("Nombre d'interactions")
plt.show()


plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10, 8))
index = np.arange(4)
bar_width = 0.15
opacity = 0.9
ax.bar(index, Nb_Ray/Nb, bar_width, alpha=opacity, color='y', label='Rayleigh')
ax.bar(index+bar_width, Nb_photo/Nb, bar_width, alpha=opacity, color='r', label='Photo-électrique')
ax.bar(index+2*bar_width, Nb_compton/Nb, bar_width, alpha=opacity, color='b', label='Compton')
ax.bar(index+3*bar_width, Nb_paire/Nb, bar_width, alpha=opacity, color='g', label='Paire')
ax.set_title("Type d'interactions")
ax.set_ylabel("Proportion d'interactions")
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(E_int_name)
ax.legend()
plt.show()

duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)