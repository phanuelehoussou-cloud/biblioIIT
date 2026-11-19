from dataclasses import dataclass

@dataclass
class Reservation:
    id_reservation: int
    livre_reserver:str
    date_reservation: str
    temps_utilsation:str
    nom_client:str
    