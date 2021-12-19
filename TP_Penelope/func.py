#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 09:20:31 2021

@author: quentin
"""

import numpy as np
import matplotlib.pyplot as plt


# Classe pour utilisation et analyse des données à partir des fichier .dat de penelope
class Data:
    def __init__(self, file_dose, energy, energy_name, particle=None, milieu=None, divergence=None):

        # Variables
        self.file_dose = file_dose
        self.energy = energy
        self.energy_name = energy_name
        self.particle = particle
        self.milieu = milieu
        self.divergence = divergence
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

        # Récupération du rendement en profondeur de dose
        f = open(self.file_dose + '/depth-dose.dat', 'r')
        self.data = f.read()
        f.closed
        self.line = self.data.splitlines()
        for i in range(9):
            del self.line[0]
        self.z = np.zeros(len(self.line))
        self.dose = np.zeros(len(self.line))
        self.dose_err = np.zeros(len(self.line))
        self.trash = np.zeros(len(self.line))
        for i in range(len(self.line)):
            self.z[i], self.dose[i], self.dose_err[i], self.trash[i] = self.line[i].split()
            if (self.dose[i] >= self.dose_max):
                self.dose_max = self.dose[i]
                self.z_max = self.z[i]
        self.dose_max = max(self.dose)

        # Prise en compte de la divergence pour faire la conversion
        if self.divergence == None:
            self.surface_source = 5.64*5.64*np.pi
        else:
            self.surface_source = np.zeros(len(self.z))
            for i in range(len(self.z)):
                self.surface_source[i] = np.pi * \
                    pow((100+self.z[i])*np.tan(self.divergence*np.pi/180), 2)
        # Conversion de la dose
        if self.divergence == None:
            self.dose *= (1.6*pow(10, -19)*1e3) * \
                (float(self.Nb_particles))*(1/self.surface_source)
            self.dose_err *= (1.6*pow(10, -19)*1e3) * \
                (float(self.Nb_particles))*(1/self.surface_source)
        else:
            for i in range(len(self.z)):
                self.dose[i] *= (1.6*pow(10, -19)*1e3) * \
                    (float(self.Nb_particles))*(1/self.surface_source[i])
                self.dose_err[i] *= (1.6*pow(10, -19)*1e3) * \
                    (float(self.Nb_particles))*(1/self.surface_source[i])

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
        for i in range(len(self.angle)):
            self.theta[i], self.pdf_theta_elec[i], self.pdf_theta_elec_err[i], self.trash[
                i], self.trash[i], self.trash[i], self.trash[i] = self.angle[i].split()
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
        if milieu=='cuve':
            
            self.line = []
            self.nK = 5  # Nombre de couches dans le fantôme
            self.Z_bin = 100  # Nombre de bin en profondeur par couches
            self.R_bin = 100  # Nombre de bin de rayon
            self.taille = 10100   # Nombre de lignes dans le fichier (en lien direct avec le nombre de bin)
            self.dose2d_cuve = np.zeros((self.nK, self.R_bin, self.Z_bin)) # Carte de dose
            self.r_scale = [0, 100]   # Echelle selon le rayon de la cuve
            self.z_scale = [0, 100]   # Echelle en profondeur de la cuve 
            
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
                        self.r_scale.append(min(self.rayon))
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
        if milieu=='fantome':
            
            self.line = []
            self.nK = 10  # Nombre de couches dans le fantôme
            self.taille = 10100   # Nombre de lignes dans le fichier (en lien direct avec le nombre de bin)
            self.r_scale = [0, 5]   # Echelle selon le rayon de la cuve
            self.z_scale = [0, 20]   # Echelle en profondeur de la cuve 
            
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
                    
                if kc == 0:
                    self.Z_bin = 8
                    self.R_bin = 150
                    self.dose2d_cuve_1 = np.zeros((self.R_bin, self.Z_bin)) # Carte de dose
                if kc == 1:
                    self.Z_bin = 16
                    self.R_bin = 30
                    self.dose2d_cuve_2 = np.zeros((self.R_bin, self.Z_bin)) # Carte de dose
                if kc == 2 or kc == 3:
                    self.Z_bin = 16
                    self.R_bin = 60
                    self.dose2d_cuve_3 = np.zeros((2, self.R_bin, self.Z_bin)) # Carte de dose
                if kc == 4:
                    self.Z_bin = 80
                    self.R_bin = 60
                    self.dose2d_cuve_4 = np.zeros((self.R_bin, self.Z_bin)) # Carte de dose
                if kc == 5:
                    self.Z_bin = 80
                    self.R_bin = 90
                    self.dose2d_cuve_5 = np.zeros((self.R_bin, self.Z_bin)) # Carte de dose
                if kc == 6:
                    self.Z_bin = 192
                    self.R_bin = 150
                    self.dose2d_cuve_6 = np.zeros((self.R_bin, self.Z_bin)) # Carte de dose
                if kc == 7:
                    self.Z_bin = 16
                    self.R_bin = 30
                    self.dose2d_cuve_7 = np.zeros((self.R_bin, self.Z_bin)) # Carte de dose
                if kc == 7 or kc == 8 or kc == 9:
                    self.Z_bin = 16
                    self.R_bin = 60
                    self.dose2d_cuve_8 = np.zeros((2, self.R_bin, self.Z_bin)) # Carte de dose
                    
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
                        
                        if kc == 0:
                            self.dose2d_cuve_1[k][j] = self.dose_1[i]
                        if kc == 1:
                            self.dose2d_cuve_2[k][j] = self.dose_1[i]
                        if kc == 2 or kc == 3:
                            self.dose2d_cuve_3[kc-2][k][j] = self.dose_1[i]
                        if kc == 4:
                            self.dose2d_cuve_4[k][j] = self.dose_1[i]
                        if kc == 5:
                            self.dose2d_cuve_5[k][j] = self.dose_1[i]
                        if kc == 6:
                            self.dose2d_cuve_6[k][j] = self.dose_1[i]
                        if kc == 7:
                            self.dose2d_cuve_7[k][j] = self.dose_1[i]
                        if kc == 8 or kc == 9:
                            self.dose2d_cuve_8[kc-8][k][j] = self.dose_1[i]
        
                        j += 1
                    else:
                        k += 1
                        j = 0

                # Récupération des échelles en r et en z                 
                if kc == 0:
                        self.z_scale.append(min(self.profondeur_z))
                        self.r_scale.append(min(self.rayon))
                        self.r_scale.append(max(self.rayon))
                if kc == (self.nK-1):
                        self.z_scale.append(max(self.profondeur_z))

            # Combinaison des cartes de dose 
            self.layer2 = np.concatenate((self.dose2d_cuve_2, self.dose2d_cuve_3[0], self.dose2d_cuve_3[1]), axis=0)
            self.layer3 = np.concatenate((self.dose2d_cuve_4, self.dose2d_cuve_5), axis=0)
            self.layer5 = np.concatenate((self.dose2d_cuve_7, self.dose2d_cuve_8[0], self.dose2d_cuve_8[1]), axis=0)
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

###################################################################################
# Fonctions hors classe 
###################################################################################

def matrice_revolution(matrice, n_bin):
    
    matrice_miroir = np.zeros((2*matrice.shape[0], matrice.shape[1]))
    for i in range(matrice.shape[0]):
        for j in range(matrice.shape[1]): 
            matrice_miroir[i,j] = matrice[(n_bin-1)-i,j]
    for i in range(matrice.shape[0], matrice_miroir.shape[0]):
        for j in range(0, matrice.shape[1]):
            matrice_miroir[i,j] = matrice[i-matrice.shape[0],j-matrice.shape[1]]
                
    return matrice_miroir



