from models.tournoi import Tournoi
from models.gestionnaire_persistance import GestionnairePersistance
from views.tournoi_vue import TournoiVue


class TournoiControleur:
    """Contrôleur gérant les interactions entre la vue et le modèle pour les tournois."""

    def __init__(self) -> None:
        """Initialise le contrôleur du tournoi avec la vue et le gestionnaire de persistance."""
        self.o_tournoi_vue = TournoiVue()
        self.o_gestionnaire_persistance = GestionnairePersistance()

#
    def ajouter_tournoi(self) -> None:
        """
        Gère l'ajout d'un nouveau tournoi en collectant les informations et en les sauvegardant.
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
        """Permet d'inscrire un ou plusieurs joueurs à un tournoi existant.

        Args:
            None

        Returns:
            None
        """

        # Récupère la liste des tournois existants depuis le fichier JSON.
        l_liste_tournois = self.o_gestionnaire_persistance.recuperer_fichiers_tournois()

        # # Affiche les tournois disponibles et demande à l'utilisateur d'en choisir un.
        i_identifiant_tournoi = self.o_tournoi_vue.render_choix_tournoi(
            l_liste_tournois
        )
        # Charge les données du tournoi sélectionné.
        o_tournoi_choisi = self.o_gestionnaire_persistance.recuperer_objet_tournoi(
            i_identifiant_tournoi
        )

        if not len(o_tournoi_choisi.liste_tours) == 0:
            self.o_tournoi_vue.render_impossible_inscription(o_tournoi_choisi.nom_tournoi)
            return

        # Récupère la liste des joueurs disponibles.
        l_liste_joueurs = self.o_gestionnaire_persistance.charger_joueurs()

        # Affiche les joueurs et demande à l'utilisateur de sélectionner ceux à inscrire.
        l_choix_joueur = self.o_tournoi_vue.render_choix_joueur(l_liste_joueurs, o_tournoi_choisi)

        # Met à jour la liste des joueurs du tournoi.
        o_tournoi_choisi.liste_joueurs = l_choix_joueur

        # Sauvegarde la mise à jour du tournoi dans la base de données.
        self.o_gestionnaire_persistance.sauvegarder_joueurs_tournoi(o_tournoi_choisi)

#
    def lister_tournois(self) -> None:
        """Affiche la liste des tournois enregistrés dans la base de données.

        Args:
            None

        Returns:
            None
        """

        # Charge la liste des tournois existants.
        l_liste_tournois = self.o_gestionnaire_persistance.recuperer_fichiers_tournois()

        # Affiche les informations de chaque tournoi dans la console.
        self.o_tournoi_vue.render_lister_tournois(l_liste_tournois)

#
    def visualiser_tournoi(self) -> None:
        """Affiche les détails d'un tournoi sélectionné par l'utilisateur.

        Args:
            None

        Returns:
            None
        """

        # Charge la liste des joueurs enregistrés.
        l_liste_joueurs = self.o_gestionnaire_persistance.charger_joueurs()

        # Charge la liste des tournois existants.
        l_liste_tournois = self.o_gestionnaire_persistance.recuperer_fichiers_tournois()

        # Affiche les tournois disponibles et demande à l'utilisateur d'en choisir un.
        i_identifiant_tournoi = self.o_tournoi_vue.render_choix_tournoi(
            l_liste_tournois
        )

        # Récupère les données du tournoi sélectionné.
        d_tournoi = self.o_gestionnaire_persistance.charger_tournoi(
            i_identifiant_tournoi
        )

        # Affiche les informations détaillées du tournoi, y compris les joueurs inscrits àce tournoi.
        self.o_tournoi_vue.render_visualiser_tournoi(d_tournoi, l_liste_joueurs)
