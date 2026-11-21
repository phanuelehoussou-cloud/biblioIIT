from rich.prompt import Prompt
from rich.table import Table

from views.outils import console, afficher_resultat, attendre


def _tableau(emprunts):
    table = Table(title="Emprunts en cours")
    for colonne in ("N°", "Exemplaire", "Livre", "Adhérent", "Emprunté le",
                    "Retour prévu", "Statut"):
        table.add_column(colonne)
    for e in emprunts:
        statut = "[red]En retard[/red]" if e["en_retard"] else "[green]OK[/green]"
        table.add_row(str(e["id_emprunt"]), str(e["exemplaire_id"]), e["titre"],
                        e["adherent"], str(e["date_emprunt"]),
                        str(e["date_retour_prevue"]), statut)
    console.print(table)


def menu(controller):
    while True:
        console.rule("[bold]Emprunts")
        console.print("1. Emprunter   2. Retourner   3. Emprunts en cours   0. Retour")
        choix = Prompt.ask("Choix", choices=["0", "1", "2", "3"])
        if choix == "0":
            return
        if choix == "1":
            rep = controller.emprunter(Prompt.ask("N° de l'adhérent"),
                                        Prompt.ask("N° du livre"))
        elif choix == "2":
            rep = controller.retourner(Prompt.ask("N° de l'exemplaire"))
        else:
            rep = controller.lister_en_cours()

        afficher_resultat(rep)
        if rep["ok"] and rep["data"]:
            _tableau(rep["data"])
        attendre()