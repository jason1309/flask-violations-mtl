DROP TABLE IF EXISTS violations;
DROP TABLE IF EXISTS plainte;
DROP TABLE IF EXISTS utilisateur;

create table violations (
    id integer primary key,
    id_poursuite varchar(10),
    business_id varchar(10),
    date text,
    description varchar(500),
    adresse varchar(100),
    date_jugement text,
    etablissement varchar(50),
    montant varchar(10),
    proprietaire varchar(50),
    ville varchar(20),
    statut varchar(20),
    date_statut text,
    categorie varchar(20)
);

create table plainte(
    id integer primary key,
    nom_etablissement varchar(50),
    adresse varchar(50),
    ville varchar(20),
    date_visite text,
    nom_client varchar(20),
    prenom_client varchar(20),
    description varchar(500)
);

create table utilisateur(
    id integer primary key,
    nom_complet varchar(50),
    email varchar(30),
    liste_etablissements varchar(200),
    password varchar(20)
);