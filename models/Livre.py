from dataclasses import dataclass

@dataclass
class Livre :
    id: int
    titre: str
    auteur: str
    categorie: str
    annee_publication: str
    nbr_exemplaire: int
    exemplaire_disponible: int