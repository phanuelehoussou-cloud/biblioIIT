from datetime import date

from database.connexion import connexion, creer_tables
from database.livres_test import LIVRES
from database.exemplaires_test import EXEMPLAIRES
from models.Adherent import Adherent

ADHERENTS = [
    Adherent(1, "Kouassi", "Aya", date(2003, 5, 14), "F", date(2026, 9, 1)),
    Adherent(2, "Traoré", "Moussa", date(2002, 11, 3), "M", date(2026, 9, 5)),
    Adherent(3, "Koné", "Fatou", date(2004, 2, 21), "F", date(2026, 9, 12)),
]


def charger_donnees_test() -> None:
    """Crée les tables puis remplit la base, seulement si elle est vide."""
    creer_tables()
    with connexion() as conn:
        if conn.execute("SELECT COUNT(*) FROM livre").fetchone()[0] > 0:
            return

        conn.executemany(
            "INSERT INTO livre VALUES (?, ?, ?, ?, ?)",
            [(l.id, l.titre, l.auteur, l.categorie, l.annee_publication) for l in LIVRES],
        )
        conn.executemany(
            "INSERT INTO exemplaire VALUES (?, ?, ?)",
            [(e.id_exemplaire, e.livre_id, int(e.disponible)) for e in EXEMPLAIRES],
        )
        conn.executemany(
            "INSERT INTO adherent VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (a.id_adherent, a.nom, a.prenom, a.date_naissance.isoformat(),
                    a.sexe, a.date_inscription.isoformat(), int(a.actif))
                for a in ADHERENTS
            ],
        )