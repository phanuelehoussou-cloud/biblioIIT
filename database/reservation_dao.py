from datetime import date
from typing import Optional

from database.connexion import connexion
from models.Reservation import Reservation


def _vers_reservation(row) -> Reservation:
    return Reservation(
        row["id_reservation"], row["livre_id"], row["adherent_id"],
        date.fromisoformat(row["date_reservation"]), row["statut"],
    )


class ReservationDAO:
    def ajouter(self, r: Reservation) -> int:
        with connexion() as conn:
            cur = conn.execute(
                "INSERT INTO reservation (livre_id, adherent_id, date_reservation, statut) "
                "VALUES (?, ?, ?, ?)",
                (r.livre_id, r.adherent_id, r.date_reservation.isoformat(), r.statut),
            )
            return cur.lastrowid

    def obtenir(self, reservation_id: int) -> Optional[Reservation]:
        with connexion() as conn:
            row = conn.execute(
                "SELECT * FROM reservation WHERE id_reservation = ?", (reservation_id,)
            ).fetchone()
        return _vers_reservation(row) if row else None

    def lister_en_attente_par_livre(self, livre_id: int) -> list[Reservation]:
        """Les plus anciennes d'abord : premier arrivé, premier servi."""
        with connexion() as conn:
            rows = conn.execute(
                "SELECT * FROM reservation WHERE livre_id = ? AND statut = 'en_attente' "
                "ORDER BY date_reservation, id_reservation",
                (livre_id,),
            ).fetchall()
        return [_vers_reservation(r) for r in rows]

    def lister_par_adherent(self, adherent_id: int) -> list[Reservation]:
        with connexion() as conn:
            rows = conn.execute(
                "SELECT * FROM reservation WHERE adherent_id = ? ORDER BY date_reservation DESC",
                (adherent_id,),
            ).fetchall()
        return [_vers_reservation(r) for r in rows]

    def changer_statut(self, reservation_id: int, statut: str) -> None:
        with connexion() as conn:
            conn.execute(
                "UPDATE reservation SET statut = ? WHERE id_reservation = ?",
                (statut, reservation_id),
            )