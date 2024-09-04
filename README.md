# Projet Infractions Restaurant Montréal
Développement d'une application web visant à recueillir des données ouvertes de la ville de Montréal concernant les établissements ayant reçu des constats d'infraction lors des inspections alimentaires. L'objectif est d'exploiter ces informations pour fournir divers services aux utilisateurs

## Fonctionnalités

- Importation et traitement des données depuis des fichiers CSV disponible sur le site de la ville de Montréal.
- Recherche d'infractions par mots-clé (nom, rue, etc.) via une barre de recherche.
- Recherche d'infractions par intervalle de dates.
- Filtrage par liste déroulante permettant d'afficher les différentes infractions d'un restaurant.
- Soumission de plaintes avec validation des entrées en JavaScript et côté serveur.

## Technologies Utilisées

- **Backend** : Flask, Python
- **Frontend** : HTML, CSS, Bootstrap, JavaScript
- **Base de Données** : SQLite3

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/jason1309/flask-violations-mtl.git

   ```
2. **Accéder au répertoire du projet**
    ```bash
    cd flask-violations-mtl
    ```

3. **Créer un environnement virtuel, l'activer et installer les dépendances**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4. **Démarrer l'application**
    ```bash
    make run
    ```

Pour accéder à l'application, allez sur http://127.0.0.1:5000
