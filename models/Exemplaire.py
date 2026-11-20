from dataclasses import dataclass

@dataclass
class Exemplaire:
    id_exemplaire: int
    titre_livre: str
    disponible: bool
    nbr_exemplaire: int
    nbr_dispo:int
    nbr_indispo:int