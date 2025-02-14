from controllers.joueur_controleur import JoueurControleur
from controllers.tournoi_controleur import TournoiControleur
from controllers.tour_controleur import TourControleur
from rich.console import Console
from rich.panel import Panel
import questionary


MENU_GESTION_JOUEUR = "Gestion des joueurs"
MENU_GESTION_TOURNOI = "Gestion des tournois"
MENU_GESTION_RAPPORTS = "Gestion des rapports"
MENU_AJOUTER_JOUEUR = "Ajouter un joueur"
MENU_LISTER_JOUEURS = "Lister les joueurs"
MENU_CREER_TOURNOI = "Créer un tournoi"
MENU_INSCRIRE_JOUEUR = "Inscrire un joueur"
MENU_LISTER_TOURNOI = "Lister les tournois"
MENU_VISUALISER_TOURNOI = "Visualiser un tournoi"
MENU_CREER_TOUR = "Créer un tour"
RETOUR_MENU_PRINCIPAL = "Retour au menu principal"
MENU_QUITTER = "Quitter"

console = Console()


texte = "[bold blue]\n Bienvenue dans Let's Roque, le super logiciel de gestion de tournoi d'échec ! \n[/bold blue]"
console.print(Panel(texte, border_style="blue", width=len(texte)))

print("\n")


def menu_principal():
    # Création du menu principal
    choix = questionary.select(
        "Que souhaitez-vous faire ?",  # La question affichée
        choices=[
            MENU_GESTION_JOUEUR,  # Option 1
            MENU_GESTION_TOURNOI,
            MENU_GESTION_RAPPORTS,
            "Ce menu ne sert à rien",
            MENU_QUITTER,  # Option pour quitter
        ],
    ).ask()  # L’utilisateur choisit et la réponse est retournée
    return choix


def menu_joueur():
    # Création du menu joueur
    choix_joueur = questionary.select(
        "Que souhaitez-vous faire ?",  # La question affichée
        choices=[
            MENU_AJOUTER_JOUEUR,
            RETOUR_MENU_PRINCIPAL,
        ],
    ).ask()  # L’utilisateur choisit et la réponse est retournée
    return choix_joueur


def menu_tournoi():
    # Création du menu joueur
    choix_tournoi = questionary.select(
        "Que souhaitez-vous faire ?",  # La question affichée
        choices=[
            MENU_CREER_TOURNOI,
            MENU_INSCRIRE_JOUEUR,
            MENU_CREER_TOUR,
            RETOUR_MENU_PRINCIPAL,
        ],
    ).ask()  # L’utilisateur choisit et la réponse est retournée
    return choix_tournoi


def menu_rapports():
    # Création du menu joueur
    choix_rapports = questionary.select(
        "Que souhaitez-vous faire ?",  # La question affichée
        choices=[
            MENU_LISTER_JOUEURS,
            MENU_LISTER_TOURNOI,
            MENU_VISUALISER_TOURNOI,
            RETOUR_MENU_PRINCIPAL,
        ],
    ).ask()  # L’utilisateur choisit et la réponse est retournée
    return choix_rapports


# Programme principal
if __name__ == "__main__":

    # Instanciation des controlleurs
    joueur_controleur = JoueurControleur()
    tournoi_controleur = TournoiControleur()
    tour_controleur = TourControleur()

    while True:
        choix = (
            menu_principal()
        )  # Affiche le menu et récupère le choix de l’utilisateur

        if choix == MENU_GESTION_JOUEUR:
            while True:
                choix_joueur = menu_joueur()
                if choix_joueur == MENU_AJOUTER_JOUEUR:
                    joueur_controleur.ajouter_joueur()
                elif choix_joueur == RETOUR_MENU_PRINCIPAL:
                    break
        elif choix == MENU_GESTION_TOURNOI:
            while True:
                choix_tournoi = menu_tournoi()
                if choix_tournoi == MENU_CREER_TOURNOI:
                    tournoi_controleur.ajouter_tournoi()
                elif choix_tournoi == MENU_INSCRIRE_JOUEUR:
                    tournoi_controleur.inscrire_joueur()
                elif choix_tournoi == MENU_CREER_TOUR:
                    tour_controleur.creer_tour()
                elif choix_tournoi == RETOUR_MENU_PRINCIPAL:
                    break
        elif choix == MENU_GESTION_RAPPORTS:
            while True:
                choix_rapports = menu_rapports()
                if choix_rapports == MENU_LISTER_JOUEURS:
                    joueur_controleur.lister_joueurs()
                elif choix_rapports == MENU_LISTER_TOURNOI:
                    tournoi_controleur.lister_tournois()
                elif choix_rapports == MENU_VISUALISER_TOURNOI:
                    tournoi_controleur.visualiser_tournoi()
                elif choix_rapports == RETOUR_MENU_PRINCIPAL:
                    break
        elif choix == MENU_QUITTER:
            console.print("[bold blue] \n Fermeture du programme. \n [/bold blue]")
            break
        else:
            console.print("[bold red]\n Choix inconnu \n[/bold red]")
