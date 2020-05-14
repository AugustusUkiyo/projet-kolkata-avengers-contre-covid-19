# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys


    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default 20
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()

    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = len(goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or  goalStates] 
    
    #-------------------------------
    # Placement aleatoire des joueurs, en évitant les obstacles
    #-------------------------------
        
    posPlayers = initStates

    
    for j in range(nbPlayers):
        x,y = random.choice(allowedStates)
        players[j].set_rowcol(x,y)
        game.mainiteration()
        posPlayers[j]=(x,y)

    #-------------------------------
    # chaque joueur choisit un restaurant
    #-------------------------------

    restau=[0]*nbPlayers
    for j in range(nbPlayers):
        c = random.randint(0,nbRestaus-1)
        print(c)
        restau[j]=c
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
    # A-star
    from A_star import astar, ProblemeJeu
    
    # Strategies
    from Strategie import Strategie
    from Strategie import StrategieAleatoire
    from Strategie import StrategieTeTu
    from Strategie import StrategieMoinsRempli
    from Strategie import StrategieRestauPlusProche
    from draft import donner_strategie_aux_joeurs, terminer, gain
    Strategie.liste_strategies(goalStates)
    strat = [None]*10
    L=[]
    L.append(StrategieTeTu())
    L.append(StrategieAleatoire())
    L.append(StrategieMoinsRempli())
    L.append(StrategieRestauPlusProche(posPlayers,0))
    donner_strategie_aux_joeurs(L, strat)
    """
    strat_alea = StrategieAleatoire()
    strat_tetu = StrategieTeTu()
    strat_moins_rempli = StrategieMoinsRempli()
    strat_restau_plus_proche = StrategieRestauPlusProche(posPlayers,0)
    strat = [strat_alea.nouvelle_strategie(0),
             strat_tetu.nouvelle_strategie(1),
             strat_tetu.nouvelle_strategie(2),
             strat_tetu.nouvelle_strategie(3),
             strat_tetu.nouvelle_strategie(4),
             strat_moins_rempli.nouvelle_strategie(5),
             strat_restau_plus_proche.nouvelle_strategie(6),
             strat_restau_plus_proche.nouvelle_strategie(7),
             strat_restau_plus_proche.nouvelle_strategie(8),
             strat_restau_plus_proche.nouvelle_strategie(9),]
    """
    liste_gain = np.zeros(nbPlayers)
    list_goal = [None]*nbPlayers
    for j in range(iterations):

        # ==== Initialisation des positions d'arriver
        chemin = [None]*nbPlayers
        for k in range(nbPlayers):
            list_goal[k] = goalStates[strat[k].prendre_indice_restaurant()]
            p = ProblemeJeu(posPlayers[k], list_goal[k], wallStates)
            chemin[k] = astar(p)


        while (not terminer(chemin)):
            for i in range(len(chemin)):
                if len(chemin[i]) == 0:
                    continue
                next_row,next_col = chemin[i].pop(0)
                players[i].set_rowcol(next_row,next_col)
                game.mainiteration()
                col=next_col
                row=next_row
                posPlayers[i] = (row,col)
                if (row,col) == list_goal[i]:
                    game.mainiteration()
        d = gain(posPlayers, liste_gain, goalStates)
        Strategie.repartition(d)
        
        # Placement aleatoire des joueurs, en évitant les obstacles
        #-------------------------------           
        posPlayers = initStates    
        for j in range(nbPlayers):
            x,y = random.choice(allowedStates)
            players[j].set_rowcol(x,y)
            game.mainiteration()
            posPlayers[j]=(x,y)

    for k in range(len(liste_gain)) :
        print("resultat joueur",k)
        print("type de stratégie: ",strat[k].get_nom())
        print("score :", liste_gain[k])
        print("score moyen :", liste_gain[k]/iterations)
    print(liste_gain)
    
        
    # bon ici on fait juste plusieurs random walker pour exemple...
    """
    for i in range(iterations):
        
        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            row,col = posPlayers[j]
            # choisir aleatoire un resto
            
            resto = restau[j]
            p = A_start.ProblemeJeu((row,col), goalStates[resto], wallStates)
            l = A_start.astar(p)
            print('debut')
            print('Joueur ', j,'a position ',(row,col),' va au restau ', resto)
            print(l)
            print('fin')
            
            x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            next_row = row+x_inc
            next_col = col+y_inc
            # and ((next_row,next_col) not in posPlayers)
            if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                players[j].set_rowcol(next_row,next_col)
                print ("pos :", j, next_row,next_col)
                game.mainiteration()
    
                col=next_col
                row=next_row
                posPlayers[j]=(row,col)
            
            
      
        
            
            # si on est à l'emplacement d'un restaurant, on s'arrête
            if (row,col) == restau[j]:
                #o = players[j].ramasse(game.layers)
                game.mainiteration()
                print ("Le joueur ", j, " est à son restaurant.")
               # goalStates.remove((row,col)) # on enlève ce goalState de la liste
                
                
                break
    """        
    
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


