class Utilisateur:
    def __init__(self, id, nom_complet, email,
                 liste_etablissements, password):

        self.id = id
        self.nom_complet = nom_complet
        self.email = email
        self.liste_etablissements = liste_etablissements
        self.password = password

    def asDictionary(self):
        return {"id": self.id,
                "nom_complet": self.nom_complet,
                "email": self.email,
                "liste_etablissements": self.liste_etablissements,
                "password": self.password}
