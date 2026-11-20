from dataclasses import dataclass

@dataclass
class Emprunt:
    id_emprunt: int
    livre_conserne: str
    adherent_nom:str
    date_retrait: str
    date_depot: str
    temps_utilsation:str