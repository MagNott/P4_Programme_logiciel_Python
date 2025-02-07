from tinydb import TinyDB, Query



class GestionnairePersistance:
    def __init__(self):
        self.db_joueurs = TinyDB("data/players/joueurs_db.json")

    def sauvegarder(self):
        # Logique à implémenter plus tard
        pass

    def sauvegarder_joueur(self, p_joueur_modele):
        donnees_joueur = {
            "identifiant_national_echec": p_joueur_modele.identifiant_national_echec,
            "nom_famille": p_joueur_modele.nom_famille,
            "prenom": p_joueur_modele.prenom,
            "date_naissance": p_joueur_modele.date_naissance,
        }
        self.db_joueurs.insert(donnees_joueur)

    def charger(self):
        # Logique à implémenter plus tard
        pass

    def charger_joueurs(self):
        return self.db_joueurs.all()
