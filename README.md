# Let's Roque : Logiciel de Gestion de Tournois d'Échecs
Projet Openclassrooms : P4_Programme_logiciel_Python
Développez un programme logiciel en Python

## Présentation du projet
Ce projet est une application de gestion de tournois d'échecs développée en Python en utilisant le modèle MVC (Modèle-Vue-Contrôleur).
Elle permet de :
Créer et gérer des tournois (ajout de joueurs, suivi des tours et des matchs).
Gérer les joueurs (ajout et affichage des joueurs inscrits).
Apparier les joueurs pour les matchs.
Afficher les résultats des matchs et des classements.
Enregistrer et restaurer des données via un système de sauvegarde JSON.

L'application fonctionne entièrement en console (CLI), avec une interface interactive utilisant Rich et Questionary pour améliorer l'expérience utilisateur.

# Installation et Prérequis

## Prérequis
Python 3.10+ (Vérifiez votre version avec `python --version`)
Il faut que je gestionnaire de paquets python soit installé (pip)

## Installation
Clonez le projet

```
git clone https://github.com/MagNott/P4_Programme_logiciel_Python.git
cd P4_Programme_logiciel_Python
```

Installez les dépendances
`pip install -r requirements.txt`


## Mise en place de l'environnement et activation de l'environnement
```
python3 -m venv env
source env/bin/activate
```

# Utilisation
Lancez l’application avec la commande suivante :
`python main.py`

L’interface vous proposera un menu interactif pour gérer les tournois et les joueurs.

## Fonctionnalités principales
Créer un tournoi	Ajoute un nouveau tournoi en spécifiant son nom, lieu, dates, nombre de tours.
Lister les tournois	Affiche les tournois enregistrés.
Inscrire des joueurs	Ajoute des joueurs à un tournoi existant.
Créer des tours et matchs	Génère automatiquement les matchs du premier tour, puis les suivants selon le système suisse.
Saisir les résultats	Permet d'entrer les résultats des matchs en cours.
Sauvegarde automatique	Sauvegarde les données des joueurs et tournois après chaque action.
Restaurer une sauvegarde	Permet de restaurer un état précédent des données.

# Architecture du Projet
Le projet suit une architecture Modèle-Vue-Contrôleur (MVC) :

```
P4-PROGRAMME_LOGICIEL_PYTON/
│
├── models/                  # Modèles de données
│   ├── joueur.py               # Gestion des joueurs
│   ├── tournoi.py              # Gestion des tournois
│   ├── tour.py                 # Gestion des tours
│   ├── match.py                # Gestion des matchs
│   ├── gestionnaire_persistance.py  # Sauvegarde et chargement des données (TinyDB)
│
├── views/                   # Affichage et interface utilisateur
│   ├── vue.py                  # Classe de base des vues
│   ├── joueur_vue.py           # Vue dédiée aux joueurs
│   ├── tournoi_vue.py          # Vue dédiée aux tournois
│   ├── tour_vue.py             # Vue dédiée aux tours
│   ├── sauvegarde_vue.py       # Vue dédiée aux sauvegardes
│
├── controllers/             # Logique métier et interaction entre modèles et vues
│   ├── joueur_controleur.py    # Gestion des joueurs
│   ├── tournoi_controleur.py   # Gestion des tournois
│   ├── tour_controleur.py      # Gestion des tours
│   ├── sauvegarde_controleur.py # Gestion des sauvegardes/restaurations
│
├── data/                    # Stockage des données JSON
│   ├── players/             # Fichiers des joueurs
│   ├── tournaments/         # Fichiers des tournois
│   ├── sauvegarde/          # Dossiers de sauvegarde
│
├── sauvegarde/          # Dossiers de sauvegarde
│
├── main.py                     # Point d’entrée principal de l'application
└── requirements.txt             # Dépendances Python
```

# Sauvegarde et Restauration
L’application enregistre automatiquement les données au format JSON après chaque modification.
Une option de sauvegarde permet de sauvegarder l'intégralité des données à un instant T
Une option permet également de restaurer une sauvegarde précédente.

## Emplacement des données
Joueurs : data/players/
Tournois : data/tournaments/

## Emplacement des sauvegardes
Sauvegardes complètes : data/sauvegarde/

## Restaurer une sauvegarde
Lancer l'application : `python main.py`
Aller dans "Restaurer une sauvegarde"
Sélectionner une sauvegarde
Confirmer la restauration
**Attention** : Restaurer une sauvegarde écrasera les données actuelles.

# Technologies Utilisées
- Python 3.10+
- TinyDB (Base de données JSON embarquée)
- Rich (Affichage amélioré en console)
- Questionary (Interface interactive en ligne de commande)
- Pathlib (Gestion des fichiers et répertoires)

# Qualité de code 

## Convention de nommage
Utilisation de la notation hongroise
- Les paramétres de fonctions sont préfixés avec p_
- Les objets sont préfixés avec o_
- Les entiers sont préfixés avec i_
- Les chaines de caractères sont préfixés avec s_
- Les listes sont préfxées avec l_
- Les dictionnaires sont préfixés avec d_

## Espacement du code 
Pour faciliter la lecture dans les classes, des commentaires vides ont été ajoutés avant chaque fonction

## Configuration de l’analyse de code 
**Flake8 : vérification de la PEP 8**
Le projet utilise Flake8 pour vérifier la conformité du code aux normes PEP 8, avec une limite de 119 caractères par ligne définie dans le fichier setup.cfg.

Pour lancer le programme :
`python main.py`

Pour régénérer le rapport Flake8 :
`flake8 --format=html --htmldir=flake8_rapport`

**Black : formateur automatique**
Le projet utilise Black pour formater automatiquement le code avec la même limite de 119 caractères par ligne.

Pour formater le code avec Black :
`black .`

# Note pour l'évaluateur
Le projet sur main ne contient aucun document JSON pour la base de données, afin de faciliter l'évaluation, une branche contenant le projet fini et un jeu de données a été créé :
https://github.com/MagNott/P4_Programme_logiciel_Python/tree/projet_fini_jeux_de_donnees

