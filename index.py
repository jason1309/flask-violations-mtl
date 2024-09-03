from flask import Flask, render_template, g, redirect, request
from flask import url_for, jsonify, make_response, Response
from .database import Database
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import urllib.parse
from .violation import Violation
import xml.etree.ElementTree as ET
import csv
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
import json
from .schema import plainte_insert_schema
from .plainte import Plainte
from .utilisateur import Utilisateur
from .schema import utilisateur_insert_schema


def update_database():
    print("Mise à jour de la base de données")
    subprocess.run(["python3", "update_database.py"])


scheduler = BackgroundScheduler(timezone="Canada/Eastern")
scheduler.add_job(update_database, 'interval', days=1,
                  start_date='2023-03-31 00:00:00')
scheduler.start()

app = Flask(__name__, static_url_path="", static_folder="static")
schema = JsonSchema(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(JsonValidationError)
def validation_error(e):
    erreurs = [validation_error.message for validation_error in e.errors]
    return jsonify({'erreur': e.message, 'erreurs': erreurs}), 400


@app.route('/')
def index():
    return render_template('index.html', titre="Contrevenants - Montréal")


@app.route('/plainte')
def plainte():
    return render_template("plainte.html", titre="Formulaire de plainte")


@app.route('/confirmation/')
def confirmation():
    return render_template("confirmation.html", titre="Confirmation plainte")


@app.route('/doc')
def doc():
    return render_template('doc.html')


@app.route('/search', methods=['POST'])
def search():
    la_recherche = request.form['larecherche']
    return redirect(url_for("recherche", recherche=la_recherche))


@app.route('/send', methods=['POST'])
def send():
    return redirect(url_for("confirmation"))


@app.route('/recherche/<recherche>')
def recherche(recherche):
    violations_trouve = get_db().rechercher_violations(recherche)
    return render_template('recherche.html', violations=violations_trouve,
                           titre="Recherche")


@app.route('/api/contrevenants', methods=['GET'])
def contrevenants():
    date_debut = request.args.get('du')
    date_fin = request.args.get('au')

    contrevenants_trouve = get_db().get_contrevenants_date(date_debut,
                                                           date_fin)

    liste_contrevenants = [{"nom_etablissement": contrevenant["etablissement"],
                            "_id": contrevenant["id"]}
                           for contrevenant in contrevenants_trouve]

    return jsonify(liste_contrevenants), 200


@app.route('/api/contrevenants-noms', methods=['GET'])
def get_contrevenants_noms():
    liste_noms = get_db().get_all_contrevenants_noms()

    return jsonify(liste_noms), 200


@app.route('/api/contrevenant/<nom>', methods=['GET'])
def get_contrevenant(nom):
    nom = nom.replace('%20', ' ').replace('-', '/')
    print(nom)
    violations = get_db().get_violations_etablissement(nom)

    return jsonify([violation.asDictionary() for violation in violations]), 200


@app.route('/api/contrevenants-infractions', methods=['GET'])
def get_contrevenants():
    contrevenants = get_db().get_all_contrevenants_nb_infractions()

    return jsonify(contrevenants), 200


@app.route('/api/contrevenants-infractions-xml', methods=['GET'])
def get_contrevants_xml():
    contrevenants = get_db().get_all_contrevenants_nb_infractions()

    root = ET.Element("contrevenants")
    for cont in contrevenants:
        e_contrevenant = ET.SubElement(root, "contrevenant")
        ET.SubElement(e_contrevenant,
                      "nom_etablissement").text = cont["nom_etablissement"]
        ET.SubElement(e_contrevenant, "nb_infractions").text = str(
            cont["nb_infractions"])
        xml = ET.tostring(root, encoding="UTF-8")

    return Response(xml, mimetype="text/xml"), 200


@app.route('/api/contrevenants-infractions-csv', methods=['GET'])
def get_contrevenants_csv():
    contrevenants = get_db().get_all_contrevenants_nb_infractions()

    csv = ""
    entetes = contrevenants[0].keys()
    les_contrevenants = [[str(contrevenant.get(entete, ""))
                          for entete in entetes]
                         for contrevenant in contrevenants]
    csv = ",".join(entetes) + "\n" + "\n".join(
        [",".join(un_contrevenant) for un_contrevenant in les_contrevenants])

    reponse = make_response(csv)
    reponse.headers["Content-Type"] = "text/plain; charset=utf8"
    reponse.headers["Content-Disposition"] = "inline"

    return reponse, 200


@app.route('/api/plainte', methods=['POST'])
@schema.validate(plainte_insert_schema)
def post_plainte():
    data = request.get_json()
    plainte = Plainte(None, data["etablissement"], data["adresse"],
                      data["ville"], data["date_visite"],
                      data["nom_client"], data["prenom_client"],
                      data["description"])
    plainte = get_db().add_plainte(plainte)
    return jsonify(plainte.asDictionary()), 201


@app.route('/api/plainte/<id>', methods=['DELETE'])
def delete_plainte(id):
    plainte = get_db().get_plainte(id)

    if plainte is None:
        return "", 404
    else:
        get_db().delete_plainte(plainte)
        return "", 200


@app.route('/api/utilisateur', methods=['POST'])
@schema.validate(utilisateur_insert_schema)
def add_user():
    data = request.get_json()
    utilisateur = Utilisateur(None, data["nom_complet"],
                              data["email"], data["liste_etablissements"],
                              data["password"])

    utilisateur = get_db().add_user(utilisateur)
    return jsonify(utilisateur.asDictionary()), 201


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
