#!/usr/bin/env python3

import sys
from coordonnee import Coordonnee
from environnement import Environnement

PERTE_MORTELLE = float("inf")
GAIN_OR = 10**100
COUT_FLECHE = 10**50

if len(sys.argv) != 2:
    #print("Utilisation: " + sys.argv[0] + " carte.txt")
    exit(-1)

puits = []
wumpus = []
poids = []
carte_poids = []
pos_col = -1
OR_col = -1
with open(sys.argv[1], "r") as file:
    for line in file:
        row_puits = []
        row_wumpus = []
        row_poids = []
        for c in line:
            #print("c = ", c)
            if c == '\n':
                break
            if c == '.':
                if pos_col != -1:
                    print("Erreur de format de fichier. Il ne peut y avoir qu'une seule position de départ.")
                    exit(-1)
                row_puits.append(False)
                row_wumpus.append(False)
                row_poids.append(0)
                pos_col = len(row_puits) - 1
                pos_line = len(puits)
            elif c == 'O':
                if OR_col != -1:
                    print("Erreur de format de fichier. Il ne peut y avoir qu'un seul lingot d'or.")
                    exit(-1)
                row_puits.append(False)
                row_wumpus.append(False)
                row_poids.append(0)
                OR_col = len(row_puits) - 1
                OR_line = len(puits)
            elif c == 'W':
                row_wumpus.append(True)
                row_puits.append(False)
                row_poids.append(0)
            elif c == 'P':
                row_puits.append(True)
                row_wumpus.append(False)
                row_poids.append(0)
            elif c >= '0' and c <= '9':
                row_puits.append(False)
                row_wumpus.append(False)
                row_poids.append(int(c))
            else:
                print("Erreur format fichier. Le caractère '" + c + "' non reconnu.")
                exit(-1)
        puits.append(row_puits)
        wumpus.append(row_wumpus)
        poids.append(row_poids)

   # print(poids)
    #print(wumpus)
    #print(puits)

    if pos_col == -1:
        print("Erreur format fichier. Position de l'agent manquante.")
        exit(-1)
    if OR_col == -1:
        print("Erreur format fichier. Position de l'or manquante.")
        exit(-1)

# Afficher la carte sur stderr
sys.stderr.write("carte:\n")


for j in range(len(puits)):
    ligne_poids = []
    for i in range(len(puits[j])):
        if puits[j][i]:
            ligne_poids.append(PERTE_MORTELLE)
            #carte_poids[j][i] = PERTE_MORTELLE
            sys.stderr.write("P")
        elif wumpus[j][i]:
            ligne_poids.append(PERTE_MORTELLE)
            #carte_poids[j][i] = PERTE_MORTELLE
            sys.stderr.write("W")
        else:
            ligne_poids.append(poids[j][i])
            #carte_poids[j][i] = poids[j][i]
            sys.stderr.write(f"{poids[j][i]}")
    carte_poids.append(ligne_poids)
    sys.stderr.write("\n")

#print(carte_poids)
#print(poids)
sys.stderr.write("OR: (line " + str(OR_line) + ", col " + str(OR_col) + ")\n")
sys.stderr.write("Position: (line " + str(pos_line) + ", col " + str(pos_col) + ")\n")

# TODO: trouver la meilleur suite d'action a faire

env = Environnement(carte_poids, puits, wumpus, poids, OR_line, OR_col, pos_line, pos_col)

path1 = env.Resoudre_A_star()
env.debuter_retour_case_depart()
path2 = env.Resoudre_A_star()
path = path1 + path2

for a in path:
    sys.stdout.write(a + "\n")   # une action par ligne
    sys.stdout.flush()           # OBLIGATOIRE