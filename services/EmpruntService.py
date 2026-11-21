from datetime import date, timedelta

from models.Emprunt import Emprunt
from database.adherent_dao import AdherentDAO
from database.emprunt_dao import EmpruntDAO
from database.exemplaire_dao import ExemplaireDAO


class EmpruntService:
    LIMITE_EMPRUNTS = 3
    DUREE_JOURS = 14

    def __init__(self):
        self.adherent_dao = AdherentDAO()
        self.emprunt_dao = EmpruntDAO()
        self.exemplaire_dao = ExemplaireDAO()

    def emprunter(self, adherent_id, livre_id):
        adherent = self.adherent_dao.obtenir(adherent_id)
        if adherent is None:
            raise ValueError("Adhérent introuvable")
        if not adherent.actif:
            raise ValueError("Adhérent inactif")
        if self.emprunt_dao.compter_en_cours(adherent_id) >= self.LIMITE_EMPRUNTS:
            raise ValueError("Limite d'emprunts atteinte")

        exemplaire = self.exemplaire_dao.premier_disponible(livre_id)
        if exemplaire is None:
            raise ValueError("Aucun exemplaire disponible")

        date_emprunt = date.today()
        date_retour_prevue = date_emprunt + timedelta(days=self.DUREE_JOURS)

        emprunt = Emprunt(0, exemplaire.id_exemplaire, adherent_id,
                        date_emprunt, date_retour_prevue)
        emprunt.id_emprunt = self.emprunt_dao.ajouter(emprunt)

        self.exemplaire_dao.changer_disponibilite(exemplaire.id_exemplaire, False)
        return emprunt

    def retourner(self, exemplaire_id):
        emprunt = self.emprunt_dao.trouver_en_cours_par_exemplaire(exemplaire_id)
        if emprunt is None:
            raise ValueError("Aucun emprunt en cours pour cet exemplaire")

        self.emprunt_dao.enregistrer_retour(emprunt.id_emprunt, date.today())
        self.exemplaire_dao.changer_disponibilite(exemplaire_id, True)
        return emprunt