from datetime import date
from typing import Optional

from database.connexion import connexion
from models.Adherent import Adherent


def _date(valeur: Optional[str]) -> Optional[date]:
    return date.fromisoformat(valeur) if valeur else None


def _vers_adherent(row) -> Adherent:
    return Adherent(
        row["id_adherent"], row["nom"], row["prenom"],
        _date(row["date_naissance"]), row["sexe"],
        _date(row["date_inscription"]), bool(row["actif"]),
    )


class AdherentDAO:
    def ajouter(self, a: Adherent) -> int:
        with connexion() as conn:
            cur = conn.execute(
                "INSERT INTO adherent (nom, prenom, date_naissance, sexe, "
                "date_inscription, actif) VALUES (?, ?, ?, ?, ?, ?)",
                (a.nom, a.prenom, a.date_naissance.isoformat(), a.sexe,
                    a.date_inscription.isoformat(), int(a.actif)),
            )
            return cur.lastrowid

    def obtenir(self, adherent_id: int) -> Optional[Adherent]:
        with connexion() as conn:
            row = conn.execute(
                "SELECT * FROM adherent WHERE id_adherent = ?", (adherent_id,)
            ).fetchone()
        return _vers_adherent(row) if row else None

    def lister(self) -> list[Adherent]:
        with connexion() as conn:
            rows = conn.execute("SELECT * FROM adherent ORDER BY nom, prenom").fetchall()
        return [_vers_adherent(r) for r in rows]

    def changer_actif(self, adherent_id: int, actif: bool) -> None:
        with connexion() as conn:
            conn.execute(
                "UPDATE adherent SET actif = ? WHERE id_adherent = ?",
                (int(actif), adherent_id),
            )