from services.BibliothequeService import BibliothequeService
from controllers.reponse import succes, echec, entier


class LivreController:
    def __init__(self):
        self.service = BibliothequeService()

    def lister(self):
        livres = self.service.lister_livres()
        return succes(f"{len(livres)} livre(s)", livres)

    def rechercher(self, texte):
        livres = self.service.rechercher_livres(texte)
        return succes(f"{len(livres)} résultat(s)", livres)

    def ajouter(self, titre, auteur, categorie, annee, nb_exemplaires):
        try:
            livre_id = self.service.ajouter_livre(
                titre, auteur, categorie,
                entier(annee, "Année"),
                entier(nb_exemplaires, "Nombre d'exemplaires"),
            )
            return succes(f"Livre ajouté (n°{livre_id})")
        except ValueError as erreur:
            return echec(str(erreur))