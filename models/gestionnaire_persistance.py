from tinydb import TinyDB
from models.tournoi import Tournoi
from models.joueur import Joueur
from models.tour import Tour
from models.match import Match
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
    def recuperer_objet_tournoi(self, p_identifiant_tournoi: str) -> Tournoi:
        """Récupère un tournoi sous forme d'objet Tournoi à partir de TinyDB.

        Args:
            p_identifiant_tournoi (str): L'identifiant du tournoi.

        Returns:
            Tournoi: L'objet Tournoi correspondant.
        """
        self.db_tournois = TinyDB(f"data/tournaments/tournoi_{p_identifiant_tournoi}.json")

        d_tournoi = self.db_tournois.all()[0]  # Récupérer les données

        o_tournoi = Tournoi(
            p_identifiant=p_identifiant_tournoi,
            p_nom_tournoi=d_tournoi["nom_tournoi"],
            p_lieu_tournoi=d_tournoi["lieu_tournoi"],
            p_date_debut_tournoi=d_tournoi["date_debut_tournoi"],
            p_date_fin_tournoi=d_tournoi["date_fin_tournoi"],
            p_nombre_tours=d_tournoi["nombre_tours"],
            p_description=d_tournoi["description"],
            p_liste_joueurs=d_tournoi["liste_joueurs"]
        )

        for tour in d_tournoi["liste_tours"]:
            # Créer un objet Tour pour chaque tour et l'ajouter à la liste des tours du tournoi
            p_tour = Tour(
                p_identifiant=tour["identifiant"],
                p_nom=tour["nom"],
                p_tournoi=o_tournoi,
                p_statut=tour["statut"],
                p_date_heure_debut=tour["date_heure_debut"],
                p_date_heure_fin=tour["date_heure_fin"],
            )
            o_tournoi.liste_tours.append(p_tour)

        return o_tournoi

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

#
    def enregistrer_tour_tournoi(self, p_tour: Tour, p_tournoi: Tournoi) -> None:
        """Ajoute un tour à un tournoi existant dans TinyDB.

        Args:
            p_tour (Tour): L'objet Tour à ajouter.
            p_tournoi (Tournoi): L'objet Tournoi dans lequel ajouter le tour.
        """
        self.db_tournois = TinyDB(f"data/tournaments/tournoi_{p_tournoi.identifiant}.json")

        # Charger les données actuelles du tournoi
        d_tournoi = self.db_tournois.all()[0]

        # Vérifier si "liste_tours" existe, sinon l'initialiser
        if "liste_tours" not in d_tournoi:
            d_tournoi["liste_tours"] = []

        # Vérifier si "liste_tours" existe, sinon l'initialiser
        if "liste_tours" not in d_tournoi:
            d_tournoi["liste_tours"] = []

        # Transformer chaque match en dictionnaire
        l_matchs_dictionnaire = []
        for o_match in p_tour.liste_matchs:
            d_match = {
                "nom_match": o_match.nom_match,
                "joueur_blanc": o_match.joueur_blanc,
                "joueur_noir": o_match.joueur_noir,
            }
            l_matchs_dictionnaire.append(d_match)

        # Transformer l'objet Tour en dictionnaire
        d_nouveau_tour = {
            "identifiant": p_tour.identifiant,
            "nom": p_tour.nom,
            "statut": p_tour.statut,
            "liste_matchs": l_matchs_dictionnaire,
            "date_heure_debut": p_tour.date_heure_debut,
            "date_heure_fin": p_tour.date_heure_fin,
        }

        # Ajouter ce tour aux données du tournoi
        d_tournoi["liste_tours"].append(d_nouveau_tour)

        print("Données de liste_matchs avant enregistrement :", d_tournoi["liste_tours"][-1]["liste_matchs"])

        # Mettre à jour le tournoi dans TinyDB
        self.db_tournois.update(d_tournoi, doc_ids=[1])

#
    def recuperer_liste_objets_matchs(self, p_identifiant_tournoi: str) -> list[Match]:
        """Récupère les matchs sous forme d'objets Match à partir du fichier JSON d'un tournoi.

        Args:
            p_identifiant_tournoi (str): L'identifiant du tournoi dont on veut récupérer les matchs.

        Returns:
            list[Match]: Liste d'objets Match correspondant aux matchs enregistrés.
        """
        self.db_tournois = TinyDB(f"data/tournaments/tournoi_{p_identifiant_tournoi}.json")

        d_tournoi = self.db_tournois.all()[0]  # Charger les données du tournoi
        l_matchs = []  # Liste des objets Match

        # Parcourir tous les tours du tournoi
        for d_tour in d_tournoi.get("liste_tours", []):
            for d_match in d_tour.get("liste_matchs", []):
                # Création de l'objet Match
                o_match = Match(
                    p_identifiant=d_match["identifiant"],
                    p_nom_match=f"{d_match['identifiant']} - {d_match['joueur_blanc']} VS {d_match['joueur_noir']}",
                    p_joueur_noir=d_match["joueur_noir"],
                    p_score_blanc=d_match["score_blanc"],
                    p_score_noir=d_match["score_noir"],
                    p_statut=d_match["statut"]
                )
                l_matchs.append(o_match)  # Ajouter l'objet Match à la liste

        return l_matchs  # Retourner la liste des matchs
