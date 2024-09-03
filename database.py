import sqlite3
from .violation import Violation
from .plainte import Plainte


def _build_violation(result_set_item):
    violation = {}
    violation["id"] = result_set_item[0]
    violation["id_poursuite"] = result_set_item[1]
    violation["business_id"] = result_set_item[2]
    violation["date"] = result_set_item[3]
    violation["description"] = result_set_item[4]
    violation["adresse"] = result_set_item[5]
    violation["date_jugement"] = result_set_item[6]
    violation["etablissement"] = result_set_item[7]
    violation["montant"] = result_set_item[8]
    violation["proprietaire"] = result_set_item[9]
    violation["ville"] = result_set_item[10]
    violation["statut"] = result_set_item[11]
    violation["date_statut"] = result_set_item[12]
    violation["categorie"] = result_set_item[13]
    return violation


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/data.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def rechercher_violations(self, recherche):
        cursor = self.get_connection().cursor()
        query = ("SELECT id, id_poursuite, business_id, date, "
                 "description, adresse, date_jugement, etablissement, "
                 "montant, proprietaire, ville, statut, date_statut, "
                 "categorie "
                 "FROM violations "
                 "WHERE etablissement LIKE ? OR proprietaire LIKE ? "
                 "OR adresse LIKE ?")
        cursor.execute(query, ('%'+recherche+'%', '%'+recherche+'%',
                               '%'+recherche+'%'))

        violations_trouve = cursor.fetchall()
        return [_build_violation(item) for item in violations_trouve]

    def get_contrevenants_date(self, date_debut, date_fin):
        cursor = self.get_connection().cursor()
        query = ("SELECT id, id_poursuite, business_id, date, "
                 "description, adresse, date_jugement, "
                 "etablissement, montant, proprietaire, ville, "
                 "statut, date_statut, categorie "
                 "FROM violations "
                 "WHERE date BETWEEN ? AND ?")
        cursor.execute(query, (date_debut, date_fin))
        contrevenants = cursor.fetchall()
        return [_build_violation(item) for item in contrevenants]

    def get_violations_etablissement(self, nom_etablissement):
        cursor = self.get_connection().cursor()
        query = ("SELECT id, id_poursuite, business_id, "
                 "date, description, adresse, date_jugement, "
                 "etablissement, montant, proprietaire, ville, "
                 "statut, date_statut, categorie "
                 "FROM violations "
                 "WHERE etablissement = ?")
        cursor.execute(query, (nom_etablissement,))
        violations = cursor.fetchall()

        return [Violation(une_violation[0], une_violation[1], une_violation[2],
                          une_violation[3], une_violation[4], une_violation[5],
                          une_violation[6], une_violation[7], une_violation[8],
                          une_violation[9], une_violation[10],
                          une_violation[11], une_violation[12],
                          une_violation[13]) for une_violation in violations]

    def get_all_contrevenants_nb_infractions(self):
        cursor = self.get_connection().cursor()
        query = ("SELECT etablissement, COUNT(*) AS nb_infractions "
                 "FROM violations "
                 "GROUP BY etablissement "
                 "ORDER BY nb_infractions DESC")
        cursor.execute(query)
        all_contrevenants = cursor.fetchall()
        liste_contrevenants = [{"nom_etablissement": contrevenant[0],
                                "nb_infractions": contrevenant[1]}
                               for contrevenant in all_contrevenants]
        return liste_contrevenants

    def get_all_contrevenants_noms(self):
        cursor = self.get_connection().cursor()
        query = ("SELECT etablissement FROM violations ")
        cursor.execute(query)
        data = cursor.fetchall()
        liste_nom_contrevenants = [{"nom_etablissement": contrevenant[0]}
                                   for contrevenant in data]
        return liste_nom_contrevenants

    def add_plainte(self, plainte):
        connection = self.get_connection()
        query = ("INSERT into plainte(nom_etablissement, adresse, ville, "
                 "date_visite, nom_client, prenom_client, description) "
                 "VALUES(?, ?, ?, ?, ?, ?, ?)")
        connection.execute(query, (plainte.nom_etablissement, plainte.adresse,
                                   plainte.ville, plainte.date_visite,
                                   plainte.nom_client, plainte.prenom_client,
                                   plainte.description))
        connection.commit()
        cursor = connection.cursor()
        cursor.execute("select last_insert_rowid()")
        resultat = cursor.fetchall()
        plainte.id = resultat[0][0]

        return plainte

    def delete_plainte(self, plainte):
        connection = self.get_connection()
        connection.execute("DELETE FROM plainte WHERE rowid = ?",
                           (plainte.id,))
        connection.commit()

    def get_plainte(self, id_plainte):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT rowid, nom_etablissement, adresse, ville, "
                       "date_visite, nom_client, prenom_client, description "
                       "FROM plainte "
                       "WHERE rowid = ?", (id_plainte,))
        plaintes = cursor.fetchall()

        if len(plaintes) == 0:
            return None
        else:
            plainte = plaintes[0]
            return Plainte(plainte[0], plainte[1], plainte[2], plainte[3],
                           plainte[4], plainte[5], plainte[6], plainte[7])

    def add_user(self, utilisateur):
        connection = self.get_connection()
        liste_etablissements = ",".join(utilisateur.liste_etablissements)
        connection.execute("INSERT INTO utilisateur(nom_complet, email, "
                           "liste_etablissements, password) "
                           "VALUES (?, ?, ?, ?)",
                           (utilisateur.nom_complet, utilisateur.email,
                            liste_etablissements, utilisateur.password))
        connection.commit()
        cursor = connection.cursor()
        cursor.execute("select last_insert_rowid()")
        resultat = cursor.fetchall()
        utilisateur.id = resultat[0][0]

        return utilisateur
