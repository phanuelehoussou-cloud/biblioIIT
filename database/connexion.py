import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent / "bibliotheque.db"


@contextmanager
def connexion():
    """Ouvre la base, valide les changements à la fin, annule en cas d'erreur, puis ferme."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # accès aux colonnes par nom
    conn.execute("PRAGMA foreign_keys = ON")  # vérifie les liens entre tables
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def creer_tables() -> None:
    with connexion() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS livre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            categorie TEXT NOT NULL,
            annee_publication INTEGER
        );

        CREATE TABLE IF NOT EXISTS exemplaire (
            id_exemplaire INTEGER PRIMARY KEY AUTOINCREMENT,
            livre_id INTEGER NOT NULL REFERENCES livre(id),
            disponible INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS adherent (
            id_adherent INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_naissance TEXT,
            sexe TEXT,
            date_inscription TEXT,
            actif INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS emprunt (
            id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT,
            exemplaire_id INTEGER NOT NULL REFERENCES exemplaire(id_exemplaire),
            adherent_id INTEGER NOT NULL REFERENCES adherent(id_adherent),
            date_emprunt TEXT NOT NULL,
            date_retour_prevue TEXT NOT NULL,
            date_retour_reelle TEXT
        );

        CREATE TABLE IF NOT EXISTS reservation (
            id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
            livre_id INTEGER NOT NULL REFERENCES livre(id),
            adherent_id INTEGER NOT NULL REFERENCES adherent(id_adherent),
            date_reservation TEXT NOT NULL,
            statut TEXT NOT NULL DEFAULT 'en_attente'
        );
        """)