from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Emprunt:
    id_emprunt: int
    exemplaire_id: int
    adherent_id: int
    date_emprunt: date
    date_retour_prevue: date
    date_retour_reelle: Optional[date] = None