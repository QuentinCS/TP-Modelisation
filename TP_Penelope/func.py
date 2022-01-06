#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 09:20:31 2021

@author: quentin
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import sys


# Classe pour utilisation et analyse des données à partir des fichier .dat de penelope
# profil de dose, carte de dose, distributions angulaire, ...

# 2 milieux possibles :
#   - Cuve à eau avec 5 cylindres et NZ = 100 bin, NR = 100 bin => 'cuve'
#   - Fantôme anthropomorphique avec 10 cylindres, voir définitions des cartes de dose => 'fantome'

class Data:
    def __init__(self, file_dose, energy, energy_name, particle=None, milieu=None):
        
        # Vérification que le fantôme soit correct 
        if milieu!= 'cuve' and milieu!= 'fantome':
            print('Erreur: milieu inconnu')
            sys.exit() 
        
        # Variables
        self.file_dose = file_dose
        self.energy = energy
        self.energy_name = energy_name
        self.particle = particle
        self.milieu = milieu
        self.dose_max = 0
        self.z_max = 0

        # Initialisation et tri des données
        f = open(self.file_dose + '/pencyl-res.dat', 'r')
        self.res = f.read()
        f.closed
        result = self.res.splitlines()
        self.trash, self.trash, self.trash, self.time, self.trash = result[10].split(
        )
        self.trash, self.trash, self.trash, self.phi, self.trash = result[11].split(
        )
        self.trash, self.trash, self.trash, self.trash, self.Nb_particles = result[14].split(
        )
        
        # Récupération des caractéristiques de la source: taille et divergence
        f = open(self.file_dose + '/pencyl.dat', 'r')
        self.res = f.read()
        f.closed
        result = self.res.splitlines()
        if milieu=='cuve':
            self.trash, self.trash, self.trash, self.taille_source, self.trash = result[50].split()
            self.trash, self.trash, self.trash, self.trash, self.divergence, self.trash = result[58].split()
            self.divergence = float(self.divergence)
        if milieu=='fantome':
            self.trash, self.trash, self.trash, self.taille_source, self.trash = result[75].split()
            self.trash, self.trash, self.trash, self.trash, self.divergence, self.trash = result[83].split()
            self.divergence = float(self.divergence)

        self.taille_source = float(self.taille_source)


        # Récupération du rendement en profondeur de dose
        f = open(self.file_dose + '/depth-dose.dat', 'r')
        self.data = f.read()
        f.closed
        self.line = self.data.splitlines()
        for i in range(9):
            del self.line[0]
        self.z = np.zeros(len(self.line))
        self.dose = np.zeros(len(self.line))
        self.dose_phi = np.zeros(len(self.line))
        self.dose_err = np.zeros(len(self.line))
        self.dose_phi_err = np.zeros(len(self.line))
        self.trash = np.zeros(len(self.line))
        for i in range(len(self.line)):
            self.z[i], self.dose_phi[i], self.dose_phi_err[i], self.trash[i] = self.line[i].split()
            if (self.dose_phi[i] >= self.dose_max):
                self.dose_max = self.dose_phi[i]
                self.z_max = self.z[i]
        self.dose_max = max(self.dose_phi)

        # Prise en compte de la divergence pour faire la conversion
        if self.divergence == 0:
            self.surface_source =self.taille_source*self.taille_source*np.pi
        else:
            self.surface_source = np.zeros(len(self.z))
            for i in range(len(self.z)):
                self.surface_source[i] = np.pi*pow((100+self.z[i])*np.tan(float(self.divergence)*np.pi/180), 2)
        # Conversion de la dose
        if self.divergence == 0:
            for i in range(len(self.z)):
                self.dose[i] = self.dose_phi[i]*(1.6*pow(10, -19)*1e3) * \
                    (float(self.Nb_particles))*(1/self.surface_source)
                self.dose_err[i] = self.dose_phi_err[i]*(1.6*pow(10, -19)*1e3) * \
                        (float(self.Nb_particles))*(1/self.surface_source)
        else:
            for i in range(len(self.z)):
                self.dose[i] = self.dose_phi[i]*(1.6*pow(10, -19)*1e3) * \
                    (float(self.Nb_particles))*(1/self.surface_source[i])
                self.dose_err[i] = self.dose_phi_err[i]*(1.6*pow(10, -19)*1e3) * \
                    (float(self.Nb_particles))*(1/self.surface_source[i])
        
        self.dose_norm_e = np.zeros(len(self.z))
        for i in range(len(self.z)):
            self.dose_norm_e[i] = self.dose[i]/self.dose[0]

        # Récupération des angles d'émission des électrons
        f = open(self.file_dose + '/polar-angle.dat', 'r')
        self.res_angle = f.read()
        f.closed
        self.angle = self.res_angle.splitlines()
        for i in range(7):
            del self.angle[0]
        self.theta = np.zeros(len(self.angle))
        self.pdf_theta_elec = np.zeros(len(self.angle))
        self.pdf_theta_elec_err = np.zeros(len(self.angle))
        self.pdf_theta_pos = np.zeros(len(self.angle))
        self.pdf_theta_pos_err = np.zeros(len(self.angle))
        for i in range(len(self.angle)):
            self.theta[i], self.pdf_theta_elec[i], self.pdf_theta_elec_err[i], self.pdf_theta_pos[i], self.pdf_theta_pos_err[i], self.trash[i], self.trash[i] = self.angle[i].split()
            # self.pdf_theta_elec[i] = self.pdf_theta_elec[i] * float(self.Nb_particles) # à vérifier ?

        # Récupération des distributions en énergie des électrons transmis
        f = open(self.file_dose + '/energy-up.dat', 'r')
        self.dist_up = f.read()
        f.closed
        self.tr_elec = self.dist_up.splitlines()
        for i in range(7):
            del self.tr_elec[0]
        self.energy_tr = np.zeros(len(self.tr_elec))  # en eV
        self.pdf_tr = np.zeros(len(self.tr_elec))
        self.pdf_tr_err = np.zeros(len(self.tr_elec))
        for i in range(len(self.tr_elec)):
            self.energy_tr[i], self.pdf_tr[i], self.pdf_tr_err[i], self.trash[
                i], self.trash[i], self.trash[i], self.trash[i] = self.tr_elec[i].split()
        self.energy_tr *= 1e-6  # conversion Energy en MeV
        # self.pdf_tr *= float(self.Nb_particles)     # Je suis pas sur de la conversion ...
        # self.pdf_tr_err *= float(self.Nb_particles) # Je suis pas sur de la conversion ...

        # Récupération des distributions en énergie des électrons rétrodiffusé
        f = open(self.file_dose + '/energy-down.dat', 'r')
        self.dist_down = f.read()
        f.closed
        self.bck_elec = self.dist_down.splitlines()
        for i in range(7):
            del self.bck_elec[0]
        self.energy_bck = np.zeros(len(self.bck_elec))  # en eV
        self.pdf_bck = np.zeros(len(self.bck_elec))
        self.pdf_bck_err = np.zeros(len(self.bck_elec))
        for i in range(len(self.bck_elec)):
            self.energy_bck[i], self.pdf_bck[i], self.pdf_bck_err[i], self.trash[
                i], self.trash[i], self.trash[i], self.trash[i] = self.bck_elec[i].split()
        self.energy_bck *= 1e-6  # conversion Energy en MeV



        # Obtention de la carte de dose en 2D dans la cas d'une cuve (à eau ou autre)
        # avec 5 cylindres de 50cm de rayon et 20cm de haut 
        if milieu=='cuve':
            
            self.line = []
            self.nK = 5  # Nombre de couches dans le fantôme
            self.Z_bin = 100  # Nombre de bin en profondeur par couches
            self.R_bin = 100  # Nombre de bin de rayon
            self.taille = 10100   # Nombre de lignes dans le fichier (en lien direct avec le nombre de bin)
            self.dose2d_cuve = np.zeros((self.nK, self.R_bin, self.Z_bin)) # Carte de dose
            self.r_scale = []   # Echelle selon le rayon de la cuve
            self.z_scale = []   # Echelle en profondeur de la cuve 
            
            # Boucle de récupération des données à partir des fichiers pour chaques couches dans la cuve
            for kc in range(self.nK):

                file = self.file_dose + '/dose-charge-0' + str(kc+1) +'.dat'
                f = open(file, 'r')
                data = f.read()
                f.closed
                self.line.append(data.splitlines())
                for i in range(6):
                    del self.line[kc][0]
                self.rayon = np.zeros(len(self.line[kc]))
                self.profondeur_z = np.zeros(len(self.line[kc]))
                self.dose_1 = np.zeros(len(self.line[kc]))
                self.dose_1_err = np.zeros(len(self.line[kc]))
                trash = np.zeros(len(self.line[kc]))
                trash2 = np.zeros(len(self.line[kc]))
                k = 0
                j = 0 
                for i in range(len(self.line[kc])):
                    if len(self.line[kc][i]) > 10:
                        self.rayon[i], self.profondeur_z[i], self.dose_1[i], self.dose_1_err[i], trash[i], trash2[i] = self.line[kc][i].split()
                        self.dose2d_cuve[kc][k][j] = self.dose_1[i]
                        j += 1
                    else:
                        k += 1
                        j = 0

                # Récupération des échelles en r et en z                 
                if kc == 0:
                        self.z_scale.append(min(self.profondeur_z))
                        self.r_scale.append(-max(self.rayon))
                        self.r_scale.append(max(self.rayon))
                if kc == (self.nK-1):
                        self.z_scale.append(max(self.profondeur_z))

            # Combinaison des cartes de dose 
            self.Dose2d = self.dose2d_cuve[0]
            for kc in range(1, self.nK):
                self.Dose2d = np.concatenate((self.Dose2d, self.dose2d_cuve[kc]), axis=1)

            # Symétrie cylindrique de la carte de dose 
            self.Dose2D = matrice_revolution(self.Dose2d, self.R_bin)



        # Obtention de la carte de dose en 2D dans le cas d'un fantôme anthropomorphique
        # récupération de la carte de dose avec 10 couches (il manque la couche de tissus en 
        # sortie du fantôme)
        if milieu=='fantome':
            
            self.line = []
            self.nK = 10  # Nombre de couches dans le fantôme
            self.taille = 10100   # Nombre de lignes dans le fichier (en lien direct avec le nombre de bin)
            self.r_scale = []   # Echelle selon le rayon de la cuve
            self.z_scale = []   # Echelle en profondeur de la cuve 
            
            # Définitions des cartes de dose avec les bonnes dimensions
            self.dose2d_cuve_1 = np.zeros((150, 8)) # Carte de dose couche 1
            self.dose2d_cuve_2 = np.zeros((30, 16)) # Carte de dose couche 2
            self.dose2d_cuve_3 = np.zeros((60, 16)) # Carte de dose couche 3
            self.dose2d_cuve_4 = np.zeros((60, 16)) # Carte de dose couche 4
            self.dose2d_coeur = np.zeros((60, 80)) # Carte de dose couche coeur
            self.dose2d_cuve_5 = np.zeros((90, 80)) # Carte de dose couche 5
            self.dose2d_cuve_6 = np.zeros((150, 192)) # Carte de dose 6
            self.dose2d_cuve_7 = np.zeros((30, 16)) # Carte de dose 7
            self.dose2d_cuve_8 = np.zeros((60, 16)) # Carte de dose 8 
            self.dose2d_cuve_9 = np.zeros((60, 16)) # Carte de dose 9
            
            # Boucle de récupération des données à partir des fichiers pour chaques couches dans la cuve
            for kc in range(self.nK):
                if kc == 9:
                    file = self.file_dose + '/dose-charge-' + str(kc+1) +'.dat'
                else:
                    file = self.file_dose + '/dose-charge-0' + str(kc+1) +'.dat'
                f = open(file, 'r')
                data = f.read()
                f.closed
                self.line.append(data.splitlines())
                for i in range(6):
                    del self.line[kc][0]

                self.rayon = np.zeros(len(self.line[kc]))
                self.profondeur_z = np.zeros(len(self.line[kc]))
                self.dose_1 = np.zeros(len(self.line[kc]))
                self.dose_1_err = np.zeros(len(self.line[kc]))
                trash = np.zeros(len(self.line[kc]))
                trash2 = np.zeros(len(self.line[kc]))
                k = 0
                j = 0 
                for i in range(len(self.line[kc])):
                    if len(self.line[kc][i]) > 10:
                        self.rayon[i], self.profondeur_z[i], self.dose_1[i], self.dose_1_err[i], trash[i], trash2[i] = self.line[kc][i].split()
                        if self.divergence == 0:
                            self.dose_1[i] *= (1.6*pow(10, -19)*1e3)*(float(self.Nb_particles))*(1/self.surface_source)
                        else:
                            self.dose_1[i] *= (1.6*pow(10, -19)*1e3)*(float(self.Nb_particles))*(1/(np.pi*pow((100+self.profondeur_z[i])*np.tan(float(self.divergence)*np.pi/180), 2)))
                        if kc == 0:
                            self.dose2d_cuve_1[k][j] = self.dose_1[i]
                        if kc == 1:
                            self.dose2d_cuve_2[k][j] = self.dose_1[i]
                        if kc == 2:
                            self.dose2d_cuve_3[k][j] = self.dose_1[i]
                        if kc == 3:
                            self.dose2d_cuve_4[k][j] = self.dose_1[i]
                        if kc == 4:
                            self.dose2d_coeur[k][j] = self.dose_1[i]
                        if kc == 5:
                            self.dose2d_cuve_5[k][j] = self.dose_1[i]
                        if kc == 6:
                            self.dose2d_cuve_6[k][j] = self.dose_1[i]
                        if kc == 7:
                            self.dose2d_cuve_7[k][j] = self.dose_1[i]
                        if kc == 8:
                            self.dose2d_cuve_8[k][j] = self.dose_1[i]
                        if kc == 9:
                            self.dose2d_cuve_9[k][j] = self.dose_1[i]
        
                        j += 1
                    else:
                        k += 1
                        j = 0

                # Récupération des échelles en r et en z                 
                if kc == 0:
                        self.z_scale.append(min(self.profondeur_z))
                        self.r_scale.append(-max(self.rayon))
                        self.r_scale.append(max(self.rayon))
                if kc == (self.nK-1):
                        self.z_scale.append(max(self.profondeur_z))
 
            # Combinaison des cartes de dose 
            self.layer2 = np.concatenate((self.dose2d_cuve_2, self.dose2d_cuve_3, self.dose2d_cuve_4), axis=0)
            self.layer3 = np.concatenate((self.dose2d_coeur, self.dose2d_cuve_5), axis=0)
            self.layer5 = np.concatenate((self.dose2d_cuve_7, self.dose2d_cuve_8, self.dose2d_cuve_9), axis=0)
            self.Dose2D = np.concatenate((self.dose2d_cuve_1, self.layer2, self.layer3, self.dose2d_cuve_6, self.layer5), axis=1)
            
            # Révolution cylindrique
            self.Dose2D = matrice_revolution(self.Dose2D, 150)


    # Fonctions
    def get_name(self):
        return self.energy_name

    def get_milieu(self):
        return self.milieu

    def get_faisceau(self):
        if self.divergence == None:
            return 'Parralèle'
        else:
            return 'Divergent'

    def get_energy(self):
        return self.energy

    def get_dose(self):
        return self.dose

    def get_dose_err(self):
        return self.dose_err

    def get_z(self):
        return self.z
    
    def get_time(self):
        return float(self.time)

    def get_zmax(self):
        return self.z_max

    def get_dosemax(self):
        return self.dose_max

    def affiche(self):
        print("Nom:", self.energy_name)
        print("Dose maxe:", self.dose_max, "eV.cm^{2}.g^{-1}")
        print("z max:", self.z_max, "cm")

    def plot(self):
        plt.figure(figsize=(15, 8))
        plt.plot(self.z, self.dose, label='%s' % (self.energy_name))
        plt.xlabel("z (cm)")
        plt.ylabel("Dose $eV.cm^{2}.g^{-1}$")
        plt.legend(loc=1, prop={'size': 16})
    
    def get_dose_moyenne_coeur(self):
        return np.mean(self.dose2d_coeur)

    def get_dose_max_coeur(self):
        return self.dose2d_coeur.max()
    
    def get_dose_moyenne(self):
        return np.mean(self.Dose2D)

    def get_dose_max(self):
        return self.Dose2D.max()
    
    def get_dose_peau(self):
        return self.Dose2D[int(len(self.Dose2D[0])/2)][0]

