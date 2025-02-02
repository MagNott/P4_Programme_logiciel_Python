from models import Joueur
from views import JoueurVue

import questionary


class JoueurControleur:
    # def __init__(self):
    #     self.o_joueur_vue = JoueurVue()

    def ajouter_joueur(self):
        # Poser les questions pour obtenir les informations du joueur
        s_nom = questionary.text("Entrez le nom du joueur :").ask()
        s_prenom = questionary.text("Entrez le prenom du joueur :").ask()

        o_joueur_modele = Joueur(s_nom, s_prenom)
        Joueur.liste_joueur.append(o_joueur_modele)

        JoueurVue.render_confirm_ajout_joueur(s_nom, s_prenom)

    def lister_joueurs(self):
        JoueurVue.render_lister_joueur(Joueur.liste_joueur)
