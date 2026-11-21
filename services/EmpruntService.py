from datetime import date, timedelta

from models.Emprunt import Emprunt
from database.adherent_dao import AdherentDAO
from database.emprunt_dao import EmpruntDAO
from database.exemplaire_dao import ExemplaireDAO
from database.livre_dao import LivreDAO


class EmpruntService:
    LIMITE_EMPRUNTS = 3
    DUREE_JOURS = 14

    def __init__(self):
        self.adherent_dao = AdherentDAO()
        self.emprunt_dao = EmpruntDAO()
        self.exemplaire_dao = ExemplaireDAO()
        self.livre_dao = LivreDAO()

    def emprunter(self, adherent_id, livre_id):
        adherent = self.adherent_dao.obtenir(adherent_id)
        if adherent is None:
            raise ValueError("Adhérent introuvable")
        if not adherent.actif:
            raise ValueError("Adhérent inactif")
        if self.livre_dao.obtenir(livre_id) is None:
            raise ValueError("Livre introuvable")
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

    def lister_en_cours(self):
        resultat = []
        for e in self.emprunt_dao.lister_en_cours():
            exemplaire = self.exemplaire_dao.obtenir(e.exemplaire_id)
            livre = self.livre_dao.obtenir(exemplaire.livre_id)
            adherent = self.adherent_dao.obtenir(e.adherent_id)
            resultat.append({
                "id_emprunt": e.id_emprunt,
                "exemplaire_id": e.exemplaire_id,
                "titre": livre.titre,
                "adherent": f"{adherent.prenom} {adherent.nom}",
                "date_emprunt": e.date_emprunt,
                "date_retour_prevue": e.date_retour_prevue,
                "en_retard": date.today() > e.date_retour_prevue,
            })
        return resultat