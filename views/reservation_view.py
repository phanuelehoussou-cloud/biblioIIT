from rich.prompt import Prompt
from rich.table import Table

from views.outils import console, afficher_resultat, attendre


def _tableau(reservations):
    table = Table(title="Réservations")
    for colonne in ("N°", "Livre", "Date", "Statut"):
        table.add_column(colonne)
    for r in reservations:
        table.add_row(str(r["id"]), r["titre"], str(r["date"]), r["statut"])
    console.print(table)


def menu(controller):
    while True:
        console.rule("[bold]Réservations")
        console.print("1. Réserver   2. Annuler   3. Réservations d'un adhérent   0. Retour")
        choix = Prompt.ask("Choix", choices=["0", "1", "2", "3"])
        if choix == "0":
            return
        if choix == "1":
            rep = controller.reserver(Prompt.ask("N° de l'adhérent"),
                                        Prompt.ask("N° du livre"))
        elif choix == "2":
            rep = controller.annuler(Prompt.ask("N° de la réservation"))
        else:
            rep = controller.lister_par_adherent(Prompt.ask("N° de l'adhérent"))

        afficher_resultat(rep)
        if rep["ok"] and rep["data"]:
            _tableau(rep["data"])
        attendre()