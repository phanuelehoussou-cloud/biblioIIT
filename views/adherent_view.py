from rich.prompt import Prompt
from rich.table import Table

from views.outils import console, afficher_resultat, attendre


def _tableau(adherents):
    table = Table(title="Adhérents")
    for colonne in ("ID", "Nom", "Prénom", "Naissance", "Sexe", "Statut"):
        table.add_column(colonne)
    for a in adherents:
        statut = "[green]Actif[/green]" if a.actif else "[red]Inactif[/red]"
        table.add_row(str(a.id_adherent), a.nom, a.prenom,
                      str(a.date_naissance), a.sexe, statut)
    console.print(table)


def menu(controller):
    while True:
        console.rule("[bold]Adhérents")
        console.print("1. Lister   2. Inscrire   3. Activer/Désactiver   0. Retour")
        choix = Prompt.ask("Choix", choices=["0", "1", "2", "3"])
        if choix == "0":
            return
        if choix == "1":
            rep = controller.lister()
        elif choix == "2":
            rep = controller.inscrire(
                Prompt.ask("Nom"), Prompt.ask("Prénom"),
                Prompt.ask("Date de naissance (AAAA-MM-JJ)"),
                Prompt.ask("Sexe", choices=["M", "F"]))
        else:
            adherent_id = Prompt.ask("N° de l'adhérent")
            action = Prompt.ask("Nouveau statut", choices=["actif", "inactif"])
            rep = controller.changer_statut(adherent_id, action == "actif")

        afficher_resultat(rep)
        if rep["ok"] and rep["data"]:
            _tableau(rep["data"])
        attendre()