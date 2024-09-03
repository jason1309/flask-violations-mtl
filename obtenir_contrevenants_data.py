import csv
import requests
import sqlite3
from datetime import datetime

url = ("https://data.montreal.ca/dataset/"
       "05a9e718-6810-4e73-8bb9-5955efeb91a0/"
       "resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/"
       "download/violations.csv")

conn = sqlite3.connect('db/data.db')

cursor = conn.cursor()

reponse = requests.get(url)

csv_text = reponse.content.decode('utf-8')
csv_reader = csv.reader(csv_text.splitlines(), delimiter=',')

next(csv_reader)

for row in csv_reader:
    (id_poursuite, business_id, date_str,
     description, adresse, date_jugement_str,
     etablissement, montant, proprietaire, ville,
     statut, date_statut_str, categorie) = row

    date = datetime.strptime(date_str, "%Y%m%d").date()
    date_formate = date.strftime("%Y-%m-%d")

    date_jugement = datetime.strptime(date_jugement_str, "%Y%m%d").date()
    date_jugement_formate = date_jugement.strftime("%Y-%m-%d")

    date_statut = datetime.strptime(date_statut_str, "%Y%m%d").date()
    date_statut_formate = date_statut.strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO violations (id_poursuite, business_id, date, "
        "description, adresse, date_jugement, etablissement, "
        "montant, proprietaire, ville, statut, date_statut, "
        "categorie) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (id_poursuite,
         business_id,
         date_formate,
         description,
         adresse,
         date_jugement_formate,
         etablissement,
         montant,
         proprietaire,
         ville,
         statut,
         date_statut_formate,
         categorie))

conn.commit()
conn.close()
