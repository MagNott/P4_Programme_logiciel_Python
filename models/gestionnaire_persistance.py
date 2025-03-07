from tinydb import TinyDB
from models.tournoi import Tournoi
from models.joueur import Joueur
from models.tour import Tour
from models.match import Match
from datetime import datetime
from pathlib import Path
import shutil


class GestionnairePersistance:
    """Gère la persistance des données des joueurs et des tournois avec TinyDB."""

    """
    Gère la persistance des données des joueurs et des tournois avec TinyDB.

    Cette classe permet d'enregistrer, de charger et de gérer les données 
    des joueurs et des tournois dans des fichiers JSON. Elle assure également 
    la création et la gestion des dossiers de stockage.
    """

    def __init__(self):
        """
        Initialise le gestionnaire de persistance et crée les dossiers nécessaires.

        Cette méthode initialise la base de données des joueurs et configure les
        chemins des dossiers de stockage pour les tournois, les joueurs et les sauvegardes.
        Si les dossiers n'existent pas, ils sont créés automatiquement.

        Attributs créés:
            db_joueurs (TinyDB): Base de données TinyDB stockant les informations des joueurs.
            dossier_projet (Path): Chemin racine du projet.
            dossier_source (Path): Dossier contenant toutes les données du projet.
            dossier_tournois (Path): Dossier dédié au stockage des fichiers des tournois.
            dossier_joueurs (Path): Dossier dédié au stockage des fichiers des joueurs.
            dossier_sauvegarde (Path): Dossier utilisé pour stocker les sauvegardes.
        """
        self.db_joueurs = TinyDB("data/players/joueurs_db.json")

        """Initialise les chemins des fichiers"""
        self.dossier_projet = Path(__file__).parent.parent  # Racine du projet
        self.dossier_source = (
            self.dossier_projet / "data"
        )  # Dossier principal des données
        self.dossier_tournois = self.dossier_source / "tournaments"
        self.dossier_joueurs = self.dossier_source / "players"
        self.dossier_sauvegarde = self.dossier_projet / "sauvegarde"

        # S'assure que les dossiers existent
        self.dossier_source.mkdir(parents=True, exist_ok=True)
        self.dossier_tournois.mkdir(parents=True, exist_ok=True)
        self.dossier_joueurs.mkdir(parents=True, exist_ok=True)
        self.dossier_sauvegarde.mkdir(parents=True, exist_ok=True)

    #
    # SAUVEGARDE ET CHARGEMENT DES JOUEURS

    def sauvegarder_joueur(self, p_joueur_modele: Joueur) -> None:
        """
        Enregistre un joueur dans la base de données JSON avec TinyDB.

        Cette fonction extrait les informations du joueur depuis l'objet `Joueur`
        et les insère dans la base de données `joueurs_db.json`.

        Args:
            p_joueur_modele (Joueur): Instance de la classe `Joueur` contenant les informations du joueur.

        Returns:
            None: Met à jour la base de données mais ne retourne pas de valeur.
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
    def charger_joueurs(self) -> list[dict]:
        """Charge tous les joueurs depuis la base de données TinyDB et
        les retourne sous forme de liste de dictionnaire.

        Récupère les joueurs stockés dans la table `_default` de TinyDB,
        ajoute leur `doc_id` (ID interne TinyDB), et retourne une liste de dictionnaires
        contenant ces informations.

        Returns:
            list[dict]: Une liste de dictionnaires où chaque dictionnaire
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

    #
    def recuperer_objet_joueur(self, p_identifiant_joueur: str) -> Joueur:
        """
        Récupère un joueur sous forme d'objet `Joueur` à partir du fichier JSON Joueur.

        Cette fonction recherche un joueur dans la base de données en fonction de son
        identifiant TinyDB, puis reconstruit un objet `Joueur` à partir des informations
        trouvées.

        Args:
            p_identifiant_joueur (str): Identifiant du joueur dans la base de données TinyDB.

        Returns:
            Joueur: L'objet `Joueur` correspondant aux données stockées.
        """

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
    # SAUVEGARDE ET CHARGEMENT DES TOURNOIS

    def sauvegarder_tournoi(self, p_tournoi_modele: Tournoi) -> None:
        """
        Sauvegarde un tournoi dans un fichier JSON spécifique.

        Cette fonction stocke toutes les informations du tournoi dans un fichier
        JSON unique sous `data/tournaments/`.

        Args:
            p_tournoi_modele (Tournoi): Objet `Tournoi` contenant les informations du tournoi.

        Returns:
            None: Met à jour la base de données mais ne retourne pas de valeur.
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

        # Utilisation de variables intermédiaire pour réduire la taille de la fstring
        identifiant = p_tournoi_modele.identifiant
        nom = p_tournoi_modele.nom_tournoi
        date_debut = p_tournoi_modele.date_debut_tournoi

        fichier_tournoi = (
            self.dossier_tournois / f"tournoi_{identifiant}_{nom}_{date_debut}.json"
        )

        self.db_tournois = TinyDB(str(fichier_tournoi))
        self.db_tournois.insert(d_donnees_tournoi)

    #
    def sauvegarder_joueurs_tournoi(self, p_tournoi_modele: Tournoi) -> None:
        """
        Sauvegarde la liste des joueurs associés à un tournoi dans le fichier JSON du tournoi.

        Cette fonction met à jour le fichier JSON du tournoi en ajoutant ou modifiant
        la liste des joueurs inscrits.

        Args:
            p_tournoi_modele (Tournoi): Objet `Tournoi` contenant les informations du tournoi
                                        et la liste des joueurs.

        Returns:
            None: Met à jour le fichier du tournoi mais ne retourne pas de valeur.
        """

        d_liste_joueurs_db_tournoi = {
            "liste_joueurs": p_tournoi_modele.liste_joueurs,
        }

        # Utilisation de variables intermédiaire pour réduire la taille de la fstring
        identifiant = p_tournoi_modele.identifiant
        nom = p_tournoi_modele.nom_tournoi
        date_debut = p_tournoi_modele.date_debut_tournoi

        self.db_tournois = TinyDB(
            f"data/tournaments/tournoi_{identifiant}_{nom}_{date_debut}.json"
        )

        self.db_tournois.update(d_liste_joueurs_db_tournoi, doc_ids=[int(1)])

    #
    def recuperer_objet_tournoi(self, p_identifiant_tournoi: str) -> Tournoi:
        """Récupère un tournoi sous forme d'objet Tournoi à partir de TinyDB.
        Cette fonction charge les informations du tournoi depuis son fichier JSON,
        reconstruit un objet `Tournoi` et y associe les objets `Tour`, `Match` et `Joueur`.

        Args:
            p_identifiant_tournoi (str): L'identifiant du tournoi à recupérer.

        Returns:
            Tournoi: L'objet Tournoi recontruit avec tous ses tours et ses matchs associés.
        """

        fichier_tournoi = self._trouver_fichier_par_identifiant(p_identifiant_tournoi)

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
        for d_tour in d_tournoi["liste_tours"]:
            # Créer un objet Tour pour chaque tour et l'ajouter à la liste des tours du tournoi
            o_tour = Tour(
                p_identifiant=d_tour["identifiant"],
                p_nom=d_tour["nom"],
                p_tournoi=o_tournoi,
                p_statut=d_tour["statut"],
                p_date_heure_debut=d_tour["date_heure_debut"],
                p_date_heure_fin=d_tour["date_heure_fin"],
            )

            o_tour.liste_match = []
            for match in d_tour["liste_matchs"]:
                o_match = Match(
                    p_identifiant=match["identifiant"],
                    p_joueur_blanc=self.recuperer_objet_joueur(match["joueur_blanc"]),
                    p_joueur_noir=self.recuperer_objet_joueur(match["joueur_noir"]),
                    p_score_blanc=match.get("score_blanc", 0.0),
                    p_score_noir=match.get("score_noir", 0.0),
                    p_statut=match["statut"],
                )
                o_tour.liste_matchs.append(o_match)

            o_tournoi.liste_tours.append(o_tour)

        o_tournoi.liste_joueurs = []
        for i_joueur in d_tournoi["liste_joueurs"]:
            o_joueur = self.recuperer_objet_joueur(i_joueur)

            o_tournoi.liste_joueurs.append(o_joueur)

        return o_tournoi

    #
    def recuperer_fichiers_tournois(self) -> list[str]:
        """Liste tous les fichiers JSON présents dans le dossier des tournois.

        Returns:
            list[str]: Liste des noms de fichiers de tournois présents dans le dossier 'data/tournaments'.
        """
        # chemin_dossier = "data/tournaments"
        fichiers_tournois = []

        for tournoi in sorted(self.dossier_tournois.iterdir()):
            if tournoi.is_file():
                fichiers_tournois.append(tournoi.name)

        return fichiers_tournois

    #
    def enregistrer_tour_tournoi(
        self, p_objet_tour: Tour, p_objet_tournoi: Tournoi
    ) -> None:
        """Ajoute un tour à un tournoi existant et met à jour le fichier JSON.

        Args:
            p_objet_tour (Tour): L'objet Tour à ajouter.
            p_objet_tournoi (Tournoi): L'objet Tournoi dans lequel ajouter le tour.

        Returns:
            None: Met à jour le fichier JSON mais ne retourne pas de valeur.
        """

        # Utilisation de variables intermédiaire pour réduire la taille de la fstring
        identifiant = p_objet_tournoi.identifiant
        nom = p_objet_tournoi.nom_tournoi
        date_debut = p_objet_tournoi.date_debut_tournoi

        fichierTournoi = (
            self.dossier_tournois
            / f"tournoi_{identifiant}_{nom}_{date_debut}.json"
        )
        self.db_tournois = TinyDB(str(fichierTournoi))

        # Charge les données actuelles du tournoi
        d_tournoi = self.db_tournois.all()[0]

        # Vérifie si "liste_tours" existe, sinon l'initialise
        if "liste_tours" not in d_tournoi:
            d_tournoi["liste_tours"] = []

        # Transforme chaque match en dictionnaire
        l_matchs_dictionnaire = []
        for o_match in p_objet_tour.liste_matchs:
            d_match = {
                "identifiant": o_match.identifiant,
                "nom_match": o_match.nom_match,
                "joueur_blanc": o_match.joueur_blanc.identifiant_tinydb,
                "joueur_noir": o_match.joueur_noir.identifiant_tinydb,
                "statut": o_match.statut,
            }
            l_matchs_dictionnaire.append(d_match)

        # Transforme l'objet Tour en dictionnaire
        d_nouveau_tour = {
            "identifiant": p_objet_tour.identifiant,
            "nom": p_objet_tour.nom,
            "statut": p_objet_tour.statut,
            "liste_matchs": l_matchs_dictionnaire,
            "date_heure_debut": p_objet_tour.date_heure_debut,
            "date_heure_fin": p_objet_tour.date_heure_fin,
        }

        # Ajoute ce tour aux données du tournoi
        d_tournoi["liste_tours"].append(d_nouveau_tour)

        # Met à jour le tournoi dans TinyDB
        self.db_tournois.update(d_tournoi, doc_ids=[1])

    #
    def recuperer_dernier_tour(self, p_identifiant_tournoi: str) -> dict:
        """
        Récupère le dernier tour d'un tournoi à partir de son fichier JSON.

        Args:
            p_identifiant_tournoi (str): L'identifiant du tournoi dont on veut récupérer le dernier tour.

        Returns:
            dict: Un dictionnaire contenant les informations du dernier tour du tournoi
                  y compris la liste des matchs joués.
        """

        fichier_tournoi = self._trouver_fichier_par_identifiant(p_identifiant_tournoi)
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
        l_objets_matchs = []

        for d_match in p_dernier_tour.get("liste_matchs", []):
            # Création de l'objet Match
            o_match = Match(
                p_identifiant=d_match["identifiant"],
                p_joueur_blanc=self.recuperer_objet_joueur(d_match["joueur_blanc"]),
                p_joueur_noir=self.recuperer_objet_joueur(d_match["joueur_noir"]),
                p_score_blanc=d_match.get("score_blanc", 0),
                p_score_noir=d_match.get("score_noir", 0),
                p_statut=d_match["statut"],
            )
            l_objets_matchs.append(o_match)
            print(o_match)

        return l_objets_matchs

    #
    def enregistrer_resultat_match(
        self, p_resultats: list[dict], p_identifiant_tournoi: str
    ) -> None:
        """
        Enregistre les résultats des matchs d'un tour et met à jour les scores des joueurs.

        Cette fonction met à jour les informations du dernier tour d'un tournoi en enregistrant
        les résultats des matchs, en mettant à jour les scores des joueurs, et en clôturant le tour
        en ajoutant la date et l'heure de fin.

        Args:
            p_resultats (list[dict]): Liste des résultats des matchs sous forme de dictionnaires,
                                    contenant `score_blanc` (float), `score_noir` (float), et `statut` (str).
            p_identifiant_tournoi (str): Identifiant unique du tournoi concerné.

        Returns:
            None: Met à jour la base de données, mais ne retourne pas de valeur.
        """

        fichier_tournoi = self._trouver_fichier_par_identifiant(p_identifiant_tournoi)

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
            self._mettre_a_jour_joueur(
                d_liste_match["joueur_blanc"], d_resultat["score_blanc"]
            )
            self._mettre_a_jour_joueur(
                d_liste_match["joueur_noir"], d_resultat["score_noir"]
            )

            d_tournoi["liste_joueurs"][d_liste_match["joueur_blanc"]] += d_resultat[
                "score_blanc"
            ]
            d_tournoi["liste_joueurs"][d_liste_match["joueur_noir"]] += d_resultat[
                "score_noir"
            ]

        # Marque le tour comme "Terminé" et enregistre l'heure de fin.
        d_tournoi["liste_tours"][-1]["statut"] = "Terminé"
        d_tournoi["liste_tours"][-1]["date_heure_fin"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Sauvegarde les modifications dans TinyDB.
        self.db_tournois.update(d_tournoi, doc_ids=[1])

    #
    def recuepere_score_joueurs(self, p_identifiant_tournoi: str) -> dict:
        """
        Récupère les scores des joueurs d'un tournoi donné.

        Cette fonction recherche le fichier du tournoi correspondant à l'identifiant fourni,
        charge les données du tournoi depuis TinyDB et extrait les scores des joueurs.

        Args:
            p_identifiant_tournoi (str): Identifiant du tournoi dont on veut récupérer les scores.

        Returns:
            dict: Un dictionnaire contenant les scores des joueurs,
                  où la clé est l'identifiant du joueur et la valeur est son score.
        """

        fichier_tournoi = self._trouver_fichier_par_identifiant(p_identifiant_tournoi)
        self.db_tournois = TinyDB(fichier_tournoi)
        d_tournoi = self.db_tournois.all()[0]

        d_scores = d_tournoi["liste_joueurs"]

        return d_scores

    #
    def effectuer_sauvegarde(self) -> tuple:
        """
        Effectue une sauvegarde complète des données du projet.

        Cette fonction copie le dossier `data/` dans un dossier de sauvegarde unique
        nommé `data_backup_YYYYMMDD_HHMMSS` sous `sauvegarde/`. Elle vérifie également
        l'existence du dossier `data/` avant de procéder.

        Returns:
            tuple:
                - Un message de succès ou d'erreur.
                - Une chaîne "success" si la sauvegarde réussit, sinon "error".
        """

        try:
            if not self.dossier_source.exists():
                message = (
                    "❌ Le dossier `data/` n'existe pas, impossible de sauvegarder."
                )
                return message, "error"

            # Générer un dossier unique pour la sauvegarde
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dossier_sauvegarde_unique = (
                self.dossier_sauvegarde / f"data_backup_{timestamp}"
            )

            # Copier `data/` dans `sauvegarde/`
            shutil.copytree(self.dossier_source, dossier_sauvegarde_unique)

            message = f"\n ✅ Sauvegarde réussie dans : {dossier_sauvegarde_unique }\n "
            return message, "success"

        except Exception as e:
            message = f"\n ❌ Erreur lors de la sauvegarde : {e}\n "
            return message, "error"

    #
    def restaurer_sauvegarde(self, p_nom_sauvegarde: str) -> tuple:
        """
        Restaure une sauvegarde précédemment créée.

        Cette fonction remplace le dossier `data/` actuel par une sauvegarde choisie.
        Si le dossier de sauvegarde n'existe pas, elle retourne un message d'erreur.

        Args:
            p_nom_sauvegarde (str): Nom du dossier de sauvegarde à restaurer.

        Returns:
            tuple:
                - Un message de succès ou d'erreur.
                - Une chaîne "success" si la restauration réussit, sinon "error".
        """

        try:
            dossier_sauvegarde_cible = self.dossier_sauvegarde / p_nom_sauvegarde

            if not dossier_sauvegarde_cible.exists():
                return "\n ❌ La sauvegarde choisie n'existe pas.\n ", "error"

            # Supprimer `data/` s'il existe
            if self.dossier_source.exists():
                shutil.rmtree(self.dossier_source)

            # Copier la sauvegarde dans `data/`
            shutil.copytree(dossier_sauvegarde_cible, self.dossier_source)

            return (
                f"\n ✅ Restauration réussie depuis : {p_nom_sauvegarde}\n ",
                "success",
            )

        except Exception as e:
            return f"\n ❌ Erreur lors de la restauration : {e}\n ", "error"

    #
    # METHODES PRIVEES
    #
    def _trouver_fichier_par_identifiant(
        self, p_identifiant_tournoi: str
    ) -> str | None:
        """
        Recherche un fichier tournoi correspondant à l'identifiant fourni.

        Cette fonction parcourt le dossier des tournois et cherche un fichier
        dont le nom commence par "tournoi_{p_identifiant_tournoi}_".
        Si un fichier correspondant est trouvé, son chemin est retourné sous forme de chaîne de caractère.

        Args:
            p_identifiant_tournoi (str): Identifiant unique du tournoi à rechercher.

        Returns:
            str | None: Le chemin du fichier tournoi trouvé, ou None si aucun fichier correspondant n'est trouvé.
        """

        for fichier in self.dossier_tournois.iterdir():
            if fichier.is_file() and fichier.name.startswith(
                f"tournoi_{p_identifiant_tournoi}_"
            ):
                return str(fichier)

        # Explicite le retour si aucun fichier n'est trouvé
        return None

    #
    def _mettre_a_jour_joueur(self, p_id_tinydb: int, p_score_gagne: float) -> None:
        """
        Met à jour le score d'un joueur dans dans le fichier JSON Joueur.

        Cette fonction récupère un joueur en fonction de son identifiant dans TinyDB,
        ajoute le score gagné à son score actuel, et met à jour la base de données.

        Args:
            p_id_tinydb (int): Identifiant du joueur dans la base de données TinyDB.
            p_score_gagne (float): Nombre de points à ajouter au score du joueur.

        Returns:
            None: Met à jour la base de données mais ne retourne pas de valeur.
        """
        # Vérifier si le joueur existe dans TinyDB
        joueur_trouve = self.db_joueurs.get(doc_id=p_id_tinydb)

        if joueur_trouve:
            # Ajouter le score au total existant
            score_final = joueur_trouve["score"] + p_score_gagne

            # Mettre à jour le score du joueur dans TinyDB
            self.db_joueurs.update({"score": score_final}, doc_ids=[int(p_id_tinydb)])
