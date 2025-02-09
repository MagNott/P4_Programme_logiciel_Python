# from models import Joueur, Match, Tour, Tournoi
from controllers import (
    JoueurControleur,
    MatchControleur,
    TourControleur,
    TournoiControleur,
)
from rich.console import Console
from rich.panel import Panel

import questionary

MENU_AJOUTER_JOUEUR = "Ajouter un joueur"
MENU_LISTER_JOUEURS = "Lister les joueurs"
MENU_AJOUTER_TOURNOI = "Ajouter un tournoi"
MENU_INSCRIRE_JOUEUR = "Inscrire un joueur"
MENU_QUITTER = "Quitter"

console = Console()

texte = "[bold blue]\n Bienvenue dans Let's Roque, le super logiciel de gestion de tournoi d'échec ! \n[/bold blue]"
console.print(
    Panel(
        texte,
        border_style="blue", width=len(texte)
    )
)

print("\n")


def menu_principal():
    # Création du menu principal
    choix = questionary.select(
        "Que souhaitez-vous faire ?",  # La question affichée
        choices=[
            MENU_AJOUTER_JOUEUR,  # Option 1
            MENU_LISTER_JOUEURS,  # Option 2
            MENU_AJOUTER_TOURNOI,
            MENU_INSCRIRE_JOUEUR,
            "Ce menu ne sert à rien",
            MENU_QUITTER,  # Option pour quitter
        ],
    ).ask()  # L’utilisateur choisit et la réponse est retournée
    return choix


# Programme principal
if __name__ == "__main__":

    # Instanciation des controlleurs
    joueur_controleur = JoueurControleur()
    tournoi_controleur = TournoiControleur()

    while True:
        choix = (
            menu_principal()
        )  # Affiche le menu et récupère le choix de l’utilisateur

        if choix == MENU_AJOUTER_JOUEUR:
            joueur_controleur.ajouter_joueur()
        elif choix == MENU_LISTER_JOUEURS:
            joueur_controleur.lister_joueurs()
        elif choix == MENU_AJOUTER_TOURNOI:
            tournoi_controleur.ajouter_tournoi()
        elif choix == MENU_INSCRIRE_JOUEUR:
            tournoi_controleur.inscrire_joueur()
        elif choix == MENU_QUITTER:
            console.print("[bold blue] \n Fermeture du programme. \n [/bold blue]")
            break
        else:
            console.print("[bold red]\n Choix inconnu \n[/bold red]")