###################################################################################
# Fonctions hors classe 
###################################################################################

#Fonction de symétrie de matrice selon l'axe x, pour révolution cylindrique 
def matrice_revolution(matrice, n_bin):
    
    matrice_miroir = np.zeros((2*matrice.shape[0], matrice.shape[1]))
    for i in range(matrice.shape[0]):
        for j in range(matrice.shape[1]): 
            matrice_miroir[i,j] = matrice[(n_bin-1)-i,j]
    for i in range(matrice.shape[0], matrice_miroir.shape[0]):
        for j in range(0, matrice.shape[1]):
            matrice_miroir[i,j] = matrice[i-matrice.shape[0],j-matrice.shape[1]]
                
    return matrice_miroir

# Interpolation quadratique 
def Interp (energy, mu, E_i):
    #inter_mu = interpolate.interp1d(energy, mu, kind='quadratic') # interpolation quadratique 
    inter_mu = interpolate.interp1d(energy, mu, kind='slinear') # interpolation linéaire

    mu_int = np.zeros(4)

    for i in range(0, 4):    
        mu_int[i] = inter_mu(E_i[i])

    return mu_int


# Fonction création du fantôme anthropomorphique pour les calculs analytiques
def matrice(mu_soft, mu_lung, mu_bone):
    
    Matrice = np.zeros((75, 200))
    
    for y in range(0, 75):
        for x in range(0, 200):   
            if y <= 15:    
                if x <= 5 or x >= 195 :
                    Matrice[y][x] = mu_soft
                if (5<x and x<=15) or ( 185<x and x<=195):
                    Matrice[y][x] = mu_bone
                if (15< x and x<=185):
                    Matrice[y][x] = mu_lung
                
            if  15 < y and y <= 30:
                if x <=15 or x >= 185 :
                    Matrice[y][x] = mu_soft
                if 15<=x and x<=185:
                    Matrice[y][x] = mu_lung

            if 30 < y and y <= 36 :
                if x <= 5 or x >= 195:
                    Matrice[y][x] = mu_soft
                if (5<x and x<=15) or (185<x and x<=195):
                    Matrice[y][x] = mu_bone
                if 15<x and x<=185:
                    Matrice[y][x] = mu_lung
                 
            if 36 < y and y <= 45 :
                if (x <= 5 or x >= 195) or (15<=x and x<65):
                    Matrice[y][x] = mu_soft
                if (5<x and x<=15) or (185<x and x<=195): 
                    Matrice[y][x] = mu_bone
                if 65<=x and x<=185:
                    Matrice[y][x] = mu_lung
                
            if 45 < y and y <= 60 :
                if (x <= 15 or x >= 185) or ( 15<x and x<=65):
                    Matrice[y][x] = mu_soft
                if 65<=x and x<=185:
                    Matrice[y][x] = mu_lung

            if 60 < y and y <= 66:
                if (x<=5 or x>=195) or ( 15<=x and x<=65):
                    Matrice[y][x] = mu_soft
                if (5<x and x<=15) or (185<x and x<=195):
                    Matrice[y][x] = mu_bone
                if 65<=x and x<=185:
                    Matrice[y][x] = mu_lung 

            if y > 66:
                if x <= 5 or x >= 195 :
                    Matrice[y][x] = mu_soft
                if (5<x and x<=15) or ( 185<x and x<=195):
                    Matrice[y][x] = mu_bone
                if 15<x and x<=185:
                    Matrice[y][x] = mu_lung
                
    return Matrice

def func_fit(x, k, a):
    y = k*pow(x, a)
    #y = k*(np.log(a*x)) 
    return y
    
