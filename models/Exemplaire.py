from dataclasses import dataclass

@dataclass
class Exemplaire:
    id_exemplaire: int
    livre_id: int
    disponible: bool
    


EXEMPLAIRES = [
    # Livre 1 : 3 exemplaires, 3 disponibles
    Exemplaire(1, 1, True),
    Exemplaire(2, 1, True),
    Exemplaire(3, 1, True),

    # Livre 2 : 2 exemplaires, 1 disponible
    Exemplaire(4, 2, True),
    Exemplaire(5, 2, False),

    # Livre 3 : 2 exemplaires, 2 disponibles
    Exemplaire(6, 3, True),
    Exemplaire(7, 3, True),

    # Livre 4 : 4 exemplaires, 3 disponibles
    Exemplaire(8, 4, True),
    Exemplaire(9, 4, True),
    Exemplaire(10, 4, True),
    Exemplaire(11, 4, False),

    # Livre 5 : 3 exemplaires, 2 disponibles
    Exemplaire(12, 5, True),
    Exemplaire(13, 5, True),
    Exemplaire(14, 5, False),

    # Livre 6 : 2 exemplaires, 2 disponibles
    Exemplaire(15, 6, True),
    Exemplaire(16, 6, True),

    # Livre 7 : 5 exemplaires, 4 disponibles
    Exemplaire(17, 7, True),
    Exemplaire(18, 7, True),
    Exemplaire(19, 7, True),
    Exemplaire(20, 7, True),
    Exemplaire(21, 7, False),

    # Livre 8 : 3 exemplaires, 0 disponible
    Exemplaire(22, 8, False),
    Exemplaire(23, 8, False),
    Exemplaire(24, 8, False),

    # Livre 9 : 2 exemplaires, 1 disponible
    Exemplaire(25, 9, True),
    Exemplaire(26, 9, False),

    # Livre 10 : 2 exemplaires, 2 disponibles
    Exemplaire(27, 10, True),
    Exemplaire(28, 10, True),
]