#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 22:12:41 2020

@author: ukiyo
"""
from abc import abstractmethod
import functools
import heapq
import numpy as np

def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2) 
    
###############################################################################

class Probleme(object):
    """ On definit un probleme comme étant: 
        - un état initial
        - un état but
        - une heuristique
        """
        
    def __init__(self,init,but,heuristique):
        self.init=init
        self.but=but
        self.heuristique=heuristique
        
    @abstractmethod
    def estBut(self,e):
        """ retourne vrai si l'état e est un état but
            """
        pass
        
    @abstractmethod    
    def cost(self,e1,e2):
        """ donne le cout d'une action entre e1 et e2, 
            """
        pass
        
    @abstractmethod
    def successeurs(self,etat):
        """ retourne une liste avec les successeurs possibles
            """
        pass
        
    @abstractmethod
    def immatriculation(self,etat):
        """ génère une chaine permettant d'identifier un état de manière unique
            """
        pass
    
    



###############################################################################

@functools.total_ordering # to provide comparison of nodes
class Noeud:
    def __init__(self, etat, g, pere=None):
        self.etat = etat
        self.g = g
        self.pere = pere
        
    def __str__(self):
        #return np.array_str(self.etat) + "valeur=" + str(self.g)
        return str(self.etat) + " valeur=" + str(self.g)
        
    def __eq__(self, other):
        return str(self) == str(other)
        
    def __lt__(self, other):
        return str(self) < str(other)
        
    def expand(self,p):
        """ étend un noeud avec ces fils
            pour un probleme de taquin p donné
            """
        nouveaux_fils = [Noeud(s,self.g+p.cost(self.etat,s),self) for s in p.successeurs(self.etat)]
        return nouveaux_fils
        
    def expandNext(self,p,k):
        """ étend un noeud unique, le k-ième fils du noeud n
            ou liste vide si plus de noeud à étendre
            """
        nouveaux_fils = self.expand(p)
        if len(nouveaux_fils)<k: 
            return []
        else: 
            return self.expand(p)[k-1]
            
    def trace(self,p):
        """ affiche tous les ancetres du noeud
            """
        n = self
        c=0 
        l = []
        while n!=None :
            l.append(n.etat)
            #print (n)
            n = n.pere
            c+=1
        print ("Nombre d'étapes de la solution:", c-1)
        l.reverse()
        return l           
        
        
###############################################################################

class ProblemeJeu(Probleme):
    """
        le jeu est defini:
            la position initiale
            la position but
            matrice heuristique du jeu
    """
    # Creer une grille heuristique du jeu
    
    def __init__(self,init,but,wall):
        self.init=init
        self.but=but
        self.wall=wall
        # Creer une grille heuristique du jeu
        self.grille_h = np.full((20, 20), 1000)
        for i in range(20):
            for j in range(20):
                if (i,j) not in self.wall:
                    heuristique = distManhattan((i,j),self.but)
                    self.grille_h[i,j] = heuristique
    
    def cost(self,e1,e2):
        """ donne le cout d'une action entre e1 et e2, 
            toujours 1 pour ce jeu
            """
        return 1
    
    def estBut(self,e):
        """ retourne vrai si l'état e est un état but
            """
        if e == self.but:
            return True
        return False#(self.but==e[0]).all()
    
    def h_value(self,e):
        """ renvoie la valeur heuristique entre etat current et etat final
        """
        x,y = e
        return self.grille_h[x,y]
    
    def successeurs(self,etat):
        """ retourne une liste des etats suivants 
            """
        l = []
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        for x_inc,y_inc in directions:
            next_row = etat[0] + x_inc
            next_col = etat[1] + y_inc
            if next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                l.append((next_row,next_col))
        return l

def astar(p):
    """ application de l'algorithme a-star sur un probleme donné
        """
    nodeInit = Noeud(p.init, 0, None)
    frontiere = [(nodeInit.g + p.h_value(nodeInit.etat), nodeInit)] 
    reserve = {}        
    bestNoeud = nodeInit
    
    while frontiere != [] and not p.estBut(bestNoeud.etat):              
        (min_f,bestNoeud) = heapq.heappop(frontiere)         
    # Suppose qu'un noeud en réserve n'est jamais ré-étendu 
    # Hypothèse de consistence de l'heuristique
    # ne gère pas les duplicatas dans la frontière
        #print(bestNoeud.etat)
        if bestNoeud.etat not in reserve:            
            reserve[bestNoeud.etat] = bestNoeud.g #maj de reserve
            nouveauxNoeuds = bestNoeud.expand(p)            
            for n in nouveauxNoeuds:
                f = n.g+p.h_value(n.etat)
                heapq.heappush(frontiere, (f,n))              
    # Afficher le résultat                    
    return bestNoeud.trace(p)
    
    