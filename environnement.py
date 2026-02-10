"""
INF4230 - INTELLIGENCE ARTIFICIELLE
UQAM | Faculté des sciences | Département d'informatique
TP1 : Jeu du Wumpus
ETUDIANT : DEGNI KAIKOU LOIC DEGK24059500
Module : environnement.py
"""

from collections import deque
from staticmap import StaticMap
from coordonnee import Coordonnee
from typing import TypeVar, Generic, Dict, Set 
import heapq
import math

# Constantes
PERTE_MORTELLE = float("inf")
GAIN_OR = 10**100
COUT_FLECHE = 10**50
TAILLE_CARTE = 4

DEPLACEMENT_DROITE = 'd'
DEPLACEMENT_GAUCHE = 'g'
DEPLACEMENT_HAUT = 'h'
DEPLACEMENT_BAS = 'b'
FLECHE_DROITE = 'D'
FLECHE_GAUCHE = 'G'
FLECHE_HAUT = 'H'
FLECHE_BAS = 'B'
SAISIR = 's'
QUITTER = 'q'

S = TypeVar("S")

class Environnement(Generic[S]):
    
    def __init__(self, carte_poid, ensemble_puit, ensemble_wumpus, ensemble_poids, OR_line, OR_col, pos_line = 3, pos_col = 0):
        #Statique
        self.OR_line = OR_line
        self.OR_col = OR_col
        self.start_line = pos_line
        self.start_col = pos_col
        self.goal_line = OR_line
        self.goal_col = OR_col

        #Etat courant
        self.current_agent_line = pos_line
        self.current_agent_col = pos_col
        self.current_wumpus_position = ensemble_wumpus
        
        self.map: StaticMap = StaticMap[S, int]()
        self.ajouter_sommets_carte(carte_poid, ensemble_puit, ensemble_wumpus, ensemble_poids)
    #-------------------------------------------------------------------------------------------------------------------------------------------
    # Interface publique
    def Resoudre_A_star(self):
        '''
            Fonction servant a résoudre A*
            
            Return: 
            None si aucune suite d'action possible
            path si une suite d'action est trouve
        '''
        file = []
        path = []
        parents = self.creer_map_parents()
        current_cost = 0 
        self.map.sommets[Coordonnee(self.current_agent_col, self.current_agent_line)].visited = True
        self.trouver_action_possible(file, current_cost)
        
        #Boucle principale
        while file:
            cost, action, coordonnee = heapq.heappop(file)
            
            #S'il est impossible d'atteindre l'objectif
            if math.isinf(cost):
                return None
            
            self.map.sommets[coordonnee].visited = True
            self.current_agent_col = coordonnee.i
            self.current_agent_line = coordonnee.j
            
            #Si l'action est un deplacement
            if action == DEPLACEMENT_DROITE:
                parents[coordonnee] = Coordonnee(coordonnee.i - 1, coordonnee.j)
            elif action == DEPLACEMENT_GAUCHE:
                parents[coordonnee] = Coordonnee(coordonnee.i + 1, coordonnee.j)
            elif action == DEPLACEMENT_BAS:
                parents[coordonnee] = Coordonnee(coordonnee.i, coordonnee.j - 1)
            elif action == DEPLACEMENT_HAUT:
                parents[coordonnee] = Coordonnee(coordonnee.i, coordonnee.j + 1)
            #Si l'action est un tirer de fleche
            if action in (FLECHE_GAUCHE,FLECHE_DROITE,FLECHE_HAUT,FLECHE_BAS):
                self.actualiser_poids_wumpus_sur_carte(action)
                
            path.append((action,coordonnee))

            #Si nous atteignons notre objectif
            if coordonnee == Coordonnee(self.goal_col, self.goal_line):
                if self.goal_col == self.OR_col and self.goal_line == self.OR_line:
                    path.append((SAISIR, Coordonnee(self.goal_col, self.goal_line)))
                elif self.goal_col == self.start_col and self.goal_line == self.start_line:
                    path.append((QUITTER, Coordonnee(self.goal_col, self.goal_line)))
                return self.create_path(path, parents)
            
            #Exploration
            self.trouver_action_possible(file, current_cost)

    def create_path(self, path, parents):
        ''' 
            path_element[0] : action 
            path_element[1] : coordonnee
            
            Return:
            Suite action effectué en ordre
        '''
        nouveau_path = []
        coord_courant = None
        count = 0
        for path_element in reversed(path):
            if path_element[0] in (SAISIR,QUITTER):
                nouveau_path.append(path_element[0])
                coord_courant = path_element[1]
            elif coord_courant == path_element[1]:
                nouveau_path.append(path_element[0])
            else:
                if parents[coord_courant] == path_element[1]:
                    nouveau_path.append(path_element[0])
                    coord_courant = path_element[1]
            count = count + 1
        nouveau_path.reverse()
        return nouveau_path
    
    def creer_map_parents(self):
        dict = {}
        for coordonnee in self.map.sommets.keys():
            dict[coordonnee] = None
        return dict
    
    def debuter_retour_case_depart(self):
        self.goal_line = self.start_line
        self.goal_col = self.start_col
        for coord, sommet in self.map.sommets.items():
            sommet.visited = False
        
    def actualiser_poids_wumpus_sur_carte(self, action):
        '''Une fois un Wumpus touche le poids pours acceder a sa case devient 0'''
        if action == FLECHE_GAUCHE:
            i = self.current_agent_col
            while i >= 0:
                if self.current_wumpus_position[self.current_agent_line][i]:
                    self.map.sommets[Coordonnee(i, self.current_agent_line)].poids = 0
                    self.current_wumpus_position[self.current_agent_line][i] = False
                i = i - 1
                
        if action == FLECHE_DROITE:
            i = self.current_agent_col
            while i <= TAILLE_CARTE -1 :
                if self.current_wumpus_position[self.current_agent_line][i]:
                    self.map.sommets[Coordonnee(i, self.current_agent_line)].poids = 0
                    self.current_wumpus_position[self.current_agent_line][i] = False
                i = i + 1
                
        if action == FLECHE_HAUT:
            j = self.current_agent_line
            while j >= 0:
                if self.current_wumpus_position[j][self.current_agent_col]:
                    self.map.sommets[Coordonnee(self.current_agent_col, j)].poids = 0
                    self.current_wumpus_position[j][self.current_agent_col] = False
                j = j - 1
                
        if action == FLECHE_BAS:
            j = self.current_agent_col
            while j <= TAILLE_CARTE:
                if self.current_wumpus_position[j][self.current_agent_col]:
                    self.map.sommets[Coordonnee(self.current_agent_col, j)].poids = 0
                    self.current_wumpus_position[j][self.current_agent_col] = False
                j = j + 1
                
    def ajouter_cout(self, file, action, next_agent_col, next_agent_line, current_cost, nb_wumpus_touche=0):
        """
        Fonction pour minimiser f(q)
        f(q) = g(q) + h(q)
        Heuristique: 
        h(q) : distance de Manhattan entre prochaine position et position de fin lors
        nb_wumpus_touche : on reduis le cout du tire d'une flèche du nombre de wumpus qu'elle touche
        """
        #calcul g(q)
        if action in (FLECHE_GAUCHE,FLECHE_DROITE,FLECHE_HAUT,FLECHE_BAS):
            g = current_cost + COUT_FLECHE - nb_wumpus_touche
        else:
            g = current_cost + self.map.sommets[Coordonnee(next_agent_col, next_agent_line)].poids
        #calcul de h(q)
        h = self.calculer_distance_manhattan(next_agent_col, next_agent_line)
        f = g + h
        heapq.heappush(file, (f, action, Coordonnee(next_agent_col, next_agent_line)))   
        
    def calculer_distance_manhattan(self, next_agent_col, next_agent_line):
        x = abs(self.goal_col - next_agent_col)
        y = abs(self.goal_line - next_agent_line)
        return y + x

    def trouver_action_possible(self, file, current_cost):
        '''
            Fonction qui verifie les actions possibles(DEPLACEMENT/FLÈCHE) 
            et les ajoutes avec leurs couts à la file de priorité
        '''
        #Recherche déplacements possibles
        if self.current_agent_col < TAILLE_CARTE -1:                                                                            #DEPLACEMENT A DROITE POSSIBLE
            if not self.map.sommets[Coordonnee(self.current_agent_col + 1, self.current_agent_line)].visited:
                self.ajouter_cout(file, DEPLACEMENT_DROITE, self.current_agent_col + 1, self.current_agent_line, current_cost)
        if self.current_agent_col > 0:                                                                                          #DEPLACEMENT A GAUCHE POSSIBLE
            if not self.map.sommets[Coordonnee(self.current_agent_col - 1, self.current_agent_line)].visited:
                self.ajouter_cout(file, DEPLACEMENT_GAUCHE, self.current_agent_col - 1, self.current_agent_line, current_cost)
        if self.current_agent_line < TAILLE_CARTE -1:                                                                           #DEPLACEMENT EN BAS POSSIBLE
            if not self.map.sommets[Coordonnee(self.current_agent_col, self.current_agent_line + 1)].visited:
                self.ajouter_cout(file, DEPLACEMENT_BAS, self.current_agent_col, self.current_agent_line + 1, current_cost)
        if self.current_agent_line > 0:                                                                                         #DEPLACEMENT EN HAUT POSSIBLE
            if not self.map.sommets[Coordonnee(self.current_agent_col, self.current_agent_line - 1)].visited:
                self.ajouter_cout(file, DEPLACEMENT_HAUT, self.current_agent_col, self.current_agent_line - 1, current_cost)
        
        #Recherche tires possibles
        wumpus_visible, nb_wumpus_visible_par_direction = self.trouver_wumpus_visible_par_agent()
        if wumpus_visible:
            if nb_wumpus_visible_par_direction[0] != 0:
                self.ajouter_cout(file, FLECHE_GAUCHE, self.current_agent_col, self.current_agent_line, current_cost, nb_wumpus_visible_par_direction[0])
            if nb_wumpus_visible_par_direction[1] != 0:
                self.ajouter_cout(file, FLECHE_DROITE, self.current_agent_col, self.current_agent_line, current_cost, nb_wumpus_visible_par_direction[1])
            if nb_wumpus_visible_par_direction[2] != 0:
                self.ajouter_cout(file, FLECHE_HAUT, self.current_agent_col, self.current_agent_line, current_cost, nb_wumpus_visible_par_direction[2])
            if nb_wumpus_visible_par_direction[3] != 0:
                self.ajouter_cout(file, FLECHE_BAS, self.current_agent_col, self.current_agent_line, current_cost, nb_wumpus_visible_par_direction[3])
                     
    def trouver_wumpus_visible_par_agent(self):
        '''Fonction qui cherche les wumpus atteignables par flèche'''
        nb_wumpus_visible_par_direction = [0,0,0,0]    #[gauche,droite,haut,bas]
        wumpus_visible = False
        for i in range(self.current_agent_col):
            if self.current_wumpus_position[self.current_agent_line][i]:
                wumpus_visible = True
                nb_wumpus_visible_par_direction[0] += 1
        for i in range(self.current_agent_col+1, TAILLE_CARTE):
            if self.current_wumpus_position[self.current_agent_line][i]:
                wumpus_visible = True
                nb_wumpus_visible_par_direction[1] += 1
        for i in range(self.current_agent_line):
            if self.current_wumpus_position[i][self.current_agent_col]:
                wumpus_visible = True
                nb_wumpus_visible_par_direction[2] += 1
        for i in range(self.current_agent_line + 1, TAILLE_CARTE):
            if self.current_wumpus_position[i][self.current_agent_col]:
                wumpus_visible = True
                nb_wumpus_visible_par_direction[3] += 1
        return wumpus_visible, nb_wumpus_visible_par_direction
    
    def ajouter_sommets_carte(self, carte_poid, ensemble_puit, ensemble_wumpus, ensemble_poids):
        for j in range(len(ensemble_puit)):
            for i in range(len(ensemble_puit[j])):
                if ensemble_puit[j][i]:
                    self.map.ajouterSommet(Coordonnee(i, j, PERTE_MORTELLE), PERTE_MORTELLE)
                elif ensemble_wumpus[j][i]:
                    self.map.ajouterSommet(Coordonnee(i, j, PERTE_MORTELLE), PERTE_MORTELLE)
                else:
                    self.map.ajouterSommet(Coordonnee(i, j, ensemble_poids[j][i]), ensemble_poids[j][i])
                self.ajouter_arete_carte(i, j, carte_poid)
        return self.map
    
    def ajouter_arete_carte(self, pos_x, pos_y, carte_poid):
        if pos_x < TAILLE_CARTE - 1:
            self.map.ajouterAreteOrientee(Coordonnee(pos_x, pos_y), Coordonnee(pos_x + 1, pos_y), carte_poid[pos_y][pos_x + 1])
        if pos_x > 0:
            self.map.ajouterAreteOrientee(Coordonnee(pos_x, pos_y), Coordonnee(pos_x - 1, pos_y), carte_poid[pos_y][pos_x - 1])
        if pos_y < TAILLE_CARTE - 1:
            self.map.ajouterAreteOrientee(Coordonnee(pos_x, pos_y), Coordonnee(pos_x, pos_y + 1), carte_poid[pos_y + 1][pos_x])
        if pos_y > 0:
            self.map.ajouterAreteOrientee(Coordonnee(pos_x, pos_y), Coordonnee(pos_x, pos_y - 1), carte_poid[pos_y - 1][pos_x]) 
