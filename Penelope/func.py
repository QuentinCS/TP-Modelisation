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
    def __init__(self, file_dose, energy, energy_name, particle=None, milieu=None):
         
        # Variables 
        self.file_dose = file_dose
        self.energy = energy
        self.energy_name = energy_name
        self.particle = particle
        self.milieu = milieu
        self.dose_max = 0
        self.z_max = 0
        self.surface_source = 0.0564*0.564*np.pi

        # Initialisation et tri des données 
        f = open(self.file_dose + '/pencyl-res.dat', 'r')
        self.res = f.read()
        f.closed
        result = self.res.splitlines()
        self.trash, self.trash, self.trash, self.time, self.trash = result[10].split()
        self.trash, self.trash, self.trash, self.phi, self.trash = result[11].split()
        self.trash, self.trash, self.trash, self.trash, self.Nb_particles = result[14].split()
        
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
        # Conversion de la dose
        self.dose *= (1e-19*1e3*1e3)*(float(self.Nb_particles))*(1/self.surface_source)
        self.dose_err *= (1e-19*1e3*1e3)*(float(self.Nb_particles))*(1/self.surface_source)
        
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
            self.theta[i], self.pdf_theta_elec[i], self.pdf_theta_elec_err[i], self.trash[i], self.trash[i], self.trash[i], self.trash[i] = self.angle[i].split()
            #self.pdf_theta_elec[i] = self.pdf_theta_elec[i] * float(self.Nb_particles) # à vérifier ?
        
        # Récupération des distributions en énergie des électrons transmis
        f = open(self.file_dose + '/energy-up.dat', 'r')
        self.dist_up = f.read()
        f.closed
        self.tr_elec = self.dist_up.splitlines()
        for i in range(7):
            del self.tr_elec[0]
        self.energy_tr = np.zeros(len(self.tr_elec)) # en eV
        self.pdf_tr = np.zeros(len(self.tr_elec))
        self.pdf_tr_err = np.zeros(len(self.tr_elec))
        for i in range(len(self.tr_elec)):
            self.energy_tr[i], self.pdf_tr[i], self.pdf_tr_err[i], self.trash[i], self.trash[i], self.trash[i], self.trash[i] = self.tr_elec[i].split()
        self.energy_tr *= 1e-6 # conversion Energy en MeV
        #self.pdf_tr *= float(self.Nb_particles)     # Je suis pas sur de la conversion ...
        #self.pdf_tr_err *= float(self.Nb_particles) # Je suis pas sur de la conversion ...


        # Récupération des distributions en énergie des électrons rétrodiffusé
        f = open(self.file_dose + '/energy-down.dat', 'r')
        self.dist_down = f.read()
        f.closed
        self.bck_elec = self.dist_down.splitlines()
        for i in range(7):
            del self.bck_elec[0]
        self.energy_bck = np.zeros(len(self.bck_elec)) # en eV
        self.pdf_bck = np.zeros(len(self.bck_elec))
        self.pdf_bck_err = np.zeros(len(self.bck_elec))
        for i in range(len(self.bck_elec)):
            self.energy_bck[i], self.pdf_bck[i], self.pdf_bck_err[i], self.trash[i], self.trash[i], self.trash[i], self.trash[i] = self.bck_elec[i].split()
        self.energy_bck *= 1e-6 # conversion Energy en MeV
        
        """ ça fonctionne pas ...
        # Récupération de la carte de dose
        f = open(self.file_dose + '/dose-charge-01.dat', 'r')
        self.data1 = f.read()
        f.closed
        self.dose_map = self.data1.splitlines()
        for i in range(6):
            del self.dose_map[0]
        self.radius = np.zeros(len(self.dose_map))
        self.z_position = np.zeros(len(self.dose_map))
        self.dose2D = np.zeros(len(self.dose_map))
        self.dose2D_err = np.zeros(len(self.dose_map))
        self.trash = np.zeros(len(self.dose_map))
        for i in range(len(self.dose_map)):
            self.radius[i], self.z_position[i], self.dose2D[i], self.dose2D_err[i], self.trash[i], self.trash[i] = self.dose_map[i].split()
        """
        
    # Fonctions     
    def get_name(self):
        return self.energy_name
        
    def get_milieu(self):
        return self.milieu
    
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
        print("Dose maxe:", self.dose_max,"eV.cm^{2}.g^{-1}")
        print("z max:", self.z_max, "cm")


    def plot(self):
        plt.figure(figsize=(15, 8))
        plt.plot(self.z, self.dose, label='%s' %(self.energy_name))
        plt.xlabel("z (cm)")
        plt.ylabel("Dose $eV.cm^{2}.g^{-1}$")
        plt.legend(loc=1, prop={'size': 16})