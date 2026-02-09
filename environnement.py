from collections import deque
from staticmap import StaticMap
from coordonnee import Coordonnee
from typing import TypeVar, Generic, Dict, Set 
import heapq

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
        file = []
        path = []
        current_cost = 0 
        self.map.sommets[Coordonnee(self.current_agent_col, self.current_agent_line)].visited = True
        self.trouver_action_possible(file, current_cost)
        while file:
            cost, action, coordonnee = heapq.heappop(file)
            path.append(action)
            #path.append((coordonnee.i, coordonnee.j))
            self.map.sommets[coordonnee].visited = True
            self.current_agent_col = coordonnee.i
            self.current_agent_line = coordonnee.j
            if coordonnee == Coordonnee(self.goal_col, self.goal_line):
                if self.goal_col == self.OR_col:
                    path.append('s')
                elif self.goal_col == self.start_col:
                    path.append('q')
                return path
            if action in (FLECHE_GAUCHE,FLECHE_DROITE,FLECHE_HAUT,FLECHE_BAS):
                self.actualiser_wumpus(action)

            self.trouver_action_possible(file, current_cost)

    def debuter_retour_case_depart(self):
        self.goal_line = self.start_line
        self.goal_col = self.start_col
        
        for coord, sommet in self.map.sommets.items():
            sommet.visited = False
        
    def actualiser_wumpus(self, action):
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
                
    def ajouter_cout(self, file, action, next_agent_col, next_agent_line, current_cost):
        """
        f(q) = g(q) + h(q)
        Fonction pour minimiser f(q)
        """
        #calcul g(q)
        if action in (FLECHE_GAUCHE,FLECHE_DROITE,FLECHE_HAUT,FLECHE_BAS):
            g = current_cost + COUT_FLECHE
        else:
            g = current_cost + self.map.sommets[Coordonnee(next_agent_col, next_agent_line)].poids
        #calcul de h(q)
        h = self.calculer_distance_manhattan(next_agent_col, next_agent_line)
        
        f = g + h
        #print(f"g: {g} h: {h} f: {f} - ({next_agent_col}, {next_agent_line})" )
        heapq.heappush(file, (f, action, Coordonnee(next_agent_col, next_agent_line)))   # Il faut trouver comment faire en sorte que l'info recupere ici soit suffisante pour parcours

    def calculer_distance_manhattan(self, next_agent_col, next_agent_line):
        x = abs(self.goal_col - next_agent_col)
        y = abs(self.goal_line - next_agent_line)
        return y + x

    def trouver_action_possible(self, file, current_cost):
        positions_wumpus_visible = self.trouver_wumpus_visible_par_agent()
        if self.current_agent_col < TAILLE_CARTE -1: #DEPLACEMENT A DROITE POSSIBLE
            if not self.map.sommets[Coordonnee(self.current_agent_col + 1, self.current_agent_line)].visited:
                self.ajouter_cout(file, DEPLACEMENT_DROITE, self.current_agent_col + 1, self.current_agent_line, current_cost)
        if self.current_agent_col > 0:               #DEPLACEMENT A GAUCHE POSSIBLE
            if not self.map.sommets[Coordonnee(self.current_agent_col - 1, self.current_agent_line)].visited:
                self.ajouter_cout(file, DEPLACEMENT_GAUCHE, self.current_agent_col - 1, self.current_agent_line, current_cost)
        if self.current_agent_line < TAILLE_CARTE -1: #DEPLACEMENT EN BAS POSSIBLE
            if not self.map.sommets[Coordonnee(self.current_agent_col, self.current_agent_line + 1)].visited:
                self.ajouter_cout(file, DEPLACEMENT_BAS, self.current_agent_col, self.current_agent_line + 1, current_cost)
        if self.current_agent_line > 0:               #DEPLACEMENT EN HAUT POSSIBLE
            if not self.map.sommets[Coordonnee(self.current_agent_col, self.current_agent_line - 1)].visited:
                self.ajouter_cout(file, DEPLACEMENT_HAUT, self.current_agent_col, self.current_agent_line - 1, current_cost)
        
        if positions_wumpus_visible:
            for wumpus_position in positions_wumpus_visible:
                if self.current_agent_col == wumpus_position[0]:                                           #UN AGENT ET UN WUMPUS SONT SUR LA MÊME COLONNE
                    if self.current_agent_line > wumpus_position[1]:                                       #TIR POSSIBLE VERS LE HAUT
                        self.ajouter_cout(file, FLECHE_HAUT, self.current_agent_col, self.current_agent_line, current_cost)
                        #frontiere['H'] = (self.current_agent_col, self.current_agent_line)                #POSITION RESTE LA MÊME 
                    else:                                                                                  #TIR POSSIBLE VERS LE BAS
                        self.ajouter_cout(file, FLECHE_BAS, self.current_agent_col, self.current_agent_line, current_cost)
                        #frontiere['B'] = (self.current_agent_col, self.current_agent_line)                #POSITION RESTE LA MÊME 
                        
                elif self.current_agent_line == wumpus_position[1]:                         #UN AGENT ET UN WUMPUS SONT SUR LA MÊME LIGNE
                    if self.current_agent_col > wumpus_position[0]:                         #TIR POSSIBLE VERS LA GAUCHE
                        self.ajouter_cout(file, FLECHE_GAUCHE, self.current_agent_col, self.current_agent_line, current_cost)
                        #frontiere['G'] = (self.current_agent_col, self.current_agent_line)  #POSITION RESTE LA MÊME 
                    else:                                                                   #TIR POSSIBLE VERS LA DROITE
                        self.ajouter_cout(file, FLECHE_DROITE, self.current_agent_col, self.current_agent_line, current_cost)
                        #frontiere['D'] = (self.current_agent_col, self.current_agent_line)  #POSITION RESTE LA MÊME 

    def trouver_wumpus_visible_par_agent(self):
        wumpus_visible = []
        for index_col, contient_wumpus in enumerate(self.current_wumpus_position[self.current_agent_line]):
            if contient_wumpus:
                wumpus_visible.append((index_col, self.current_agent_line))
        for index_ligne, contient_wumpus in enumerate(self.current_wumpus_position):
            if contient_wumpus[self.current_agent_col]:
                wumpus_visible.append((self.current_agent_col, index_ligne))
        return wumpus_visible
    
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
    
    def __getitem__(self, pos):
        """
        Permet d'utiliser env[x, y] pour accéder au sommet en (x, y)
        pos: tuple (x, y)
        """
        if not (isinstance(pos, tuple) and len(pos) == 2):
            raise TypeError("Index doit être un tuple (x, y)")
        
        x, y = pos
        c = Coordonnee(x, y)
        
        # Retourne le sommet correspondant dans le graphe
        if c in self.map.sommets:
            return self.map.sommets[c]
        else:
            raise KeyError(f"Coordonnee {c} non trouvée dans le graphe")
