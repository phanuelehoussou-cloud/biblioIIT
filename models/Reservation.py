from dataclasses import dataclass
from datetime import date

@dataclass
class Reservation:
    id_reservation: int
    livre_id: int
    adherent_id: int
    date_reservation: date
    statut: str = "en_attente"