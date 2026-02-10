"""
INF4230 - INTELLIGENCE ARTIFICIELLE
UQAM | Faculté des sciences | Département d'informatique
TP1 : Jeu du Wumpus
ETUDIANT : DEGNI KAIKOU LOIC DEGK24059500
Module : staticmap.py
"""

import sys
from typing import Dict, TypeVar, Generic
from coordonnee import Coordonnee

S = TypeVar("S")  # type des sommets
A = TypeVar("A")  # type des poids (ou étiquettes)
TAILLE_CARTE = 4

class StaticMap(Generic[S, A]):

    class Sommet:
        def __init__(self, poids= None):
            self.voisins: Dict[S, A] = {}
            self.visited: bool = False
            self.poids = poids

    def __init__(self):
        self.sommets: Dict[S, StaticMap.Sommet] = {}

    # ===== Méthodes publiques =====

    def ajouterSommet(self, s: S, poids=None):
        if s not in self.sommets:
            self.sommets[s] = StaticMap.Sommet(poids)

    def ajouterAreteOrientee(self, s1: S, s2: S, p: A):
        self.ajouterSommet(s1)
        self.ajouterSommet(s2,p)
        self.sommets[s1].voisins[s2] = p

    def ajouterAreteNonOrientee(self, s1: S, s2: S, p: A):
        self.ajouterAreteOrientee(s1, s2, p)
        self.ajouterAreteOrientee(s2, s1, p)
        
    def afficher_map(self):
        largeur = 4  # largeur d’une cellule
        ligne_sep = "_" * (TAILLE_CARTE * (largeur + 3))
        sys.stderr.write("\n\n===========================\nCARTE COURANTE\n===========================\n")
        sys.stderr.write(ligne_sep + "\n")
        for j in range(TAILLE_CARTE):
            sys.stderr.write("\n|")
            for i in range(TAILLE_CARTE):
                poids_courant = self.sommets[Coordonnee(i,j)].poids
                sys.stderr.write(str(poids_courant).rjust(largeur) + " | ")
            sys.stderr.write("\n" + ligne_sep + "\n\n")
