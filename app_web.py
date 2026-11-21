from flask import Flask, render_template, request, redirect, url_for, flash

from database.donnees_test import charger_donnees_test
from controllers.LivreController import LivreController
from controllers.AdherentController import AdherentController
from controllers.EmpruntController import EmpruntController
from controllers.ReservationController import ReservationController

app = Flask(__name__)
app.secret_key = "biblioiit-dev"

charger_donnees_test()
livres_ctrl = LivreController()
adherents_ctrl = AdherentController()
emprunts_ctrl = EmpruntController()
reservations_ctrl = ReservationController()


def notifier(rep):
    """Affiche le message du controller dans un bandeau Bootstrap."""
    flash(rep["message"], "success" if rep["ok"] else "danger")


# ---------- Livres ----------
@app.route("/")
@app.route("/livres")
def livres():
    q = request.args.get("q", "").strip()
    rep = livres_ctrl.rechercher(q) if q else livres_ctrl.lister()
    return render_template("livres.html", livres=rep["data"], q=q)


@app.post("/livres/ajouter")
def ajouter_livre():
    f = request.form
    notifier(livres_ctrl.ajouter(f.get("titre"), f.get("auteur"), f.get("categorie"),
                                 f.get("annee"), f.get("nb_exemplaires")))
    return redirect(url_for("livres"))


# ---------- Adhérents ----------
@app.route("/adherents")
def adherents():
    return render_template("adherents.html", adherents=adherents_ctrl.lister()["data"])


@app.post("/adherents/inscrire")
def inscrire_adherent():
    f = request.form
    notifier(adherents_ctrl.inscrire(f.get("nom"), f.get("prenom"),
                                     f.get("date_naissance"), f.get("sexe")))
    return redirect(url_for("adherents"))


@app.post("/adherents/<int:adherent_id>/statut")
def statut_adherent(adherent_id):
    actif = request.form.get("actif") == "1"
    notifier(adherents_ctrl.changer_statut(adherent_id, actif))
    return redirect(url_for("adherents"))


# ---------- Emprunts ----------
@app.route("/emprunts")
def emprunts():
    return render_template("emprunts.html", emprunts=emprunts_ctrl.lister_en_cours()["data"])


@app.post("/emprunts/emprunter")
def emprunter():
    f = request.form
    notifier(emprunts_ctrl.emprunter(f.get("adherent_id"), f.get("livre_id")))
    return redirect(url_for("emprunts"))


@app.post("/emprunts/retourner")
def retourner():
    notifier(emprunts_ctrl.retourner(request.form.get("exemplaire_id")))
    return redirect(url_for("emprunts"))


# ---------- Réservations ----------
@app.route("/reservations")
def reservations():
    adherent_id = request.args.get("adherent_id", "").strip()
    liste = None
    if adherent_id:
        rep = reservations_ctrl.lister_par_adherent(adherent_id)
        if rep["ok"]:
            liste = rep["data"]
        else:
            notifier(rep)
    return render_template("reservations.html", reservations=liste, adherent_id=adherent_id)


@app.post("/reservations/reserver")
def reserver():
    f = request.form
    notifier(reservations_ctrl.reserver(f.get("adherent_id"), f.get("livre_id")))
    return redirect(url_for("reservations", adherent_id=f.get("adherent_id")))


@app.post("/reservations/<int:reservation_id>/annuler")
def annuler_reservation(reservation_id):
    notifier(reservations_ctrl.annuler(reservation_id))
    return redirect(url_for("reservations", adherent_id=request.form.get("adherent_id")))


if __name__ == "__main__":
    app.run(debug=True)