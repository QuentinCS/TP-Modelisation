#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 20:44:19 2021

@author: quentin
"""

import numpy as np

def moy(list1):
    somme = 0
    for i in range(0, len(list1)):
        somme += list1[i]
    
    return somme/(len(list1))

def MLinQ(d, alpha, beta):
    return np.exp(-alpha*d - beta*d*d)

def EBR(survie, alpha1, beta1, alpha2, beta2):
    Dose1 = (-alpha1 + np.sqrt(alpha1*alpha1 -4*beta1*np.log(survie)))/(2*beta1)
    Dose2 = (-alpha2 + np.sqrt(alpha2*alpha2 -4*beta2*np.log(survie)))/(2*beta2)
    
    #print("\n \nDose 1", Dose1)
    #print("Dose 2", Dose2)
    
    return Dose2/Dose1 


def chi2(data, fit, err):
    Chi2 = 0
    for i in range(0, len(data)):
        if err[i] == 0:
            Chi2 += pow((data[i] - fit[i])/(err[i]+1), 2)
        else:
            Chi2 += pow((data[i] - fit[i])/(err[i]), 2)
        #print("chi =", Chi2)
        #print("valeur =", data[i])
        #print("fit =", fit[i]) 
        #print("Err =", err[i], "\n")
        
    return Chi2


