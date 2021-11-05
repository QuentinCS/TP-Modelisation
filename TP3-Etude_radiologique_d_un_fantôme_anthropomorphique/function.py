#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 13:32:08 2021

@author: quentin
"""

from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

# Interpolation quadratique 
def Interp (energy, mu, E_i):
    #inter_mu = interpolate.interp1d(energy, mu, kind='quadratic') #quadratique 
    inter_mu = interpolate.interp1d(energy, mu, kind='slinear') # linéaire

    mu_int = np.zeros(4)

    for i in range(0, 4):    
        mu_int[i] = inter_mu(E_i[i])

    return mu_int

# Fonction création du fantôme
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

# Fonction affichage fantôme
def printmatrice(matrice_1, matrice_2, matrice_3, matrice_4, title):
    pl.figure(figsize=(20, 10)) 
    plt.subplot(2, 2, 1)
    plt.imshow(matrice_1)
    plt.title("17 keV")
    plt.xlabel("Longueur (mm)")
    plt.ylabel("Largeur (mm)")
    plt.colorbar(shrink=0.5)
    plt.subplot(2, 2, 2)
    plt.imshow(matrice_2)
    plt.title("16 keV")
    plt.xlabel("Longueur (mm)")
    plt.ylabel("Largeur (mm)")
    plt.colorbar(shrink=0.5)
    plt.subplot(2, 2, 3)
    plt.imshow(matrice_3)
    plt.title("100 keV")
    plt.xlabel("Longueur (mm)")
    plt.ylabel("Largeur (mm)")
    plt.colorbar(shrink=0.5)
    plt.subplot(2, 2, 4)
    plt.imshow(matrice_4)
    plt.title("10 MeV")
    plt.xlabel("Longueur (mm)")
    plt.ylabel("Largeur (mm)")
    plt.colorbar(shrink=0.5)
    plt.suptitle(title, fontsize=30)
    plt.show()











