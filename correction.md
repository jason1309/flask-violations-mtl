# Correction projet de session
# Nom, Prenom : Gagné, Jason
# Code permanent : GAGJ16059700

# Point A1:
Tout d'abord, vous pouvez vérifier que la base de données nommées `data.db`, située dans le répertoire db, est bien vide.
Cette base de donnée est crée grâce au script de création table nommée db.sql comme mentionné dans l'énoncé.

Pour tester ce point, il suffit d'aller a la racine du projet.
Ensuite, utiliser le script `obtenir_contrevenants_data.py` pour remplir la base de données.

```
python3 obtenir_contrevenants_data.py
```
Par la suite, pour vérifier qu'elle soit bien remplit, déplacez vous dans le répertoire db.
Utilisez :

```
sqlite3 data.db
```

Une fois dans sqlite3, tapez:

```
select * from violations;
```

Et vous pouvez observer que la base de données est bel et bien remplis.

# Point A2:
Pour ce point, vous devez aller sur la page d'accueil, nommée `index.html`.
Il y a une barre de recherche située sous RECHERCHER LES CONTREVENANTS DE MONTRÉAL.
Tapez subway, par exemple, dans cette barre de recherche et cliquer sur Rechercher.
Les différentes informations sur les contrevenants vont apparaitre sur une nouvelle page.

# Point A3:
Pour tester ce point, vous pouvez aller dans le fichier `index.py` et modifier l'heure du scheduler.
Donc, au début du code, vous allez voir en dessous de la fonction `update_database():`

```
scheduler = BackgroundScheduler(timezone="Canada/Eastern")
scheduler.add_job(update_database, 'interval', days=1,
                  start_date='2023-03-31 00:00:00')
scheduler.start()
```
Vous pouvez changer l'heure après start_date pour tester. 
Par exemple, s'il est 14:22:00, changez l'heure pour 14:22:20.
Le message "Mise à jour de la base de données" va s'afficher ce qui démontre que le BackgroundScheduler fonctionne. 

Si vous voulez tester qu'il met bien à jour la base de données, vous pouvez supprimer la dernière donnée de la base de donnée avant d'effectuer le changement de l'heure. Ensuite, lorsque le BackgroundScheduler s'activera, retournez voir les données de la base de données et elle seront synchronisé à nouveau.

# Point A4:
Pour ce point, vous pouvez ajouter à l'URL les arguments.
Par exemple : `localhost:5000/api/contrevenants?du=2020-05-08&au=2022-05-15`
Vous obtiendrez tous les contrevenants entre ces dates, en format JSON.
Dans mon cas, je n'ai retourné que le nom des établissements et leur ID, puisque ce sont les seules données que j'avais besoin pour faire le tableau du point A5.
J'ai nommé la route avec /api/ puisque c'est un service REST, malgré que l'exemple ne contenait pas /api/.

Pour vérifier la documentation du service, vous pouvez aller à la route /doc.

# Point A5:
Pour le point A5, il vous suffit de saisir deux dates dans la section Rechercher par date situé a l'accueil et sous la grosse barre de recherche.
Ensuite, cliquer sur Recherche et le tableau va apparaitre avec les noms des contrevenants entre ces dates et leur nombre de violations. La page ne recharge pas puisque c'est une requête Ajax.

Pour vérifier la documentation du service, vous pouvez aller à la route /doc.

# Point A6:
Pour A6, une liste déroulante se situe sous la section rechercher par date. Elle contient le nom des établissements ayant commis au moins une violation. Lorsque vous choisissez un contrevenant dans la liste, leurs infractions avec les informations sur ces dernières apparaient plus bas. La page ne recharge pas puisque c'est une requête Ajax.
Je n'ai affiché que les informations que je jugeais pertinente (donc pas les id par exemple).

Pour vérifier la documentation du service, vous pouvez aller à la route /doc.

# Point C1:
Pour tester C1, aller sur la route `http://localhost:5000/api/contrevenants-infractions`.
Les établissements ainsi que leur nombre d'infractions connue seront affichés en json. 

Pour vérifier la documentation du service, vous pouvez aller à la route /doc.

# Point C2:
Pour tester C2, aller sur la route `http://localhost:5000/api/contrevenants-infractions-xml`.
Les établissements ainsi que leur nombre d'infractions connue seront affichés en xml. 

Pour vérifier la documentation du service, vous pouvez aller à la route /doc.

