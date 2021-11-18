#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 14:21:40 2021

@author: quentin
"""

# Code de modélisation d'une source de particule, isotrope, puis collimatée dans l'espace

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pylab as pl
from random import random
from random import uniform
import time


start_time = time.time()


##################################################################################
# Plot source isotrope 
##################################################################################


Nb = 5000
theta = np.zeros(Nb)
phi = np.zeros(Nb)
R = 1


for i in range (Nb):
    theta[i] = uniform(0, np.pi)
    phi[i] = uniform(0, 2*np.pi)


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Emission isotrope de particules")
ax.set_xlabel("")
ax.set_ylabel("y")
ax.set_zlabel("z")

#draw sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = R*np.cos(u)*np.sin(v)
y = R*np.sin(u)*np.sin(v)
z = R*np.cos(v)
#ax.plot_wireframe(x, y, z, color="r") # Visualisation sphère de rayon R
ax.scatter(0, 0, 0, s=50, color='black')

for i in range(Nb):
    ax.scatter(R*np.sin(theta[i])*np.cos(phi[i]), R*np.sin(theta[i])*np.sin(phi[i]), R*np.cos(theta[i]), marker='x')
plt.show()

plt.figure(figsize=(10, 10))
plt.hist2d(theta, phi, bins=(20, 20))
plt.title("Histogramme tirage angles", fontsize=20)
plt.xlabel('\u03B8 (rad)', fontsize=10)
plt.ylabel('\u03C6 (rad)', fontsize=10)
plt.axis([0, np.pi, 0, 2*np.pi])
plt.colorbar(shrink=0.5)





##################################################################################
# Plot source collimatée à un angle de 10° autour de l'axe Z
##################################################################################

theta_col = np.zeros(Nb)
phi_col = np.zeros(Nb)
R_col = 1

for i in range (Nb):
    theta_col[i] = uniform(0, (1/18)*np.pi)
    phi_col[i] = uniform(0, 2*np.pi)


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Emission collimatée de particules")
ax.set_xlabel("")
ax.set_ylabel("y")
ax.set_zlabel("z")

#draw sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = R_col*np.cos(u)*np.sin(v)
y = R_col*np.sin(u)*np.sin(v)
z = R_col*np.cos(v)
#ax.plot_wireframe(x, y, z, color="r")
#ax.scatter(R*np.sin(np.pi)*np.cos(phi[i]), R*np.sin(np.pi)*np.sin(phi[i]), R*np.cos(np.pi), s=500, color='green')
#ax.scatter(R*np.sin(0)*np.cos(phi[i]), R*np.sin(0)*np.sin(phi[i]), R*np.cos(0), s=500, color='blue')
#ax.scatter(R*np.sin(np.pi/2)*np.cos(phi[i]/2), R*np.sin(np.pi/2)*np.sin(phi[i]/2), R*np.cos(np.pi/2), s=500, color='yellow')
ax.scatter(0, 0, 0, s=50, color='black')

for i in range(Nb):
    ax.scatter(R*np.sin(theta_col[i])*np.cos(phi_col[i]), R*np.sin(theta_col[i])*np.sin(phi_col[i]), R*np.cos(theta_col[i]), marker='x')
plt.show()


plt.figure(figsize=(10, 10))
plt.hist2d(theta_col, phi_col, bins=(20, 20))
plt.title("Histogramme tirage angles", fontsize=20)
plt.xlabel('\u03B8 (rad)', fontsize=10)
plt.ylabel('\u03C6 (rad)', fontsize=10)
plt.axis([0, np.pi, 0, 2*np.pi])
plt.colorbar(shrink=0.5)










duree = time.time() - start_time
print ('\n \nTotal running time : %5.3g s' % duree)
