from datetime import date

from models.Livre import Livre
from models.Exemplaire import Exemplaire
from models.Adherent import Adherent
from database.livre_dao import LivreDAO
from database.exemplaire_dao import ExemplaireDAO
from database.adherent_dao import AdherentDAO


class BibliothequeService:
    def __init__(self):
        self.livre_dao = LivreDAO()
        self.exemplaire_dao = ExemplaireDAO()
        self.adherent_dao = AdherentDAO()

    def _avec_stock(self, livres):
        resultat = []
        for livre in livres:
            total, dispo = self.exemplaire_dao.compter(livre.id)
            resultat.append({
                "id": livre.id, "titre": livre.titre, "auteur": livre.auteur,
                "categorie": livre.categorie, "annee": livre.annee_publication,
                "total": total, "dispo": dispo,
            })
        return resultat

    # ---------- Livres ----------
    def lister_livres(self):
        return self._avec_stock(self.livre_dao.lister())

    def rechercher_livres(self, texte):
        return self._avec_stock(self.livre_dao.rechercher((texte or "").strip()))

    def ajouter_livre(self, titre, auteur, categorie, annee, nb_exemplaires):
        titre = (titre or "").strip()
        auteur = (auteur or "").strip()
        categorie = (categorie or "").strip() or "Autre"
        if not titre or not auteur:
            raise ValueError("Le titre et l'auteur sont obligatoires")
        if nb_exemplaires < 1:
            raise ValueError("Il faut au moins un exemplaire")

        livre_id = self.livre_dao.ajouter(Livre(0, titre, auteur, categorie, annee))
        for _ in range(nb_exemplaires):
            self.exemplaire_dao.ajouter(Exemplaire(0, livre_id, True))
        return livre_id

    # ---------- Adhérents ----------
    def lister_adherents(self):
        return self.adherent_dao.lister()

    def inscrire_adherent(self, nom, prenom, date_naissance, sexe):
        nom = (nom or "").strip()
        prenom = (prenom or "").strip()
        sexe = (sexe or "").strip().upper()
        if not nom or not prenom:
            raise ValueError("Le nom et le prénom sont obligatoires")
        if date_naissance >= date.today():
            raise ValueError("Date de naissance invalide")
        if sexe not in ("M", "F"):
            raise ValueError("Le sexe doit être M ou F")

        adherent = Adherent(0, nom, prenom, date_naissance, sexe, date.today())
        return self.adherent_dao.ajouter(adherent)

    def changer_statut_adherent(self, adherent_id, actif):
        if self.adherent_dao.obtenir(adherent_id) is None:
            raise ValueError("Adhérent introuvable")
        self.adherent_dao.changer_actif(adherent_id, actif)