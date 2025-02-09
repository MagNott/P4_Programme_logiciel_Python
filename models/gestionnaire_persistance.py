from tinydb import TinyDB, Query
import os


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

    def sauvegarder_tournoi(self, p_tournoi_modele):
        donnees_tournoi = {
            "nom_tournoi": p_tournoi_modele.nom_tournoi,
            "lieu_tournoi": p_tournoi_modele.lieu_tournoi,
            "date_debut_tournoi": p_tournoi_modele.date_debut_tournoi,
            "date_fin_tournoi": p_tournoi_modele.date_fin_tournoi,
            "nombre_tours": p_tournoi_modele.nombre_tours,
            "description": p_tournoi_modele.description,
        }
        self.db_tournois = TinyDB(f"data/tournaments/tournoi_{p_tournoi_modele.identifiant}.json")
        self.db_tournois.insert(donnees_tournoi)

    def sauvegarder_joueurs_tournoi(self, p_tournoi_modele):
        donnees_joueurs = {
            "liste_joueurs": p_tournoi_modele.liste_joueurs,
        }
        self.db_tournois = TinyDB(f"data/tournaments/tournoi_{p_tournoi_modele.identifiant}.json")
        self.db_tournois.update(donnees_joueurs, doc_ids=[int(1)])

    def charger_tournoi(self, p_identifiant_tournoi):
        self.db_tournois = TinyDB(f"data/tournaments/tournoi_{p_identifiant_tournoi}.json")
        return self.db_tournois.all()

    def lister_tournois(self):
        "Liste tous les fichiers dans le dossier tournaments."
        chemin_dossier = "data/tournaments"
        fichiers_tournois = []
        for tournoi in os.listdir(chemin_dossier):
            fichiers_tournois.append(tournoi)
        return fichiers_tournois
