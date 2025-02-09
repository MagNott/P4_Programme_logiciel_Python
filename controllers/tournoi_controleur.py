from models import Tournoi, GestionnairePersistance
from views import TournoiVue

import questionary


class TournoiControleur:
    def __init__(self):
        self.o_tournoi_vue = TournoiVue()
        self.o_gestionnaire_persistance = GestionnairePersistance()

    def ajouter_tournoi(self):
        identifiant_tournoi = Tournoi.generer_identifiant()
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
            identifiant_tournoi,
            s_nom_tournoi,
            s_lieu_tournoi,
            s_date_debut_tournoi,
            s_date_fin_tournoi,
            s_nombre_tour_tournoi,
            s_description_tournoi,
        )

        self.o_gestionnaire_persistance.sauvegarder_tournoi(o_tournoi_modele)
        self.o_tournoi_vue.render_confirm_ajout_tournoi(
            s_nom_tournoi,
            s_lieu_tournoi,
            s_date_debut_tournoi,
            s_date_fin_tournoi,
            s_nombre_tour_tournoi,
            s_description_tournoi,
        )

    def inscrire_joueur(self):
        l_liste_tournois = self.o_gestionnaire_persistance.lister_tournois()
        i_identifiant_tournoi = self.o_tournoi_vue.render_choix_tournoi(l_liste_tournois)
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

        o_tournoi_choisi.liste_joueurs.append(l_choix_joueur)
        self.o_gestionnaire_persistance.sauvegarder_joueurs_tournoi(o_tournoi_choisi)
