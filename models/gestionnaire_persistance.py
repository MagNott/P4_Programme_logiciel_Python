from tinydb import TinyDB
from models.tournoi import Tournoi
from models.joueur import Joueur
from models.tour import Tour
from models.match import Match
import os
from datetime import datetime
from icecream import ic


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
            "score": p_joueur_modele.score,
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
        joueurs = self.db_joueurs.table("_default").all()
        joueurs_avec_ids = []

        for joueur in joueurs:
            # Récupérer le doc_id lié à chaque joueur
            doc_id = joueur.doc_id
            joueurs_avec_ids.append(
                {
                    "id_tinydb": doc_id,  # ID interne à TinyDB
                    **joueur,  # Les autres données du joueur
                }
            )

        return joueurs_avec_ids

    def recuperer_objet_joueur(self, p_identifiant_joueur: str) -> Joueur:

        d_joueurs = self.db_joueurs.get(
            doc_id=int(p_identifiant_joueur)
        )  # Récupérer les données

        o_joueur = Joueur(
            p_identifiant_national_echec=d_joueurs["identifiant_national_echec"],
            p_nom_famille=d_joueurs["nom_famille"],
            p_prenom=d_joueurs["prenom"],
            p_date_naissance=d_joueurs["date_naissance"],
            p_identifiant_tinydb=p_identifiant_joueur,
            p_score=d_joueurs["score"],
        )

        return o_joueur

    #
    def mettre_a_jour_joueur(self, p_id_tinydb, p_score_gagne):

        # Vérifier si le joueur existe dans TinyDB
        joueur_trouve = self.db_joueurs.get(doc_id=p_id_tinydb)

        if joueur_trouve:
            # Ajouter le score au total existant
            score_final = joueur_trouve["score"] + p_score_gagne

            # Mettre à jour le score du joueur dans TinyDB
            self.db_joueurs.update({"score": score_final}, doc_ids=[int(p_id_tinydb)])

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
            "liste_joueurs": p_tournoi_modele.liste_joueurs,
            "liste_tours": p_tournoi_modele.liste_tours,
        }
        self.db_tournois = TinyDB(
            f"data/tournaments/tournoi_{p_tournoi_modele.identifiant}_{p_tournoi_modele.nom_tournoi}_{p_tournoi_modele.date_debut_tournoi}.json"
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
            f"data/tournaments/tournoi_{p_tournoi_modele.identifiant}_{p_tournoi_modele.nom_tournoi}_{p_tournoi_modele.date_debut_tournoi}.json"
        )
        self.db_tournois.update(d_liste_joueurs_db_tournoi, doc_ids=[int(1)])

    def trouver_fichier_par_identifiant(self, p_identifiant_tournoi):
        """Retourne la liste des fichiers commençant par un certain préfixe dans un dossier donné."""

        fichiers = os.listdir("data/tournaments")  # Liste tous les fichiers du dossier

        for fichier in fichiers:  # Boucle sur chaque fichier
            if fichier.startswith(f"tournoi_{p_identifiant_tournoi}_"):  # Vérifie si le fichier commence par le préfixe
                return f"data/tournaments/{fichier}"

    #
    def charger_tournoi(self, p_identifiant_tournoi: str) -> list[dict[str, str]]:
        """Charge les données d'un tournoi depuis son fichier JSON.
        Args:
            p_identifiant_tournoi (str): Identifiant du tournoi utilisé pour retrouver son fichier.
        Returns:
            list[dict[str, str]]: Liste contenant un dictionnaire avec toutes les informations du tournoi.
        """

        fichier_tournoi = self.trouver_fichier_par_identifiant(p_identifiant_tournoi)

        self.db_tournois = TinyDB(fichier_tournoi)
        return self.db_tournois.all()

    #
    def recuperer_objet_tournoi(self, p_identifiant_tournoi: str) -> Tournoi:
        """Récupère un tournoi sous forme d'objet Tournoi à partir de TinyDB.

        Args:
            p_identifiant_tournoi (str): L'identifiant du tournoi.

        Returns:
            Tournoi: L'objet Tournoi correspondant.
        """

        fichier_tournoi = self.trouver_fichier_par_identifiant(p_identifiant_tournoi)

        self.db_tournois = TinyDB(fichier_tournoi)

        d_tournoi = self.db_tournois.all()[0]  # Récupérer les données

        o_tournoi = Tournoi(
            p_identifiant=p_identifiant_tournoi,
            p_nom_tournoi=d_tournoi["nom_tournoi"],
            p_lieu_tournoi=d_tournoi["lieu_tournoi"],
            p_date_debut_tournoi=d_tournoi["date_debut_tournoi"],
            p_date_fin_tournoi=d_tournoi["date_fin_tournoi"],
            p_nombre_tours=d_tournoi["nombre_tours"],
            p_description=d_tournoi["description"],
            p_liste_joueurs=d_tournoi["liste_joueurs"],
        )
        o_tournoi.liste_tours = []
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
    def recuperer_fichiers_tournois(self) -> list[str]:
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
    def enregistrer_tour_tournoi(self, p_tour: Tour, p_tournoi_modele: Tournoi) -> None:
        """Ajoute un tour à un tournoi existant dans TinyDB.

        Args:
            p_tour (Tour): L'objet Tour à ajouter.
            p_tournoi (Tournoi): L'objet Tournoi dans lequel ajouter le tour.
        """
        self.db_tournois = TinyDB(
            f"data/tournaments/tournoi_{p_tournoi_modele.identifiant}_{p_tournoi_modele.nom_tournoi}_{p_tournoi_modele.date_debut_tournoi}.json"
        )

        # Charge les données actuelles du tournoi
        d_tournoi = self.db_tournois.all()[0]

        # Vérifie si "liste_tours" existe, sinon l'initialise
        if "liste_tours" not in d_tournoi:
            d_tournoi["liste_tours"] = []

        # Transforme chaque match en dictionnaire
        l_matchs_dictionnaire = []
        for o_match in p_tour.liste_matchs:
            d_match = {
                "identifiant": o_match.identifiant,
                "nom_match": o_match.nom_match,
                "joueur_blanc": o_match.joueur_blanc,
                "joueur_noir": o_match.joueur_noir,
                "statut": o_match.statut,
            }
            l_matchs_dictionnaire.append(d_match)

        # Transforme l'objet Tour en dictionnaire
        d_nouveau_tour = {
            "identifiant": p_tour.identifiant,
            "nom": p_tour.nom,
            "statut": p_tour.statut,
            "liste_matchs": l_matchs_dictionnaire,
            "date_heure_debut": p_tour.date_heure_debut,
            "date_heure_fin": p_tour.date_heure_fin,
        }

        # Ajoute ce tour aux données du tournoi
        d_tournoi["liste_tours"].append(d_nouveau_tour)

        # Met à jour le tournoi dans TinyDB
        self.db_tournois.update(d_tournoi, doc_ids=[1])

    #
    def recuperer_dernier_tour(self, p_identifiant_tournoi: str) -> dict:
        """
        Récupère le dernier tour d'un tournoi à partir de la base de données.

        Args:
            p_identifiant_tournoi (str): L'identifiant du tournoi dont on veut récupérer le dernier tour.

        Returns:
            dict: Un dictionnaire contenant les informations du dernier tour du tournoi.
        """

        fichier_tournoi = self.trouver_fichier_par_identifiant(p_identifiant_tournoi)

        self.db_tournois = TinyDB(fichier_tournoi)

        d_tournoi = self.db_tournois.all()[0]

        d_dernier_tour = d_tournoi.get("liste_tours")[-1]

        return d_dernier_tour

    #
    def recuperer_liste_objets_matchs(self, p_dernier_tour: dict) -> list[Match]:
        """
        Convertit une liste de dictionnaires représentant des matchs en une liste d'objets Match.

        Args:
            p_dernier_tour (dict): Un dictionnaire contenant les informations du dernier tour,
                                y compris la liste des matchs sous forme de dictionnaires.

        Returns:
            list[Match]: Une liste d'objets Match reconstitués à partir des données du dernier tour.
        """
        l_objects_matchs = []

        for d_match in p_dernier_tour.get("liste_matchs", []):
            # Création de l'objet Match
            o_match = Match(
                p_identifiant=d_match["identifiant"],
                p_joueur_blanc=d_match["joueur_blanc"],
                p_joueur_noir=d_match["joueur_noir"],
                p_score_blanc=d_match.get("score_blanc", 0),
                p_score_noir=d_match.get("score_noir", 0),
                p_statut=d_match["statut"],
            )
            l_objects_matchs.append(o_match)

        return l_objects_matchs

    #
    def enregistrer_resultat_match(self, p_resultats, p_identifiant_tournoi):
        """
        Enregistre les résultats des matchs d'un tour et met à jour les scores des joueurs.

        Cette fonction met à jour les informations du dernier tour d'un tournoi en enregistrant
        les résultats des matchs, en mettant à jour les scores des joueurs, et en clôturant le tour
        en ajoutant la date et l'heure de fin.

        Args:
            p_resultats (list[dict]): Liste des résultats des matchs sous forme de dictionnaires,
                                    contenant `score_blanc`, `score_noir`, et `statut`.
            p_identifiant_tournoi (str): Identifiant unique du tournoi concerné.

        Returns:
            None: Met à jour la base de données, mais ne retourne pas de valeur.
        """

        fichier_tournoi = self.trouver_fichier_par_identifiant(p_identifiant_tournoi)

        self.db_tournois = TinyDB(fichier_tournoi)

        # Charge les données actuelles du tournoi
        d_tournoi = self.db_tournois.all()[0]

        # Met à jour les informations des matchs (scores et statut).
        # Transforme chaque match en dictionnaire
        for i, d_resultat in enumerate(p_resultats):
            d_match = {
                "score_blanc": d_resultat["score_blanc"],
                "score_noir": d_resultat["score_noir"],
                "statut": d_resultat["statut"],
            }
            d_liste_match = d_tournoi["liste_tours"][-1]["liste_matchs"][i]
            # Pour insérer les données au bon endroit dans le JSON, fusion des 2 dictionnaires
            # avec ** pour déballer les informations
            d_nouvelle_liste_match = {**d_liste_match, **d_match}
            d_tournoi["liste_tours"][-1]["liste_matchs"][i] = d_nouvelle_liste_match

            # Met à jour les scores des joueurs dans la base de données.
            self.mettre_a_jour_joueur(
                d_liste_match["joueur_blanc"], d_resultat["score_blanc"]
            )
            self.mettre_a_jour_joueur(
                d_liste_match["joueur_blanc"], d_resultat["score_noir"]
            )

        # Marque le tour comme "Terminé" et enregistre l'heure de fin.
        d_tournoi["liste_tours"][-1]["statut"] = "Terminé"
        d_tournoi["liste_tours"][-1]["date_heure_fin"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Sauvegarde les modifications dans TinyDB.
        self.db_tournois.update(d_tournoi, doc_ids=[1])
