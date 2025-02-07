from models import Joueur, GestionnairePersistance
from views import JoueurVue

import questionary


class JoueurControleur:
    def __init__(self):
        self.o_joueur_vue = JoueurVue()
        self.o_gestionnaire_persistance = GestionnairePersistance()

    def ajouter_joueur(self):
        # Poser les questions pour obtenir les informations du joueur
        s_nom = questionary.text("Entrez le nom du joueur :").ask()
        s_prenom = questionary.text("Entrez le prenom du joueur :").ask()
        o_joueur_modele = Joueur(s_nom, s_prenom)
        self.o_gestionnaire_persistance.sauvegarder_joueur(o_joueur_modele)
        self.o_joueur_vue.render_confirm_ajout_joueur(s_nom, s_prenom)

    def lister_joueurs(self):
        joueurs_data = self.o_gestionnaire_persistance.charger_joueurs()
        # Convertir chaque document en une instance de Joueur
        joueurs = []
        for joueur_datum in joueurs_data:
            o_joueur = Joueur(
                p_nom_famille=joueur_datum["nom_famille"],
                p_prenom=joueur_datum["prenom"]
            )
            joueurs.append(o_joueur)
        self.o_joueur_vue.render_lister_joueur(joueurs)
