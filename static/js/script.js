/**
 * Permet de rechercher les contrevenants entre deux dates.
 */

function rechercherParDate(event) {
    event.preventDefault();
    var sectionRechercheDate = document.getElementById("recherche-date");
    var dateDebut = document.getElementById("date-debut").value;
    var dateFin = document.getElementById("date-fin").value;
    var champNom = document.getElementById("champ-nom-etablissement");
    var aucunResultat = document.getElementById("no-result");

    if (verificationDateAccueil(dateDebut, dateFin)) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    gererReponse(JSON.parse(xhr.responseText), aucunResultat, sectionRechercheDate, champNom);
                }
            }
        };

        xhr.open("GET", "/api/contrevenants?du=" + dateDebut + "&au=" + dateFin, true);
        xhr.send();
    }
}


/**
 * Permet de gérer l'affichage suite a la requête HTTP.
 * @param nomsEtablissements - La liste des établissements ayant commis une infraction entre les dates entrées par l'utilisateur.
 * @param aucunResultat - Le message à afficher si aucun contrevenants a effectué une violation entre les dates.
 * @param sectionRechercheDate - La section a afficher, contenant le tableau, s'il y a des résultats.
 * @param champNom - Le tbody du tableau pour insérer chaque contrevenants dans le tableau.
 */
function gererReponse(nomsEtablissements, aucunResultat, sectionRechercheDate, champNom) {
    if (nomsEtablissements.length === 0) {
      aucunResultat.style.display = "flex";
      sectionRechercheDate.style.display = "none";
    } else {
      sectionRechercheDate.style.display = "block";
      aucunResultat.style.display = "none";
      champNom.innerHTML = creerTableau(nomsEtablissements);
    }
}

/**
 * Crée un tableau HTML à partir d'un tableau de noms d'établissements avec le nombre d'infractions
 * pour chaque établissement.
 * @param listeNoms - Tableau des noms des établissements.
 * @returns Le code HTML du tableau créé.
 */
function creerTableau(listeNoms) {
    var retourHtmlTableau = "";
    var compteurInfractions = {};

    for (var i = 0; i < listeNoms.length; i++) {
        var nomEtablissement = listeNoms[i]["nom_etablissement"];
        if (nomEtablissement in compteurInfractions) {
            compteurInfractions[nomEtablissement]++;
        } else {
            compteurInfractions[nomEtablissement] = 1;
        }
    }

    for (var nomEtablissement in compteurInfractions) {
        retourHtmlTableau +=
            "<tr><td>" + nomEtablissement + '</td><td class="nb-infraction">' + compteurInfractions[nomEtablissement] + "</td></tr>";
    }

    return retourHtmlTableau;
}

/**
 * Vérifie si les dates de début et de fin sont valides.
 *
 * @param dateDebut - La date de début à vérifier.
 * @param dateFin - La date de fin à vérifier.
 * @returns  True si les dates sont valides, false sinon.
 */
function verificationDateAccueil(dateDebut, dateFin) {
    var errDate = document.getElementById("err-date");

    if (dateDebut === "" || dateFin === "") {
        errDate.innerHTML = "Veuillez sélectionner des dates valides";
        return false;
    } else {
        errDate.innerHTML = "";
        return true;
    }
}

/**
 * Récupère la liste des noms d'établissements, crée une liste déroulante avec ces noms et l'ajoute à la page HTML.
 */
function creerListeDeroulante() {
    var nomsDejaAffiche = [];
    var listeEtablissement = document.getElementById("liste-etablissements");

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                listeNoms = JSON.parse(xhr.responseText);
                listeNoms.forEach(function (leEtablissement) {
                    if (!nomsDejaAffiche.includes(leEtablissement.nom_etablissement)) {
                        nomsDejaAffiche.push(leEtablissement.nom_etablissement);
                        listeEtablissement.appendChild(
                            new Option(leEtablissement.nom_etablissement, leEtablissement.nom_etablissement)
                        );
                    }
                });
            }
        }
    }
    xhr.open("GET", "/api/contrevenants-noms", true);
    xhr.send()
}

/**
 * Effectue une requête HTTP pour obtenir la liste des violations d'un contrevenant.
 * Affiche les informations sur ces violations dans la section information pour les violations.
 */
function rechercherParListe() {
    var nomEtablissement = document.getElementById("liste-etablissements").value;
    var sectionInfoViolation = document.getElementById("information");
    nomEtablissement = nomEtablissement.replace("/", "-");

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                sectionInfoViolation.innerHTML = afficherInformation(JSON.parse(xhr.responseText));
            }
        }
    };

    xhr.open("GET", "/api/contrevenant/" + nomEtablissement, true);
    xhr.send();
}

/**
 * Renvoie le code HTML des informations sur les violations du contrevenant.
 * @param listeViolation - la liste des violations du contrevenants
 * @returns le code HTML des informations sur les différentes violations
 */
function afficherInformation(listeViolation) {
    var htmlInfo = "";
    var cmpInfraction = 1;

    for (var i = 0; i < listeViolation.length; i++) {
            htmlInfo +=
                "<h2>Infraction #" + cmpInfraction + "</h2>" +
                "<h6>Date: " + listeViolation[i]["date"] + "</h6>" +
                "<p>Description: " + listeViolation[i]["description"] + "</p>" +
                "<p>Adresse: " + listeViolation[i]["adresse"] + "</p>" +
                "<p>Date de jugement: " + listeViolation[i]["date_jugement"] + "</p>" +
                "<p>Montant: " + listeViolation[i]["montant"] + "$</p>";
            cmpInfraction++;
    }
    cmpInfraction = 1;
    return htmlInfo;
}

