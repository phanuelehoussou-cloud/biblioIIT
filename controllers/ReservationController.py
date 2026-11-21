from services.ReservationService import ReservationService
from controllers.reponse import succes, echec, entier


class ReservationController:
    def __init__(self):
        self.service = ReservationService()

    def reserver(self, adherent_id, livre_id):
        try:
            r = self.service.reserver(entier(adherent_id, "Adhérent"),
                                        entier(livre_id, "Livre"))
            return succes(f"Réservation n°{r.id_reservation} enregistrée")
        except ValueError as erreur:
            return echec(str(erreur))

    def annuler(self, reservation_id):
        try:
            self.service.annuler(entier(reservation_id, "Réservation"))
            return succes("Réservation annulée")
        except ValueError as erreur:
            return echec(str(erreur))

    def lister_par_adherent(self, adherent_id):
        try:
            liste = self.service.lister_par_adherent(entier(adherent_id, "Adhérent"))
            return succes(f"{len(liste)} réservation(s)", liste)
        except ValueError as erreur:
            return echec(str(erreur))