from typing import Optional

from database.connexion import connexion
from models.Exemplaire import Exemplaire


def _vers_exemplaire(row) -> Exemplaire:
    return Exemplaire(row["id_exemplaire"], row["livre_id"], bool(row["disponible"]))


class ExemplaireDAO:
    def ajouter(self, exemplaire: Exemplaire) -> int:
        with connexion() as conn:
            cur = conn.execute(
                "INSERT INTO exemplaire (livre_id, disponible) VALUES (?, ?)",
                (exemplaire.livre_id, int(exemplaire.disponible)),
            )
            return cur.lastrowid

    def obtenir(self, exemplaire_id: int) -> Optional[Exemplaire]:
        with connexion() as conn:
            row = conn.execute(
                "SELECT * FROM exemplaire WHERE id_exemplaire = ?", (exemplaire_id,)
            ).fetchone()
        return _vers_exemplaire(row) if row else None

    def lister_par_livre(self, livre_id: int) -> list[Exemplaire]:
        with connexion() as conn:
            rows = conn.execute(
                "SELECT * FROM exemplaire WHERE livre_id = ?", (livre_id,)
            ).fetchall()
        return [_vers_exemplaire(r) for r in rows]

    def premier_disponible(self, livre_id: int) -> Optional[Exemplaire]:
        with connexion() as conn:
            row = conn.execute(
                "SELECT * FROM exemplaire WHERE livre_id = ? AND disponible = 1 LIMIT 1",
                (livre_id,),
            ).fetchone()
        return _vers_exemplaire(row) if row else None

    def changer_disponibilite(self, exemplaire_id: int, disponible: bool) -> None:
        with connexion() as conn:
            conn.execute(
                "UPDATE exemplaire SET disponible = ? WHERE id_exemplaire = ?",
                (int(disponible), exemplaire_id),
            )

    def compter(self, livre_id: int) -> tuple[int, int]:
        """Renvoie (total, disponibles) : remplace les anciens compteurs."""
        with connexion() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS total, COALESCE(SUM(disponible), 0) AS dispo "
                "FROM exemplaire WHERE livre_id = ?",
                (livre_id,),
            ).fetchone()
        return row["total"], row["dispo"]