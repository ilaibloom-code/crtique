# ============================================================
#  app.py  —  Serveur Flask du projet NSI
#  Réalisé par Ilaï avec l'aide de Claude (Anthropic)
# ============================================================

from flask import Flask, request, jsonify, render_template, make_response
# Flask      : le framework qui crée le serveur web
# request    : permet de lire ce que le navigateur envoie (JSON, cookies...)
# jsonify    : transforme un dict Python en réponse JSON lisible par le JS
# render_template : charge un fichier HTML depuis le dossier templates/
# make_response   : crée une réponse HTTP qu'on peut modifier (ex: ajouter un cookie)

import json   # pour lire et écrire le fichier votes.json
import os     # pour vérifier si le fichier existe avant de l'ouvrir

app = Flask(__name__)  # crée l'application Flask
VOTES_FILE = "votes.json"  # nom du fichier où on stocke les votes


# ─────────────────────────────────────────────
#  UTILITAIRES  —  lire / écrire le fichier JSON
# ─────────────────────────────────────────────

def lire_votes():
    # Si le fichier n'existe pas encore (premier lancement),
    # on retourne une structure vide plutôt que de planter
    if not os.path.exists(VOTES_FILE):
        return {"total": 0, "nb_votes": 0, "moyenne": 0, "historique": []}
    with open(VOTES_FILE, "r") as f:
        return json.load(f)  # transforme le JSON en dict Python f pour fichier juste une convention de nommage
def sauvegarder_votes(data):
    # indent=2 rend le fichier lisible si on l'ouvre à la main
    with open(VOTES_FILE, "w") as f:
        json.dump(data, f, indent=2)  # transforme le dict Python en JSON


# ─────────────────────────────────────────────
#  ROUTE  /  —  page principale
# ─────────────────────────────────────────────

@app.route("/")
def index():
    data = lire_votes()
    # render_template cherche index.html dans le dossier templates/
    # on lui passe data pour que Jinja2 puisse l'afficher dans le HTML
    return render_template("index.html", data=data)


# ─────────────────────────────────────────────
#  ROUTE  /vote  —  recevoir un vote (POST)
# ─────────────────────────────────────────────

@app.route("/vote", methods=["POST"])
def voter():

    # ÉTAPE 1 : vérifier si l'utilisateur a déjà voté
    # Le cookie "a_deja_vote" est posé par Flask via make_response dès qu'un vote est accepté — si la personne revient, le cookie est là et Flask renvoie une erreur 403 avant même de toucher au fichier.
    if request.cookies.get("a_deja_vote"):
        return jsonify({"erreur": "Vous avez déjà voté !"}), 403 #{} dictionnaire Python () appel de fonction 403 code HTTP renvoyé au navigateur

    # ÉTAPE 2 : récupérer la note envoyée par le JS (via fetch + JSON)
    note = request.json.get("note")
    prenom = request.json.get("prenom")
    commentaire = request.json.get("commentaire")

    # pourtant ca reste pas super sécurisé 
    # source :https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/Cookies mais ca ne nous dérange pas étant donné qu'on veut juste expériementer, sans l'ambition de vraiment vendre quelque chose

    # ÉTAPE 3 : valider la note — elle doit être un entier entre 1 et 5
    if not note or not isinstance(note, int) or not (1 <= note <= 5):
        return jsonify({"erreur": "Note invalide"}), 400  # 400 = mauvaise requête

    # d'apres cette article : https://pytutorial.com/fix-typeerror-not-supported-between-str-and-int c'est pas le mieux en gros si au lieu du nombre 3 je met le caractere 3 ca marchera pas parce que py ne peut pas comparer les 2, il faut juste que mes étoiles soient des nombres et pas des str

    # ÉTAPE 4 : calculer la moyenne mobile cumulative
    # Formule : moyenne = total_des_notes / nombre_de_votes
    # Exemple :  vote 1 → 5/1 = 5.0
    #            vote 2 → 9/2 = 4.5
    #            vote 3 → 10/3 = 3.3  etc.
    data = lire_votes()
    data["total"]    += note          # on ajoute la nouvelle note au total
    data["nb_votes"] += 1             # on compte un vote de plus
    data["moyenne"]   = round(data["total"] / data["nb_votes"], 2)  # 2 décimales

    # On sauvegarde aussi l'historique pour pouvoir l'afficher sur la page
    data["historique"].append({
        "note": note,
        "prenom": prenom,
        "commentaire": commentaire,
        "moyenne": data["moyenne"]
    })
    sauvegarder_votes(data)  # on écrit dans votes.json

    # ÉTAPE 5 : construire la réponse ET poser le cookie
    # make_response permet d'ajouter un cookie à une réponse JSON normale.
    # max_age = durée de vie du cookie en secondes (ici 1 an)
    reponse = make_response(jsonify({
        "succes": True,
        "moyenne": data["moyenne"],
        "nb_votes": data["nb_votes"]
    }))
    reponse.set_cookie("a_deja_vote", "1", max_age=60*60*24*365)
    #                   ^nom du cookie  ^valeur   ^1 an en secondes
    return reponse


# ─────────────────────────────────────────────
#  ROUTE  /resultats  —  afficher les données
# ─────────────────────────────────────────────

@app.route("/resultats")
def resultats():
    # Retourne tout le contenu de votes.json en JSON brut
    # Utile pour afficher les résultats sous la vidéo côté JS
    data = lire_votes()
    return jsonify(data)


# ─────────────────────────────────────────────
#  LANCEMENT  du serveur
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # debug=True : Flask recharge automatiquement quand on modifie le code
    # À désactiver en production !
    app.run(debug=True)
