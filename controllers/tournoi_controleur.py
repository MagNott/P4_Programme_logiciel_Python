from models.tournoi import Tournoi
from models.gestionnaire_persistance import GestionnairePersistance
from views.tournoi_vue import TournoiVue
import re


class TournoiControleur:
    """Contrôleur gérant les interactions entre la vue et le modèle pour les tournois."""
    """
    Contrôleur gérant les interactions entre la vue et le modèle pour la gestion des tournois.

    Ce contrôleur fait le lien entre :
    - **La vue** (`TournoiVue`), qui affiche les informations.
    - **Le modèle** (`GestionnairePersistance`), qui gère la persistance des données.

    Cette classe assure :
    - L'ajout d'un nouveau tournoi et son enregistrement en base de données.
    - L'inscription de joueurs à un tournoi (si celui-ci n'a pas encore commencé).
    - L'affichage de la liste des tournois enregistrés.
    - La visualisation détaillée d'un tournoi, y compris les matchs et les joueurs.

    """

    def __init__(self) -> None:
        """
        Initialise le contrôleur du tournoi avec la vue et le gestionnaire de persistance
        pour la gestion des tournois.
        """

        self.o_tournoi_vue = TournoiVue()
        self.o_gestionnaire_persistance = GestionnairePersistance()

#
    def ajouter_tournoi(self) -> None:
        """
        Gère l'ajout d'un nouveau tournoi en collectant les informations et en les sauvegardant.

        Cette méthode génère un identifiant unique pour le tournoi.
        Demande à l'utilisateur de saisir les informations via la vue puis
        Crée un objet `Tournoi` avec ces informations.
        Ensuite, elle Sauvegarde le tournoi dans la base de données et
        affiche un message de confirmation avec les détails du tournoi.

            Args:
                None

            Returns:
                None
        """

        # Génère un identifiant unique pour le tournoi.
        identifiant_tournoi = Tournoi.generer_identifiant()

        # Demande à l'utilisateur de saisir les informations du tournoi via la vue.
        d_infos_tournoi = self.o_tournoi_vue.render_saisie_tournoi()

        # Crée un objet `Tournoi` avec ces informations.
        o_tournoi_modele = Tournoi(
            identifiant_tournoi,
            d_infos_tournoi["p_nom_tournoi"],
            d_infos_tournoi["p_lieu_tournoi"],
            d_infos_tournoi["p_date_debut_tournoi"],
            d_infos_tournoi["p_date_fin_tournoi"],
            d_infos_tournoi["p_nombre_tour_tournoi"],
            d_infos_tournoi["p_description_tournoi"],
            [],  # initialise à liste tour vide
            []  # initialise à liste joueur vide
        )

        # Sauvegarde le tournoi dans le gestionnaire de persistance.
        self.o_gestionnaire_persistance.sauvegarder_tournoi(o_tournoi_modele)

        # Affiche un message de confirmation avec les informations du tournoi.
        self.o_tournoi_vue.render_confirm_ajout_tournoi(**d_infos_tournoi)
        # Les ** permettent de déballer le dictionnaire

#
    def inscrire_joueur(self) -> None:
        """
        Permet d'inscrire un ou plusieurs joueurs à un tournoi existant si celui_ci n'a pas commencé.

        Cette méthode charge la liste des tournois disponibles et demande à l'utilisateur d'en choisir un.
        Vérifie que le tournoi n'a pas encore commencé (aucun tour enregistré) puis
        charge la liste des joueurs disponibles et permet à l'utilisateur d'en sélectionner plusieurs.
        Esnuite, elle met à jour la liste des joueurs du tournoi avec leurs scores initiaux (0) et
        Sauvegarde les informations du tournoi mises à jour dans la base de données.

        Args:
            None

        Returns:
            None
        """

        # Récupère la liste des tournois existants depuis le fichier JSON
        l_liste_tournois = self.o_gestionnaire_persistance.recuperer_fichiers_tournois()

        # # Affiche les tournois disponibles et demande à l'utilisateur d'en choisir un
        i_identifiant_tournoi = self.o_tournoi_vue.render_choix_tournoi(
            l_liste_tournois
        )
        # Charge les données du tournoi sélectionné
        o_tournoi_choisi = self.o_gestionnaire_persistance.recuperer_objet_tournoi(
            i_identifiant_tournoi
        )

        # Vérifie si le tournoi a déjà commencé pour empecher l'inscription des joueurs
        if not len(o_tournoi_choisi.liste_tours) == 0:
            self.o_tournoi_vue.render_impossible_inscription(o_tournoi_choisi.nom_tournoi)
            return

        # Récupère la liste des joueurs disponibles
        l_liste_joueurs = self.o_gestionnaire_persistance.charger_joueurs()

        # Affiche les joueurs et demande à l'utilisateur de sélectionner ceux à inscrire
        l_choix_joueurs = self.o_tournoi_vue.render_choix_joueur(l_liste_joueurs, o_tournoi_choisi)

        # Construit un dicitonnaire qui va servir de liste de joueur mais avec leurs scores
        d_joueurs_choisis = {}
        for choix_joueur in l_choix_joueurs:
            d_joueurs_choisis[choix_joueur] = 0

        # Met à jour le dictionnaire des joueurs du tournoi
        o_tournoi_choisi.liste_joueurs = d_joueurs_choisis

        print(o_tournoi_choisi.liste_joueurs)

        # Sauvegarde la mise à jour du tournoi dans la base de données
        self.o_gestionnaire_persistance.sauvegarder_joueurs_tournoi(o_tournoi_choisi)

