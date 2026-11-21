from services.EmpruntService import EmpruntService
from controllers.reponse import succes, echec, entier


class EmpruntController:
    def __init__(self):
        self.service = EmpruntService()

    def emprunter(self, adherent_id, livre_id):
        try:
            emprunt = self.service.emprunter(entier(adherent_id, "Adhérent"),
                                                entier(livre_id, "Livre"))
            return succes(f"Emprunt enregistré, retour prévu le {emprunt.date_retour_prevue}")
        except ValueError as erreur:
            return echec(str(erreur))

    def retourner(self, exemplaire_id):
        try:
            self.service.retourner(entier(exemplaire_id, "Exemplaire"))
            return succes("Livre retourné")
        except ValueError as erreur:
            return echec(str(erreur))

    def lister_en_cours(self):
        emprunts = self.service.lister_en_cours()
        return succes(f"{len(emprunts)} emprunt(s) en cours", emprunts)