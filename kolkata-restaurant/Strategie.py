#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 17:00:35 2020

@author: ukiyo
"""

import random

class Strategie:
    liste = [] # liste des positions de restau
    d = dict()
    
    def liste_strategies(liste):
        Strategie.liste = liste
        
    def prendre_indice_restaurant(self):
        raise NotImplementedError("not implemented prendre_strategie")
        
    def repartition(d):
        for key, value in d.items():
            d[key] = len(value)
        Strategie.d = d
    
    def nouvelle_strategie(self, i):
        raise NotImplementedError("not implemented nouvelle_strategie")
        
    def get_nom(self):
        return "Strategie"
    
class StrategieAleatoire(Strategie):
    
    def prendre_indice_restaurant(self):
        return random.randint(0,len(Strategie.liste)-1)
    
    def nouvelle_strategie(self, i):
        return StrategieAleatoire()
    
    def get_nom(self):
        return "Strategie aleatoire"
    
class StrategieTeTu(Strategie):
    
    def __init__(self):
        self.strategie = random.randint(0,len(Strategie.liste)-1)
        
    def prendre_indice_restaurant(self):
        return self.strategie
    
    def nouvelle_strategie(self, i):
        return StrategieTeTu()
    
    def get_nom(self):
        return "Strategie tetu"
    
class StrategieMoinsRempli(Strategie):
    
    def prendre_indice_restaurant(self):
        if len(Strategie.d) == 0:
            return random.randint(0,len(Strategie.liste)-1)
        return Strategie.liste.index(min(Strategie.d, key=Strategie.d.get))
    
    def nouvelle_strategie(self, i):
        return StrategieMoinsRempli()
    
    def get_nom(self):
        return "Strategie moins rempli"
    
class StrategieRestauPlusProche(Strategie):
    
    def __init__(self, liste_posJoueurs, indice_Joueur):
        self.liste_posJoueurs = liste_posJoueurs
        self.indice_Joueur = indice_Joueur
        
    def prendre_indice_restaurant(self):
        distance_min = -1
        restau_plus_proche = 0
        p_x, p_y = self.liste_posJoueurs[self.indice_Joueur]
        for i in range(len(Strategie.liste)):
            r_x, r_y = Strategie.liste[i]
            distance = abs(p_x - r_x) + abs(p_y - r_y)
            if distance != 0 and (distance < distance_min or distance_min == -1):
                distance_min = distance
                restau_plus_proche = i
        return restau_plus_proche
    
    def nouvelle_strategie(self, i):
        return StrategieRestauPlusProche(self.liste_posJoueurs, i)
    
    def get_nom(self):
        return "Strategie restaurant le plus proche "
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