# Point C3:
Pour tester C3, aller sur la route `http://localhost:5000/api/contrevenants-infractions-csv`.
Les établissements ainsi que leur nombre d'infractions connue seront affichés en csv. 

Pour vérifier la documentation du service, vous pouvez aller à la route /doc.

# Point D1:
Pour tester que le formulaire de plainte fonctionne bien, vous pouvez cliquer sur la page plainte sur le menu a l'accueil ou aller directement sur `http://localhost:5000/plainte`.
Remplissez les champs du formulaire. 
Par la suite, aller dans le répertoire db et ouvrez la base de données pour vérifier que la plainte que vous venez d'effectuer s'y retrouve.

```
sqlite3 data.db
select * from plainte;
```
Votre plainte devrait y être.

Si vous devez tester que le json-schema fonctionne bien, ouvrez le ficher script.js.
Dans la fonction `creerPlainte()`, changez ce bout de code:
```
    return {
      etablissement: plainteEtablissement,
      adresse: plainteAdresse,
      ville: plainteVille,
      date_visite: plainteDate,
      nom_client: plainteNom,
      prenom_client: plaintePrenom,
      description: plainteDescription
    };
```
Par celui-ci:
```
    return {
      etablissement: plainteEtablissement,
      adresse: plainteAdresse,
      ville: plainteVille,
      date_visite: plainteDate,
      nom_client: plainteNom,
      prenom_client: plaintePrenom,
      /*description: plainteDescription*/
    };
```
Recharger la page de plainte. Remplissez le formulaire a nouveau.
Vous allez apercevoir le code 400, sur l'invite de commande, indiquant qu'il y a eu une erreur puisque les données envoyées ne respectent pas le json-schema.
Vous pouvez retourner voir dans la BD et la plainte ne sera pas la.
Cette erreur ne devrait arriver que si l'utilisateur modifie le code, puisque je fais les vérifications nécessaire.
C'est pourquoi je renvoie la page de confirmation, avec POST-REDIRECT-GET, tout de même.

Pour vérifier la documentation du service, vous pouvez aller à la route /doc.

# Point D2:
Pour tester ce point, sur un invite de commande, j'ai ouvert mon app Flask.
Sur un autre invite de commande, j'ai entré la commande :
```
curl -X DELETE http://localhost:5000/api/plainte/1
```
Ensuite, sur l'invite de commande de votre serveur, vous pouvez voir la requete DELETE suivi de la route et du code, soit 404 si la plainte n'existait pas, ou 200 si la plainte s'est bien supprimé.

Je ne sais pas si c'est la meilleure façon pour le tester, mais c'est comme cela que j'ai fait.
Assurez vous de tester le point D1 en premier pour qu'une plainte avec l'identifiant 1 existe (celle que vous avez créée).

Pour vérifier la documentation du service, vous pouvez aller à la route /doc.

# Point E1:
Pour tester ce point, il faut faire comme au point D2 puisque je n'ai pas développé E2.
Donc, sur une invite de commande le serveur doit être ouvert.
Sur un autre invite de commande, il faut entré la commande suivante:

```
curl -X POST -H "Content-Type: application/json" -d '{"nom_complet": "George Clooney", "email": "clooneylooney@exemple.ca", "liste_etablissements": ["Subway", "Basha", "pizza pizza"], "password": "password1234"}' http://localhost:5000/api/utilisateur
```

L'objet est envoyé au service et il est ajouté a la base de donnée.
Vous pouvez aller voir qu'il est bien ajouter a la base de donnée en allant dans le répertoir db.
Ouvrez la db et vérifier avec:

```
sqlite3 data.db
select * from utilisateur;
```

Sur l'invite de commande du serveur, on peut aussi observer le code 201.
Sur celui ou on a effectué la commande curl, l'objet utilisateur est retourné.

Pour vérifier que le json-schema fonctionne bien, on peut enlever le password:
```
curl -X POST -H "Content-Type: application/json" -d '{"nom_complet": "George Clooney", "email": "clooneylooney@exemple.ca", "liste_etablissements": ["Subway", "Basha", "pizza pizza"]}' http://localhost:5000/api/utilisateur
```
Il devrait y avoir le code 400 indiquant une erreur. Sur l'invite de commande ou vous avez entré la commande curl, vous devriez voir l'explication de l'erreur.

Pour vérifier la documentation du service, vous pouvez aller à la route /doc.

# Point d'xp: 110/100