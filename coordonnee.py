"""
INF4230 - INTELLIGENCE ARTIFICIELLE
UQAM | Faculté des sciences | Département d'informatique
TP1 : Jeu du Wumpus
ETUDIANT : DEGNI KAIKOU LOIC DEGK24059500
Module : coordonnee.py
"""

class Coordonnee:
    def __init__(self,i=0, j=0, poids = None):
        self.i = i          # position i
        self.j = j          # position j
        self.poids = poids  # Poids de la position
        
    # Constructeur par copie (équivalent)
    @classmethod
    def copie(cls, autre):
        return cls(autre.i, autre.j)
    
    # operator ==
    def __eq__(self, autre):
        if not isinstance(autre, Coordonnee):
            return NotImplemented
        return (self.i == autre.i and self.j == autre.j)
    
    # Hash compatible avec __eq__
    def __hash__(self):
        return hash((self.i, self.j))
    
    # Ordre (utile pour tri / debug)
    def __lt__(self, other):
        return (self.i, self.j) < (other.i, other.j)
    
    #print(obj)
    def __str__(self):
        return f"({self.i}, {self.j})"

    #pour dict, list, debug, console
    def __repr__(self):
        return f"Coordonnee(i={self.i}, j={self.j}, poids={self.poids})"