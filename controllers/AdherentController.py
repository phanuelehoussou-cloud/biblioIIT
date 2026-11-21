from services.BibliothequeService import BibliothequeService
from controllers.reponse import succes, echec, entier, date_iso


class AdherentController:
    def __init__(self):
        self.service = BibliothequeService()

    def lister(self):
        adherents = self.service.lister_adherents()
        return succes(f"{len(adherents)} adhérent(s)", adherents)

    def inscrire(self, nom, prenom, date_naissance, sexe):
        try:
            adherent_id = self.service.inscrire_adherent(
                nom, prenom, date_iso(date_naissance, "Date de naissance"), sexe)
            return succes(f"Adhérent inscrit (n°{adherent_id})")
        except ValueError as erreur:
            return echec(str(erreur))

    def changer_statut(self, adherent_id, actif):
        try:
            self.service.changer_statut_adherent(entier(adherent_id, "Adhérent"), actif)
            return succes("Adhérent activé" if actif else "Adhérent désactivé")
        except ValueError as erreur:
            return echec(str(erreur))