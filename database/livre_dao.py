from typing import Optional

from database.connexion import connexion
from models.Livre import Livre


def _vers_livre(row) -> Livre:
    return Livre(row["id"], row["titre"], row["auteur"],
                 row["categorie"], row["annee_publication"])


class LivreDAO:
    def ajouter(self, livre: Livre) -> int:
        with connexion() as conn:
            cur = conn.execute(
                "INSERT INTO livre (titre, auteur, categorie, annee_publication) "
                "VALUES (?, ?, ?, ?)",
                (livre.titre, livre.auteur, livre.categorie, livre.annee_publication),
            )
            return cur.lastrowid

    def obtenir(self, livre_id: int) -> Optional[Livre]:
        with connexion() as conn:
            row = conn.execute("SELECT * FROM livre WHERE id = ?", (livre_id,)).fetchone()
        return _vers_livre(row) if row else None

    def lister(self) -> list[Livre]:
        with connexion() as conn:
            rows = conn.execute("SELECT * FROM livre ORDER BY titre").fetchall()
        return [_vers_livre(r) for r in rows]

    def rechercher(self, texte: str) -> list[Livre]:
        motif = f"%{texte}%"
        with connexion() as conn:
            rows = conn.execute(
                "SELECT * FROM livre WHERE titre LIKE ? OR auteur LIKE ? ORDER BY titre",
                (motif, motif),
            ).fetchall()
        return [_vers_livre(r) for r in rows]

    def supprimer(self, livre_id: int) -> None:
        with connexion() as conn:
            conn.execute("DELETE FROM livre WHERE id = ?", (livre_id,))