from database.donnees_test import charger_donnees_test
from database.livre_dao import LivreDAO
from database.exemplaire_dao import ExemplaireDAO

charger_donnees_test()

livres = LivreDAO()
exemplaires = ExemplaireDAO()

for livre in livres.lister():
    total, dispo = exemplaires.compter(livre.id)
    print(f"{livre.titre} : {dispo}/{total} disponibles")

print(livres.rechercher("Kourouma"))