#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 13:28:08 2021

@author: quentin
"""
# Estimation de la valeur de pi à l'aide de méthode Monte Carlo 

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from random import random
import time

start_time = time.time()

def est_inf(x, y):
    if x<=y:
        return True
    else: 
        return False

def est_dans_cercle(a, b, R):
    if (a*a + b*b) <= R**(1/2):
    #if (a*a + b*b)**(1/2) <= R:
        return True
    else:
        return False


a = 1
b = 0.5
cercle = 1

resultat = est_inf(a, b)
#print(resultat)

resultat1 = est_dans_cercle(a, b, cercle)
#print(resultat1)

surface_cercle = 0

Nb_essai_4 = 0
Nb_essai_6 = 0

tirages = 100

x = [i for i in range(tirages)]
PI = [np.pi for i in range(tirages)]
limite_4 = [pow(10, -4) for i in range(tirages)]
limite_6 = [pow(10, -6) for i in range(tirages)]

###################################################################################
# Calcul avec un quart de cerle 
###################################################################################
pi_i_quart = np.zeros(tirages)
err_pi_quart = np.zeros(tirages)
t_calcul_quart = np.zeros(tirages)
surface_cercle = 0

R1 = np.zeros(tirages)
R2 = np.zeros(tirages)
theta = np.linspace(0, 2*np.pi, 100)
r = 1
x1 = r*np.cos(theta)
x2 = r*np.sin(theta)

print("Calcul avec un quart de cercle :")
start_calcul = time.time()
# Calcul simple
for i in range(0, tirages):
    R1[i] = random()
    R2[i] = random()
        
    if est_dans_cercle(R1[i], R2[i], 1):
        surface_cercle += 1
    if i > 0:    
        pi_i_quart[i] = 4*surface_cercle/i
        err_pi_quart[i] = (abs(np.pi-pi_i_quart[i])/np.pi)
        t_calcul_quart[i] = time.time() - start_calcul



# Plot des grahiques du calcul de pi 
pl.figure(figsize=(20, 12))
plt.plot(x, pi_i_quart)
plt.plot(x, PI, color='red', linewidth=2.5, label="Valeur $\pi$ réelle")
plt.title("Calcul de $\pi$", fontsize=20)
plt.xlabel("Nb d'essai (-)", fontsize=20)
plt.ylabel("Valeur de $\pi$", fontsize=20)
plt.ylim(2,4)
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()

pl.figure(figsize=(20, 12))
plt.plot(x, err_pi_quart)
plt.plot(x, limite_4, label="erreur relative $10^{-4}$")
plt.plot(x, limite_6, label="erreur relative $10^{-6}$")
plt.title("Erreur sur le calcul de $\pi$", fontsize=20)
plt.xlabel("Nb d'essai (-)", fontsize=20)
plt.ylabel("Erreur sur $\pi$", fontsize=20)
#plt.ylim(0,0.1)
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.show()

pl.figure(figsize=(20, 12))
plt.plot(x, t_calcul_quart)
plt.title("Temps de calcul", fontsize=20)
plt.xlabel("Nb d'essai (-)", fontsize=20)
plt.ylabel("Temps de calcul (s)", fontsize=20)
plt.yscale("log")
plt.xscale('log')
plt.show()

pl.figure(figsize=(20, 20))
plt.plot(x1, x2, linewidth=4)
plt.title("Visualisation avec un quart de cercle", fontsize=20)
plt.xlim(0,1)
plt.ylim(0,1)
plt.xlabel("x", fontsize=20) 
plt.ylabel("y", fontsize=20)
plt.scatter(R1, R2, color="orange", linewidth=0.2)
plt.pause(0.01)

print("Estimation de pi avec %.0f tirages, pi = %f"%(tirages, 4*surface_cercle/tirages))
print("-------------------\n \n")



##########################################################################################
# Test
##########################################################################################

cercle = 0
tirage_1 = 0
tirage_2 = 0
nombre_tirages = 1000
repetition = 1000

pi_result = np.zeros(repetition)
pi_error = np.zeros(repetition)


for i in range(0, repetition):
    cercle = 0
    for j in range(0, nombre_tirages):
        tirage_1 = random()
        tirage_2 = random()
            
        if est_dans_cercle(tirage_1, tirage_2, 1):
            cercle += 1
        
    pi_result[i] = 4*cercle/nombre_tirages

print("Estimation de pi : %f +- %f"%(pi_result.mean(), pi_result.std()))

pl.figure(figsize=(20, 12))
plt.hist(pi_result, 100)
plt.show()



























"""
###################################################################################
# Calcul avec un cerle entier
###################################################################################
pi_i_entier=np.zeros(tirages)
err_pi_entier = np.zeros(tirages)
t_calcul_entier = np.zeros(tirages)
surface_cercle = 0

r1 = np.zeros(tirages)
r2 = np.zeros(tirages)

print("Calcul avec un cercle entier: ")
start_calcul = time.time()
# Calcul simple
for i in range(0, tirages):
    r1[i] = random()*2 -1
    r2[i] = random()*2 -1

    if est_dans_cercle(r1[i], r2[i], 1):
        surface_cercle += 1
    if i > 0:    
        pi_i_entier[i] = 4*surface_cercle/i
        err_pi_entier[i] = (abs(np.pi-pi_i_entier[i])/np.pi)
        t_calcul_entier[i] = time.time() - start_calcul
        

# Plot des grahiques du calcul de pi 
pl.figure(figsize=(20, 12))
plt.plot(x, pi_i_entier)
plt.plot(x, PI, color='red', linewidth=2.5)
plt.title("Calcul de $\pi$", fontsize=20)
plt.xlabel("Nb d'essai (-)", fontsize=20)
plt.ylabel("Valeur de $\pi$", fontsize=20)
plt.ylim(2,4)
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()
 
pl.figure(figsize=(20, 12))
plt.plot(x, err_pi_entier)
plt.plot(x, limite_4, label="erreur relative $10^{-4}$")
plt.plot(x, limite_6, label="erreur relative $10^{-6}$")
plt.title("Erreur sur le calcul de $\pi$", fontsize=20)
plt.xlabel("Nb d'essai (-)", fontsize=20)
plt.ylabel("Erreur sur $\pi$", fontsize=20)
#plt.ylim(0,0.1)
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.show()

pl.figure(figsize=(20, 12))
plt.plot(x, t_calcul_entier)
plt.title("Temps de calcul", fontsize=20)
plt.xlabel("Nb d'essai (-)", fontsize=20)
plt.ylabel("Temps de calcul (s)", fontsize=20)
plt.yscale("log")
plt.xscale('log')
plt.show()

pl.figure(figsize=(20, 20))
plt.plot(x1, x2, linewidth=4)
plt.title("Visualisation avec un cercle entier", fontsize=20)
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.xlabel("x", fontsize=20) 
plt.ylabel("y", fontsize=20)
plt.scatter(r1, r2, color="orange", linewidth=0.2)


print("Estimation de pi avec %.0f tirages, pi = %f "%(tirages, 4*surface_cercle/tirages))
print("-------------------\n \n")
"""

duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)
