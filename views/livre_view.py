from rich.prompt import Prompt
from rich.table import Table

from views.outils import console, afficher_resultat, attendre


def _tableau(livres):
    table = Table(title="Catalogue")
    for colonne in ("ID", "Titre", "Auteur", "Catégorie", "Année", "Disponibles"):
        table.add_column(colonne)
    for l in livres:
        couleur = "green" if l["dispo"] > 0 else "red"
        table.add_row(str(l["id"]), l["titre"], l["auteur"], l["categorie"],
                        str(l["annee"]), f"[{couleur}]{l['dispo']}/{l['total']}[/{couleur}]")
    console.print(table)


def menu(controller):
    while True:
        console.rule("[bold]Livres")
        console.print("1. Lister   2. Rechercher   3. Ajouter   0. Retour")
        choix = Prompt.ask("Choix", choices=["0", "1", "2", "3"])
        if choix == "0":
            return
        if choix == "1":
            rep = controller.lister()
        elif choix == "2":
            rep = controller.rechercher(Prompt.ask("Titre ou auteur"))
        else:
            rep = controller.ajouter(
                Prompt.ask("Titre"), Prompt.ask("Auteur"), Prompt.ask("Catégorie"),
                Prompt.ask("Année"), Prompt.ask("Nombre d'exemplaires", default="1"))

        afficher_resultat(rep)
        if rep["ok"] and rep["data"]:
            _tableau(rep["data"])
        attendre()