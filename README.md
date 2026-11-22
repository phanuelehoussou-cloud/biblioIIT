# BiblioIIT

BiblioIIT est une application web de gestion de bibliothèque, développée en Python avec Flask et SQLite. Elle permet de consulter le catalogue, gérer les adhérents, suivre les emprunts et enregistrer des réservations.

## Lancer le projet

Depuis le dossier du projet, créez un environnement Python, installez les dépendances puis démarrez le serveur Flask.

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app_web.py
```

Si l’activation de l’environnement est bloquée par les règles PowerShell de votre poste, vous pouvez lancer directement son interpréteur :

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app_web.py
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python app_web.py
```

Une fois le serveur lancé, ouvrez **http://127.0.0.1:5000** dans votre navigateur. Pour arrêter le serveur, utilisez `Ctrl+C` dans le terminal.

Au premier démarrage, l’application crée les tables SQLite et charge les données de démonstration si le catalogue est vide. La base se trouve dans `database/bibliotheque.db`.

## Naviguer dans l’application

La barre de navigation en haut de chaque page donne accès aux quatre rubriques :

- **Livres** (`/livres`) : afficher le catalogue et le nombre d’exemplaires disponibles, rechercher par titre ou auteur, et ajouter un livre avec son nombre d’exemplaires.
- **Adhérents** (`/adherents`) : consulter la liste, inscrire un adhérent et activer ou désactiver son compte.
- **Emprunts** (`/emprunts`) : voir les emprunts en cours et leur échéance, enregistrer un emprunt ou le retour d’un exemplaire. Un emprunt dure 14 jours et chaque adhérent peut avoir jusqu’à trois emprunts simultanés.
- **Réservations** (`/reservations`) : rechercher les réservations d’un adhérent avec son numéro, réserver un livre indisponible ou annuler une réservation en attente. Pour consulter les réservations, saisissez le numéro de l’adhérent puis cliquez sur **Voir ses réservations**.

Les formulaires affichent un message de confirmation ou d’erreur après leur envoi. Les champs demandant un numéro attendent les identifiants affichés dans les listes (numéro d’adhérent ou identifiant de livre/exemplaire selon l’action).

## Organisation du projet

```text
app_web.py              Routes Flask et démarrage de l’application
controllers/            Validation des entrées et réponses des actions
services/               Règles de gestion de la bibliothèque
models/                 Modèles Livre, Exemplaire, Adhérent, Emprunt et Réservation
database/               Connexion SQLite, création des tables et accès aux données
templates/               Pages HTML Jinja utilisées par Flask
static/css/style.css    Styles des pages web
main.py                 Point d’entrée de l’application en console
test.py                 Vérification manuelle du catalogue et de la recherche
```

## Vérification rapide

Pour afficher les exemplaires disponibles et vérifier la recherche du catalogue :

```bash
python test.py
```

Cette commande utilise également la base SQLite du projet et initialise les données de démonstration si le catalogue est vide.
