plainte_insert_schema = {
    "type": "object",
    "required": ["etablissement", "adresse", "ville", "date_visite",
                 "nom_client", "prenom_client", "description"],
    "properties": {
        "etablissement": {
            "type": "string"
        },
        "adresse": {
            "type": "string"
        },
        "ville": {
            "type": "string"
        },
        "date_visite": {
            "type": "string"
        },
        "nom_client": {
            "type": "string"
        },
        "prenom_client": {
            "type": "string"
        },
        "description": {
            "type": "string"
        }
    },
    "additionalProperties": False
}

utilisateur_insert_schema = {
    "type": "object",
    "required": ["nom_complet", "email", "liste_etablissements", "password"],
    "properties": {
        "nom_complet": {
            "type": "string"
        },
        "email": {
            "type": "string"
        },
        "liste_etablissements": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "password": {
            "type": "string"
        }
    },
    "additionalProperties": False
}