/**
 * Crée un objet plainte à partir des valeurs des champs du formulaire de plainte.
 * @returns Objet représentant une plainte
 */
function creerPlainte() {
    var plainteEtablissement = document.getElementById("etablissement").value;
    var plainteAdresse = document.getElementById("adresse").value;
    var plainteVille = document.getElementById("ville").value;
    var plainteDate = document.getElementById("date-visite").value;
    var plainteNom = document.getElementById("nom").value;
    var plaintePrenom = document.getElementById("prenom").value;
    var plainteDescription = document.getElementById("description").value;
  
    return {
      etablissement: plainteEtablissement,
      adresse: plainteAdresse,
      ville: plainteVille,
      date_visite: plainteDate,
      nom_client: plainteNom,
      prenom_client: plaintePrenom,
      description: plainteDescription
    };
  }

/**
 * Envoie une plainte au serveur qui sera stocké dans la BD en utilisant une requête POST
 * @returns true si la requête a été envoyée avec succès ce qui mêne au patron POST-REDIRECT-GET, false sinon
 */
function sendPlainte() {
  var plainteUtilisateur = creerPlainte();

  EffacerMsgErr();
  if (verifierInput(plainteUtilisateur.etablissement, plainteUtilisateur.adresse, plainteUtilisateur.ville, 
                    plainteUtilisateur.date_visite, plainteUtilisateur.nom_client, 
                    plainteUtilisateur.prenom_client,plainteUtilisateur.description)) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 201) {
          return true;
        }
      }
    };

    xhr.open("POST", "/api/plainte", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(plainteUtilisateur));
  } else {
    return false;
  }
}

/**  
 * Verifier que les inputs ne soit pas vide et respectent les formats.
 * @param plainteEtablissement - Le nom de l'établissement.
 * @param plainteAdresse - L'adresse de l'établissement.
 * @param plainteVille - La ville de l'établissement.
 * @param plainteDate - La date de la dernière visite dans l'établissement.
 * @param plainteNom - Le nom de l'utilisateur faisant la plainte.
 * @param plaintePrenom - Le prénom de l'utilisateur faisant la plainte.
 * @param plainteDescription - La description de la plainte.
 * @returns  Renvoie true si tous les champs sont remplis correctement sinon false.
*/
function verifierInput(plainteEtablissement, plainteAdresse, plainteVille, plainteDate, plainteNom, plaintePrenom, plainteDescription) {
    var verifierEtablissement = ValiderNonVide(plainteEtablissement, "errEtablissement");
    var verifierAdresse = ValiderNonVide(plainteAdresse, "errAdresse");
    var verifierVille = ValiderNonVide(plainteVille, "errVille");
    var verifierDate = ValiderNonVide(plainteDate, "errDate") && ValiderDate(plainteDate, "errDate");
    var verifierNom = ValiderNonVide(plainteNom, "errNom");
    var verifierPrenom = ValiderNonVide(plaintePrenom, "errPrenom");
    var verifierDescription = ValiderNonVide(plainteDescription, "errDescription");

    if (verifierEtablissement && verifierAdresse && verifierVille && verifierDate && verifierNom && verifierPrenom && verifierDescription) {
        return true;
    } else {
        return false;
    }
}

/**
 * Permet d'effacer les messages d'erreurs 
 */
function EffacerMsgErr() {
    document.getElementById("errEtablissement").innerHTML = "";
    document.getElementById("errAdresse").innerHTML = "";
    document.getElementById("errVille").innerHTML = "";
    document.getElementById("errDate").innerHTML = "";
    document.getElementById("errNom").innerHTML = "";
    document.getElementById("errPrenom").innerHTML = "";
    document.getElementById("errDescription").innerHTML = "";


}

/** 
 * Valider que le input n'est pas vide, sinon afficher un message d'erreur 
 * @param input - Le input du user a vérifier
 * @param idErr - Le id du span ou on doit afficher le message d'erreur, s'il y en a une.
 * @returns true si le input est valide, false sinon
 * */
function ValiderNonVide(input, idErr){
    if(input === ""){
        document.getElementById(idErr).innerHTML = "*Ce champ est obligatoire";
        return false;
    }
    return true;
}

/**
 * Valider que la date n'est pas vide et qu'elle respecte le bon format. Sinon, afficher un message d'erreur. 
 * @param date - La date a valider
 * @param idErr - Le id du span ou on doit afficher le message d'erreur, s'il y en a une.
 * @returns true s'il n'y a pas d'erreur, false sinon.
 * */
function ValiderDate(date, idErr){
    var regexDate = /^(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;

    if(!ValiderNonVide(date, idErr)){
        return false;
    } else if(!regexDate.test(date)){
        document.getElementById(idErr).innerHTML = "*Veuillez respecter le format AAAA-MM-JJ et entrez une date valide";
        return false;
    } else {
        var today = new Date();
        var inputDate = new Date(date);
        if (inputDate > today) {
            document.getElementById(idErr).innerHTML = "*La date ne doit pas dépasser la date d'aujourd'hui";
            return false;
        }
    }
    return true;
}

document.getElementById("button-date").addEventListener("click", rechercherParDate);
window.onload(creerListeDeroulante());