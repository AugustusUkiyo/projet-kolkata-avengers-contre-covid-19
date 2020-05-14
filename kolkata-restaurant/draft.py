#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 23:51:47 2020

@author: ukiyo
"""
 
import random


def gain(posJoueurs, liste_gain, pos_restau):
    d = dict()
    for i in pos_restau :
        d[i] = []
    for i in range(len(posJoueurs)):
        if posJoueurs[i] in d:
            d[posJoueurs[i]].append(i)
    for key, value in d.items():
        if len(value) == 1 :
            liste_gain[value[0]] = liste_gain[value[0]] + 1
        elif len(value) > 1 :
            i = random.randint(0, len(value)-1)
            liste_gain[value[i]] = liste_gain[value[i]] + 1
    return d

def terminer(chemin):
    for i in chemin:
        if len(i) > 0:
            return False
    return True

def donner_strategie_aux_joeurs(L, strategie_joueur):
    for j in range(len(L)):
        for i in range(j*len(strategie_joueur)//len(L), min((j+1)*len(strategie_joueur)//len(L), len(strategie_joueur))):
            print(i,j)
            strategie_joueur[i] = L[j].nouvelle_strategie(i)


#print(L)
#print(strat)