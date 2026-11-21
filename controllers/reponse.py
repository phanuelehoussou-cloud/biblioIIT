from datetime import date


def succes(message="", data=None):
    return {"ok": True, "message": message, "data": data}


def echec(message):
    return {"ok": False, "message": message, "data": None}


def entier(valeur, nom="Valeur"):
    try:
        return int(valeur)
    except (TypeError, ValueError):
        raise ValueError(f"{nom} invalide")


def date_iso(valeur, nom="Date"):
    try:
        return date.fromisoformat(str(valeur).strip())
    except ValueError:
        raise ValueError(f"{nom} invalide (format AAAA-MM-JJ)")