#
    def lister_tournois(self) -> None:
        """
        Affiche la liste des tournois enregistrés dans la base de données (JSON).

        Cette méthode charge la liste des fichiers de tournois existants.
        Extrait les informations de chaque tournoi et
        affiche ces informations sous forme de tableau via la vue.

        Args:
            None

        Returns:
            None
        """

        # Charge la liste des tournois existants
        l_liste_tournois = self.o_gestionnaire_persistance.recuperer_fichiers_tournois()

        regex = r"tournoi_(\d+)_"
        l_objets_tournoi = []
        for s_tournoi in l_liste_tournois:
            match = re.match(regex, s_tournoi)
            if match:
                i_identifiant_tournoi = match.group(1)
                l_objets_tournoi.append(self.o_gestionnaire_persistance.recuperer_objet_tournoi(i_identifiant_tournoi))

        # Affiche les informations de chaque tournoi dans la console
        self.o_tournoi_vue.render_lister_tournois(l_objets_tournoi)

#
    def visualiser_tournoi(self) -> None:
        """
        Affiche les détails d'un tournoi sélectionné par l'utilisateur.

        Cette méthode charge la liste des tournois existants et demande à l'utilisateur d'en choisir un.
        Récupère les détails du tournoi sélectionné, y compris les scores des joueurs et
        affiche ces informations de manière détaillée via la vue.

        Args:
            None

        Returns:
            None
        """

        # Charge la liste des tournois existants.
        l_liste_tournois = self.o_gestionnaire_persistance.recuperer_fichiers_tournois()

        # Affiche les tournois disponibles et demande à l'utilisateur d'en choisir un.
        i_identifiant_tournoi = self.o_tournoi_vue.render_choix_tournoi(
            l_liste_tournois
        )

        o_tournoi = self.o_gestionnaire_persistance.recuperer_objet_tournoi(i_identifiant_tournoi)

        d_scores_joueurs = self.o_gestionnaire_persistance.recuepere_score_joueurs(i_identifiant_tournoi)

        # Affiche les informations détaillées du tournoi, y compris les joueurs inscrits àce tournoi.
        self.o_tournoi_vue.render_visualiser_tournoi(o_tournoi, d_scores_joueurs)

#
    def visualiser_tour_match_tournoi(self) -> None:
        """
        Affiche les détails d'un tournoi sélectionné par l'utilisateur.

        Cette méthode charge la liste des tournois et demande à l'utilisateur d'en choisir un.
        Récupère les informations du tournoi sélectionné,
        et affiche les détails des tours et des matchs de ce tournoi via la vue.

        Args:
            None

        Returns:
            None
        """

        # Charge la liste des tournois existants.
        l_liste_tournois = self.o_gestionnaire_persistance.recuperer_fichiers_tournois()

        # Affiche les tournois disponibles et demande à l'utilisateur d'en choisir un.
        i_identifiant_tournoi = self.o_tournoi_vue.render_choix_tournoi(
            l_liste_tournois
        )

        o_tournoi = self.o_gestionnaire_persistance.recuperer_objet_tournoi(i_identifiant_tournoi)

        # Affiche les informations détaillées du tournoi, y compris les joueurs inscrits àce tournoi.
        self.o_tournoi_vue.render_visualiser_tour_match_tournoi(o_tournoi)
