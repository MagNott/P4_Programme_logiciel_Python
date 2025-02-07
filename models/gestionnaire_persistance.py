from tinydb import TinyDB, Query


class GestionnairePersistance:
    def __init__(self):
        self.db = TinyDB("db.json")

    def sauvegarder(self):
        # Logique à implémenter plus tard
        pass

    def sauvegarder_joueur(self, p_joueur_modele):
        donnees_joueur = {
            "nom_famille": p_joueur_modele.nom_famille,
            "prenom": p_joueur_modele.prenom,
        }
        self.db.insert(donnees_joueur)

    def charger(self):
        # Logique à implémenter plus tard
        pass

    def charger_joueurs(self):
        return self.db.all()
