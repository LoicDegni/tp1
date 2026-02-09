from typing import Dict, TypeVar, Generic
from coordonnee import Coordonnee


S = TypeVar("S")  # type des sommets
A = TypeVar("A")  # type des poids (ou étiquettes)


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
