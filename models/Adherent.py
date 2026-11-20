from dataclasses import dataclass

@dataclass
class Adherent:
    id_adherent: int
    nom: str
    prenom: str
    date_naiss: str
    sexe: str
    actif:bool