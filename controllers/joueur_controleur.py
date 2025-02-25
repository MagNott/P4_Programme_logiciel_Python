from models.joueur import Joueur
from models.gestionnaire_persistance import GestionnairePersistance
from views.joueur_vue import JoueurVue


class JoueurControleur:
    """Gère les interactions entre la vue et le modèle pour les joueurs."""

    def __init__(self):
        """Initialise le contrôleur des joueurs avec la vue et le gestionnaire de persistance."""
        self.o_joueur_vue = JoueurVue()
        self.o_gestionnaire_persistance = GestionnairePersistance()

    #
    def ajouter_joueur(self) -> None:
        """Ajoute un joueur en demandant ses informations et en les enregistrant.

        Cette méthode récupère les informations d'un joueur via la vue,
        crée une instance de Joueur, puis la sauvegarde dans la base de données.
        et affiche une confirmation à l'utilisateur.

        Steps:
            1. Demande des informations à l'utilisateur via la vue.
            2. Crée un objet Joueur avec les données saisies.
            3. Sauvegarde le joueur dans la base de données.
            4. Affiche un message de confirmation.
            """

        d_infos_joueur = self.o_joueur_vue.render_saisie_joueur()

        o_joueur_modele = Joueur(
            d_infos_joueur["p_identifiant"],
            d_infos_joueur["p_nom"],
            d_infos_joueur["p_prenom"],
            d_infos_joueur["p_date_naissance"],
        )

        self.o_gestionnaire_persistance.sauvegarder_joueur(o_joueur_modele)
        self.o_joueur_vue.render_confirm_ajout_joueur(**d_infos_joueur)

#
    def lister_joueurs(self) -> None:
        """Affiche la liste des joueurs enregistrés.

        Cette méthode récupère les données des joueurs stockées dans le JSON,
        les convertit en objets Joueur, puis les affiche via la vue.

        Steps:
            1. Charge les données des joueurs depuis la base de données.
            2. Convertit chaque entrée en une instance de Joueur.
            3. Affiche la liste des joueurs à l'utilisateur.
            """

        joueurs_data = self.o_gestionnaire_persistance.charger_joueurs()

        # Convertir chaque document en une instance de Joueur
        joueurs = []
        for joueur_datum in joueurs_data:
            o_joueur = Joueur(
                p_identifiant_national_echec=joueur_datum["identifiant_national_echec"],
                p_nom_famille=joueur_datum["nom_famille"],
                p_prenom=joueur_datum["prenom"],
                p_date_naissance=joueur_datum["date_naissance"],
                p_score=joueur_datum["score"],
            )
            joueurs.append(o_joueur)

        self.o_joueur_vue.render_lister_joueur(joueurs)
