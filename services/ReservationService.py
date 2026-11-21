from datetime import date

from models.Reservation import Reservation
from database.adherent_dao import AdherentDAO
from database.exemplaire_dao import ExemplaireDAO
from database.livre_dao import LivreDAO
from database.reservation_dao import ReservationDAO


class ReservationService:
    def __init__(self):
        self.adherent_dao = AdherentDAO()
        self.exemplaire_dao = ExemplaireDAO()
        self.livre_dao = LivreDAO()
        self.reservation_dao = ReservationDAO()

    def reserver(self, adherent_id, livre_id):
        adherent = self.adherent_dao.obtenir(adherent_id)
        if adherent is None:
            raise ValueError("Adhérent introuvable")
        if not adherent.actif:
            raise ValueError("Adhérent inactif")
        if self.livre_dao.obtenir(livre_id) is None:
            raise ValueError("Livre introuvable")
        if self.exemplaire_dao.premier_disponible(livre_id) is not None:
            raise ValueError("Ce livre est disponible : empruntez-le directement")

        for r in self.reservation_dao.lister_par_adherent(adherent_id):
            if r.livre_id == livre_id and r.statut == "en_attente":
                raise ValueError("Vous avez déjà réservé ce livre")

        reservation = Reservation(0, livre_id, adherent_id, date.today())
        reservation.id_reservation = self.reservation_dao.ajouter(reservation)
        return reservation

    def annuler(self, reservation_id):
        reservation = self.reservation_dao.obtenir(reservation_id)
        if reservation is None:
            raise ValueError("Réservation introuvable")
        if reservation.statut != "en_attente":
            raise ValueError("Réservation déjà traitée")
        self.reservation_dao.changer_statut(reservation_id, "annulee")

    def prochaine_reservation(self, livre_id):
        """La plus ancienne réservation en attente, ou None."""
        attente = self.reservation_dao.lister_en_attente_par_livre(livre_id)
        return attente[0] if attente else None

    def lister_par_adherent(self, adherent_id):
        if self.adherent_dao.obtenir(adherent_id) is None:
            raise ValueError("Adhérent introuvable")
        resultat = []
        for r in self.reservation_dao.lister_par_adherent(adherent_id):
            livre = self.livre_dao.obtenir(r.livre_id)
            resultat.append({
                "id": r.id_reservation, "titre": livre.titre,
                "date": r.date_reservation, "statut": r.statut,
            })
        return resultat