# TP1 : Jeu du Wumpus

**Cours :** INF4230 – Intelligence Artificielle  
**Université :** UQAM, Faculté des sciences, Département d'informatique  
**Auteur :** DEGNI KAIKOU LOIC (DEGK24059500)

---

## Description

Ce projet implémente le **Jeu du Wumpus** dans un environnement carré `n × n`. L'objectif de l'agent est de :

- Explorer la carte.
- Éviter les puits et les Wumpus.
- Récupérer l'or et revenir à la case de départ.


## Contenu du dépôt

- `main.py` : Code de l'agent Python.
- `environnement.py` : Gestion de l'environnement Wumpus.
- `staticmap.py` : Structure de données du graphe.
- `coordonnee.py` : Classe pour représenter les coordonnées d'une case.

---

## Instructions d'utilisation

1. Placer tous les fichiers dans le même dossier.
2. Lancer le script Python avec une carte spécifique :  
```bash
python3 main.py carte.txt
