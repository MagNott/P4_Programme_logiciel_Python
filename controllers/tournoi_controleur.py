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
        """Gère l'ajout d'un nouveau tournoi en collectant les informations et en les sauvegardant.

        Cette méthode :
        1. Génère un identifiant unique pour le tournoi.
        2. Demande à l'utilisateur de saisir les informations du tournoi via la vue.
        3. Crée un objet `Tournoi` avec ces informations.
        4. Sauvegarde le tournoi dans le gestionnaire de persistance.
        5. Affiche un message de confirmation avec les informations du tournoi.
        """

        identifiant_tournoi = Tournoi.generer_identifiant()

        d_infos_tournoi = self.o_tournoi_vue.render_saisie_tournoi()
        o_tournoi_modele = Tournoi(
            identifiant_tournoi,
            d_infos_tournoi["p_nom_tournoi"],
            d_infos_tournoi["p_lieu_tournoi"],
            d_infos_tournoi["p_date_debut_tournoi"],
            d_infos_tournoi["p_date_fin_tournoi"],
            d_infos_tournoi["p_nombre_tour_tournoi"],
            d_infos_tournoi["p_description_tournoi"],
        )

        self.o_gestionnaire_persistance.sauvegarder_tournoi(o_tournoi_modele)
        # Les ** permettent de déballer le dictionnaire
        self.o_tournoi_vue.render_confirm_ajout_tournoi(**d_infos_tournoi)

#
    def inscrire_joueur(self) -> None:
        """Permet d'inscrire un ou plusieurs joueurs à un tournoi existant.

        Cette méthode suit les étapes suivantes :
        1. Récupère la liste des tournois existants depuis le fichier JSON.
        2. Affiche les tournois disponibles et demande à l'utilisateur d'en choisir un.
        3. Charge les données du tournoi sélectionné.
        4. Récupère la liste des joueurs disponibles.
        5. Affiche les joueurs et demande à l'utilisateur de sélectionner ceux à inscrire.
        6. Met à jour la liste des joueurs du tournoi.
        7. Sauvegarde la mise à jour du tournoi dans la base de données.
        """

        l_liste_tournois = self.o_gestionnaire_persistance.lister_tournois()
        i_identifiant_tournoi = self.o_tournoi_vue.render_choix_tournoi(
            l_liste_tournois
        )
        a_tournoi_choisi_data = self.o_gestionnaire_persistance.charger_tournoi(
            i_identifiant_tournoi
        )

        o_tournoi_choisi = Tournoi(
            p_identifiant=i_identifiant_tournoi,
            p_nom_tournoi=a_tournoi_choisi_data[0]["nom_tournoi"],
            p_lieu_tournoi=a_tournoi_choisi_data[0]["lieu_tournoi"],
            p_date_debut_tournoi=a_tournoi_choisi_data[0]["date_debut_tournoi"],
            p_date_fin_tournoi=a_tournoi_choisi_data[0]["date_fin_tournoi"],
            p_nombre_tours=a_tournoi_choisi_data[0]["nombre_tours"],
            p_description=a_tournoi_choisi_data[0]["description"],
        )

        l_liste_joueurs = self.o_gestionnaire_persistance.charger_joueurs()
        l_choix_joueur = self.o_tournoi_vue.render_choix_joueur(l_liste_joueurs)

        o_tournoi_choisi.liste_joueurs = l_choix_joueur
        self.o_gestionnaire_persistance.sauvegarder_joueurs_tournoi(o_tournoi_choisi)

#
    def lister_tournois(self) -> None:
        """Affiche la liste des tournois enregistrés dans la base de données.

        Cette méthode suit les étapes suivantes :
        1. Charge la liste des tournois existants.
        2. Affiche les informations de chaque tournoi dans la console.
        """

        l_liste_tournois = self.o_gestionnaire_persistance.lister_tournois()
        self.o_tournoi_vue.render_lister_tournois(l_liste_tournois)

#
    def visualiser_tournoi(self) -> None:
        """Affiche les détails d'un tournoi sélectionné par l'utilisateur.

        Cette méthode suit les étapes suivantes :
        1. Charge la liste des joueurs enregistrés.
        2. Charge la liste des tournois existants.
        3. Affiche les tournois disponibles et demande à l'utilisateur d'en choisir un.
        4. Récupère les données du tournoi sélectionné.
        5. Affiche les informations détaillées du tournoi, y compris les joueurs inscrits àce tournoi.
        """

        l_liste_joueurs = self.o_gestionnaire_persistance.charger_joueurs()
        l_liste_tournois = self.o_gestionnaire_persistance.lister_tournois()
        i_identifiant_tournoi = self.o_tournoi_vue.render_choix_tournoi(
            l_liste_tournois
        )
        d_tournoi = self.o_gestionnaire_persistance.charger_tournoi(
            i_identifiant_tournoi
        )
        self.o_tournoi_vue.render_visualiser_tournoi(d_tournoi, l_liste_joueurs)
