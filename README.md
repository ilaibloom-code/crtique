# Critique Vidéo - Projet NSI

Ce projet est une application web Flask permettant aux utilisateurs de regarder une vidéo et de donner leur avis avec une note en étoiles, un prénom et un commentaire. Le serveur calcule la moyenne cumulative des notes et stocke les données dans un fichier JSON.

## Fonctionnalités

- Affichage d'une vidéo
- Système de notation avec 5 étoiles
- Formulaire pour prénom et commentaire
- Calcul de la moyenne mobile cumulative
- Prévention des votes multiples avec cookies
- Affichage des résultats et historique

## Structure du projet

```
crtique/
├── app.py                 # Serveur Flask
├── requirements.txt       # Dépendances Python
├── votes.json             # Stockage des données (généré automatiquement)
├── templates/
│   └── index.html         # Page principale
└── static/
    ├── style.css          # Styles CSS (thème noir et rouge)
    └── script.js          # JavaScript pour les étoiles et l'envoi
```

## Installation

1. Assurez-vous d'avoir Python 3 installé.

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Lancement

Exécutez le serveur Flask :
```bash
python app.py
```

Le serveur démarrera en mode debug sur http://127.0.0.1:5000/

## Utilisation

1. Ouvrez votre navigateur et allez sur http://127.0.0.1:5000/
2. Regardez la vidéo
3. Cliquez sur les étoiles pour donner une note
4. Remplissez le prénom et le commentaire
5. Cliquez sur "Envoyer" 
6. Les résultats se mettent à jour automatiquement

## Sécurité

- Les votes sont limités à un par utilisateur grâce aux cookies
- Validation des données côté serveur
- Stockage local des données (pas de base de données externe)

## Personnalisation

- Remplacez la source vidéo dans `templates/index.html`
- Modifiez les couleurs dans `static/style.css`
- Ajustez la logique dans `app.py` et `static/script.js`

## Auteurs

- Jules et Ilaï
