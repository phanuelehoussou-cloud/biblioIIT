from rich.prompt import Prompt

from database.donnees_test import charger_donnees_test
from controllers.LivreController import LivreController
from controllers.AdherentController import AdherentController
from controllers.EmpruntController import EmpruntController
from controllers.ReservationController import ReservationController
from views import livre_view, adherent_view, emprunt_view, reservation_view
from views.outils import console


def lancer():
    charger_donnees_test()
    livres = LivreController()
    adherents = AdherentController()
    emprunts = EmpruntController()
    reservations = ReservationController()

    while True:
        console.rule("[bold cyan]BIBLIO IIT")
        console.print("1. Livres   2. Adhérents   3. Emprunts   4. Réservations   0. Quitter")
        choix = Prompt.ask("Choix", choices=["0", "1", "2", "3", "4"])
        if choix == "0":
            console.print("Au revoir !")
            return
        if choix == "1":
            livre_view.menu(livres)
        elif choix == "2":
            adherent_view.menu(adherents)
        elif choix == "3":
            emprunt_view.menu(emprunts)
        else:
            reservation_view.menu(reservations)