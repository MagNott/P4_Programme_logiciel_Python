from tinydb import TinyDB
from models.tournoi import Tournoi
from models.joueur import Joueur
import os


class GestionnairePersistance:
    """Gère la persistance des données des joueurs et des tournois avec TinyDB."""

    def __init__(self):
        """Initialise le gestionnaire de persistance en ouvrant la base de données des joueurs."""
        self.db_joueurs = TinyDB("data/players/joueurs_db.json")

# SAUVEGARDE ET CHARGEMENT DES JOUEURS

    def sauvegarder_joueur(self, p_joueur_modele: Joueur) -> None:
        """Enregistre un joueur dans la base de données JSON.

        Args:
            p_joueur_modele (Joueur): Instance de la classe Joueur contenant les informations du joueur.
        """
        d_donnees_joueur = {
            "identifiant_national_echec": p_joueur_modele.identifiant_national_echec,
            "nom_famille": p_joueur_modele.nom_famille,
            "prenom": p_joueur_modele.prenom,
            "date_naissance": p_joueur_modele.date_naissance,
        }
        self.db_joueurs.insert(d_donnees_joueur)

#
    def charger_joueurs(self) -> list[dict[str, str | int]]:
        """Charge tous les joueurs depuis la base de données TinyDB.

        Récupère les joueurs stockés dans la table `_default` de TinyDB,
        ajoute leur `doc_id` (ID interne TinyDB), et retourne une liste de dictionnaires
        contenant ces informations.

        Returns:
            list[dict[str, str | int]]: Une liste de dictionnaires où chaque dictionnaire
            représente un joueur avec son ID TinyDB et ses informations personnelles.
        """
        joueurs = self.db_joueurs.table('_default').all()
        joueurs_avec_ids = []

        for joueur in joueurs:
            # Récupérer le doc_id lié à chaque joueur
            doc_id = joueur.doc_id
            joueurs_avec_ids.append({
                "id_tinydb": doc_id,  # ID interne à TinyDB
                **joueur  # Les autres données du joueur
            })

        return joueurs_avec_ids

# SAUVEGARDE ET CHARGEMENT DES TOURNOIS

    def sauvegarder_tournoi(self, p_tournoi_modele: Tournoi) -> None:
        """Sauvegarde un tournoi dans un fichier JSON spécifique.

        Args:
            p_tournoi_modele (Tournoi): Objet contenant les informations du tournoi.
        """
        d_donnees_tournoi = {
            "nom_tournoi": p_tournoi_modele.nom_tournoi,
            "lieu_tournoi": p_tournoi_modele.lieu_tournoi,
            "date_debut_tournoi": p_tournoi_modele.date_debut_tournoi,
            "date_fin_tournoi": p_tournoi_modele.date_fin_tournoi,
            "nombre_tours": p_tournoi_modele.nombre_tours,
            "description": p_tournoi_modele.description,
        }
        self.db_tournois = TinyDB(
            f"data/tournaments/tournoi_{p_tournoi_modele.identifiant}.json"
        )
        self.db_tournois.insert(d_donnees_tournoi)

#
    def sauvegarder_joueurs_tournoi(self, p_tournoi_modele: Tournoi) -> None:
        """Sauvegarde la liste des joueurs associés à un tournoi.

        Args:
            p_tournoi_modele (Tournoi): Objet contenant les informations du tournoi et la liste des joueurs.
        """
        d_liste_joueurs_db_tournoi = {
            "liste_joueurs": p_tournoi_modele.liste_joueurs,
        }
        self.db_tournois = TinyDB(
            f"data/tournaments/tournoi_{p_tournoi_modele.identifiant}.json"
        )
        self.db_tournois.update(d_liste_joueurs_db_tournoi, doc_ids=[int(1)])

#
    def charger_tournoi(self, p_identifiant_tournoi: str) -> list[dict[str, str]]:
        """Charge les données d'un tournoi depuis son fichier JSON.
        Args:
            p_identifiant_tournoi (str): Identifiant du tournoi utilisé pour retrouver son fichier.
        Returns:
            list[dict[str, str]]: Liste contenant un dictionnaire avec toutes les informations du tournoi.
        """

        self.db_tournois = TinyDB(
            f"data/tournaments/tournoi_{p_identifiant_tournoi}.json"
        )
        return self.db_tournois.all()

#
    def lister_tournois(self) -> list[str]:
        """Liste tous les fichiers JSON présents dans le dossier des tournois.

        Returns:
            list[str]: Liste des noms de fichiers de tournois présents dans le dossier 'data/tournaments'.
        """
        chemin_dossier = "data/tournaments"
        fichiers_tournois = []

        for tournoi in os.listdir(chemin_dossier):
            fichiers_tournois.append(tournoi)

        return fichiers_tournois
