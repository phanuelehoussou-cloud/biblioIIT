from dataclasses import dataclass

@dataclass
class Reservation:
    id_reservation: int
    livre_reserver:str
    date_reservation: str
    date_retrait: str
    date_depot: str
    temps_utilsation:str
    adherent_nom:str
    