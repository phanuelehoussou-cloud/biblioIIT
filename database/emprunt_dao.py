from datetime import date
from typing import Optional

from database.connexion import connexion
from models.Emprunt import Emprunt


def _date(valeur: Optional[str]) -> Optional[date]:
    return date.fromisoformat(valeur) if valeur else None


def _vers_emprunt(row) -> Emprunt:
    return Emprunt(
        row["id_emprunt"], row["exemplaire_id"], row["adherent_id"],
        _date(row["date_emprunt"]), _date(row["date_retour_prevue"]),
        _date(row["date_retour_reelle"]),
    )


class EmpruntDAO:
    def ajouter(self, e: Emprunt) -> int:
        with connexion() as conn:
            cur = conn.execute(
                "INSERT INTO emprunt (exemplaire_id, adherent_id, date_emprunt, "
                "date_retour_prevue) VALUES (?, ?, ?, ?)",
                (e.exemplaire_id, e.adherent_id,
                    e.date_emprunt.isoformat(), e.date_retour_prevue.isoformat()),
            )
            return cur.lastrowid

    def obtenir(self, emprunt_id: int) -> Optional[Emprunt]:
        with connexion() as conn:
            row = conn.execute(
                "SELECT * FROM emprunt WHERE id_emprunt = ?", (emprunt_id,)
            ).fetchone()
        return _vers_emprunt(row) if row else None

    def trouver_en_cours_par_exemplaire(self, exemplaire_id: int) -> Optional[Emprunt]:
        with connexion() as conn:
            row = conn.execute(
                "SELECT * FROM emprunt WHERE exemplaire_id = ? "
                "AND date_retour_reelle IS NULL",
                (exemplaire_id,),
            ).fetchone()
        return _vers_emprunt(row) if row else None

    def lister_en_cours(self) -> list[Emprunt]:
        with connexion() as conn:
            rows = conn.execute(
                "SELECT * FROM emprunt WHERE date_retour_reelle IS NULL "
                "ORDER BY date_retour_prevue"
            ).fetchall()
        return [_vers_emprunt(r) for r in rows]

    def lister_par_adherent(self, adherent_id: int) -> list[Emprunt]:
        with connexion() as conn:
            rows = conn.execute(
                "SELECT * FROM emprunt WHERE adherent_id = ? ORDER BY date_emprunt DESC",
                (adherent_id,),
            ).fetchall()
        return [_vers_emprunt(r) for r in rows]

    def compter_en_cours(self, adherent_id: int) -> int:
        with connexion() as conn:
            return conn.execute(
                "SELECT COUNT(*) FROM emprunt "
                "WHERE adherent_id = ? AND date_retour_reelle IS NULL",
                (adherent_id,),
            ).fetchone()[0]

    def enregistrer_retour(self, emprunt_id: int, date_retour: date) -> None:
        with connexion() as conn:
            conn.execute(
                "UPDATE emprunt SET date_retour_reelle = ? WHERE id_emprunt = ?",
                (date_retour.isoformat(), emprunt_id),
            )