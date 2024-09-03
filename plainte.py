class Plainte:
    def __init__(self, id, nom_etablissement,
                 adresse, ville, date_visite,
                 nom_client, prenom_client,
                 description):

        self.id = id
        self.nom_etablissement = nom_etablissement
        self.adresse = adresse
        self.ville = ville
        self.date_visite = date_visite
        self.nom_client = nom_client
        self.prenom_client = prenom_client
        self.description = description

    def asDictionary(self):
        return {"id": self.id,
                "nom_etablissement": self.nom_etablissement,
                "adresse": self.adresse,
                "ville": self.ville,
                "date_visite": self.date_visite,
                "nom_client": self.nom_client,
                "prenom_client": self.prenom_client,
                "description": self.description}
