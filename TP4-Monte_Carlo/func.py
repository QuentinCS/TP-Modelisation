#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 11:36:06 2021

@author: quentin
"""

# Fichier de fonction, et de classe

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def fonction(x, A, B):
    return A*np.exp(-B*x)


def Chi2_test(data, fit, err):
    chi2 = 0
    ndf = 0
    for i in range(len(data)):
        if err[i]==0:
            chi2 += pow((data[i] - fit[i])/(err[i]+1), 2)
        else:
            chi2 += pow((data[i] - fit[i])/(err[i]), 2)
        ndf += 1
    return chi2, ndf-1

# Classe pour utilisation et analyse des données
class Set_data:
    def __init__(self, energy, energy_name):
        self.energy = energy
        self.energy_name = energy_name
        self.x = None
        self.distance_int = None
        self.data_entries = None
        self.data_err = None
        self.binscenters = None
        self.parameters = None
        self.fit_exp = None
        self.chi2 = None
        self.ndf = None

    def get_chi2(self):
        return self.chi2, self.ndf
    
    def get_mu(self):
        return self.parameters[1]

    def set_distance_int(self, distance_int):
        self.distance_int = distance_int

    def fit(self):
        self.x = np.linspace(0, max(self.distance_int),
                             int(np.sqrt(len(self.distance_int))))
        self.data_entries, self.bins_1 = np.histogram(
            self.distance_int, bins=self.x)
        self.data_err = self.data_entries/np.sqrt(self.data_entries+0.001)
        self.binscenters = np.array(
            [0.5 * (self.x[i] + self.x[i+1]) for i in range(len(self.x)-1)])
        self.parameters, self.covariance = curve_fit(
            fonction, self.binscenters, self.data_entries)
        self.fit_exp = fonction(self.x, self.parameters[0], self.parameters[1])
        self.chi2, self.ndf = Chi2_test(
            self.data_entries, self.fit_exp, self.data_err)

    def affiche(self):
        print("Nom:", self.energy_name)
        print(self.data_entries)
        print(self.data_err)
        print("Chi2 :", Chi2_test(self.data_entries, self.fit_exp, self.data_err))

    def plot(self):
        plt.bar(self.binscenters, self.data_entries,
                width=self.x[1] - self.x[0], color='navy', label=self.energy_name)
        plt.plot(self.x, self.fit_exp, label='fit : $x_0 e^{-\mu x}$ \n$x_0$ = %4.1f \n$\mu_{%s}$ = %4.4f \n$\chi^{2} /ndf$ = %4.1f/%4.0f' %(self.parameters[0], self.energy_name, self.parameters[1], self.chi2, self.ndf), color='red')
        plt.xlabel("Distance (cm)")
        plt.ylabel("Count")
        plt.legend(loc=1, prop={'size': 16})
