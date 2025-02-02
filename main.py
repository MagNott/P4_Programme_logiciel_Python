# from models import Joueur, Match, Tour, Tournoi
from controllers import (
    JoueurControleur,
    MatchControleur,
    TourControleur,
    TournoiControleur,
)

# from views import JoueurVue, MatchVue, TourVue, TournoiVue
import questionary

MENU_AJOUTER_JOUEUR = "Ajouter un joueur"
MENU_LISTER_JOUEURS = "Lister les joueurs"
MENU_QUITTER = "Quitter"




print("Bienvenue dans Let's Roque, le super logiciel de gestion de tournoi d'échec !")


def menu_principal():
    # Création du menu principal
    choix = questionary.select(
        "Que souhaitez-vous faire ?",  # La question affichée
        choices=[
            MENU_AJOUTER_JOUEUR,  # Option 1
            MENU_LISTER_JOUEURS,  # Option 2
            MENU_QUITTER,  # Option pour quitter
        ],
    ).ask()  # L’utilisateur choisit et la réponse est retournée
    return choix


# Programme principal
if __name__ == "__main__":

    # Instanciation des controlleurs
    joueur_controleur = JoueurControleur()

    while True:
        choix = (
            menu_principal()
        )  # Affiche le menu et récupère le choix de l’utilisateur

        if choix == MENU_AJOUTER_JOUEUR:
            joueur_controleur.ajouter_joueur()
        elif choix == MENU_LISTER_JOUEURS:
            joueur_controleur.lister_joueurs()
        elif choix == MENU_QUITTER:
            print("Fermeture du programme.")
            break
        else:
            print("Choix inconnu")
