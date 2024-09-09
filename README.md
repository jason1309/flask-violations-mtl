# Projet Infractions Restaurant Montréal
Développement d'une application web visant à recueillir des données ouvertes de la ville de Montréal concernant les établissements ayant reçu des constats d'infraction lors des inspections alimentaires. L'objectif est d'exploiter ces informations pour fournir divers services aux utilisateurs

Projet réalisé au cours de la session d'hiver 2023 pour le cours INF5190 - Programmation web avancée à l'UQAM.

## Démonstration
https://github.com/user-attachments/assets/1211f791-faff-4c1c-8796-e32096937558

## Table des matières
- [Fonctionnalités](#fonctionnalités)
- [Technologies Utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Contributeur](#contributeur)

## Fonctionnalités

- Importation et traitement des données depuis des fichiers CSV disponible sur le site de la ville de Montréal.
- Recherche d'infractions par mots-clé (nom, rue, etc.) via une barre de recherche.
- Recherche d'infractions par intervalle de dates.
- Filtrage par liste déroulante permettant d'afficher les différentes infractions d'un restaurant.
- Soumission de plaintes avec validation des entrées en JavaScript et côté serveur.
- BackgroundScheduler permettant une mise à jour de la base de donnée à chaque intervalle de 24 heures.

## Technologies Utilisées

- **Backend** : Flask, Python
- **Frontend** : HTML, CSS, Bootstrap, JavaScript
- **Base de Données** : SQLite3

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/jason1309/flask-violations-mtl.git
   cd flask-violations-mtl
   ```

2. **Créer un environnement virtuel, l'activer et installer les dépendances**
   ##### macOS et Linux
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
   ##### Windows
   ```bash
   python -m venv venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Démarrer l'application**
    ```bash
    make run
    ```

Pour accéder à l'application, allez sur http://127.0.0.1:5000.

## Contributeur
- [Gagné, Jason](https://www.linkedin.com/in/jason-gagn%C3%A9-839032246/)
