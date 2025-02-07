from models import Tournoi, GestionnairePersistance
from views import TournoiVue

import questionary


class TournoiControleur:
    def __init__(self):
        self.o_tournoi_vue = TournoiVue()
        self.o_gestionnaire_persistance = GestionnairePersistance()

    def ajouter_tournoi(self):
        s_nom_tournoi = questionary.text("Entrez le nom du tournoi  :").ask()
        s_lieu_tournoi = questionary.text("Entrez le lieu du tournoi  :").ask()
        s_date_debut_tournoi = questionary.text(
            "Entrez la date du début du tournoi  JJ/MM/AAAA :"
        ).ask()
        s_date_fin_tournoi = questionary.text(
            "Entrez la date de fin du tournoi  :"
        ).ask()
        s_nombre_tour_tournoi = questionary.text(
            "Entrez le nombre de tour du tournoi  :"
        ).ask()
        s_description_tournoi = questionary.text(
            "Entrez la desription du tournoi  :"
        ).ask()

        o_tournoi_modele = Tournoi(
            s_nom_tournoi,
            s_lieu_tournoi,
            s_date_debut_tournoi,
            s_date_fin_tournoi,
            s_nombre_tour_tournoi,
            s_description_tournoi,
        )

        self.o_gestionnaire_persistance.sauvegarder_tournoi(o_tournoi_modele)
        self.o_tournoi_vue.render_confirm_ajout_joueur(
            s_nom_tournoi,
            s_lieu_tournoi,
            s_date_debut_tournoi,
            s_date_fin_tournoi,
            s_nombre_tour_tournoi,
            s_description_tournoi,
        )
