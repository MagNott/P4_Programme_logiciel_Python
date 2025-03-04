from controllers.joueur_controleur import JoueurControleur
from controllers.tournoi_controleur import TournoiControleur
from controllers.tour_controleur import TourControleur
from rich.console import Console
from rich.panel import Panel
import questionary

# Définition des options du menu
# Ces constantes représentent les différentes options disponibles dans les menus de l'application.
# Elles sont utilisées pour afficher les choix dans les menus et faciliter la navigation de l'utilisateur.
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
MENU_TERMINER_TOUR = "Terminer un tour"
MENU_VISUALISER_TOUR_MATCH_TOURNOI = "Visualiser les tours et matchs d'un tournoi"
MENU_SAUVEGARDER_CHARGER = "Sauvegarder ou charger les données"
MENU_SAUVEGARDER_DONNEES = "Sauvegarder les données"
MENU_CHARGER_DONNEES = "Charger les données"
RETOUR_MENU_PRINCIPAL = "Retour au menu principal"
MENU_QUITTER = "Quitter"

console = Console()

# Affichage du message de bienvenue
# Ce message est affiché à l'utilisateur lorsqu'il lance l'application.
# Il est stylisé avec `rich`.
texte = "[bold blue]\n Bienvenue dans Let's Roque, le super logiciel de gestion de tournoi d'échec ! \n[/bold blue]"
console.print(Panel(texte, border_style="blue", width=len(texte)))

print("\n")


def menu_principal():
    """
    Affiche le menu principal et récupère le choix de l'utilisateur.

    Returns:
        str: L'option sélectionnée par l'utilisateur.
    """

    choix = questionary.select(
        "Que souhaitez-vous faire ?",
        choices=[
            MENU_GESTION_JOUEUR,
            MENU_GESTION_TOURNOI,
            MENU_GESTION_RAPPORTS,
            MENU_SAUVEGARDER_CHARGER,
            MENU_QUITTER,
        ],
    ).ask()  # L’utilisateur choisit et la réponse est retournée
    return choix


def menu_joueur():
    """
    Affiche le menu de gestion des joueurs et récupère le choix de l'utilisateur.

    Returns:
        str: L'option sélectionnée par l'utilisateur.
    """

    choix_joueur = questionary.select(
        "Que souhaitez-vous faire ?",
        choices=[
            MENU_AJOUTER_JOUEUR,
            RETOUR_MENU_PRINCIPAL,
        ],
    ).ask()
    return choix_joueur


def menu_tournoi():
    """
    Affiche le menu de gestion des tournois et récupère le choix de l'utilisateur.

    Returns:
        str: L'option sélectionnée par l'utilisateur.
    """

    choix_tournoi = questionary.select(
        "Que souhaitez-vous faire ?",
        choices=[
            MENU_CREER_TOURNOI,
            MENU_INSCRIRE_JOUEUR,
            MENU_CREER_TOUR,
            MENU_TERMINER_TOUR,
            RETOUR_MENU_PRINCIPAL,
        ],
    ).ask()
    return choix_tournoi


def menu_rapports():
    """
    Affiche le menu de gestion des rapports et récupère le choix de l'utilisateur.

    Returns:
        str: L'option sélectionnée par l'utilisateur.
    """
    choix_rapports = questionary.select(
        "Que souhaitez-vous faire ?",
        choices=[
            MENU_LISTER_JOUEURS,
            MENU_LISTER_TOURNOI,
            MENU_VISUALISER_TOURNOI,
            MENU_VISUALISER_TOUR_MATCH_TOURNOI,
            RETOUR_MENU_PRINCIPAL,
        ],
    ).ask()
    return choix_rapports


def menu_sauvergarder_charger():
    """

    """
    choix_donnees = questionary.select(
        "Que souhaitez-vous faire ?",
        choices=[
            MENU_SAUVEGARDER_DONNEES,
            MENU_CHARGER_DONNEES,
            RETOUR_MENU_PRINCIPAL,
        ],
    ).ask()
    return choix_donnees


# Point d'entrée principal du programme
# Ce code s'exécute uniquement si ce fichier est lancé directement (et non importé).
# Il initialise les contrôleurs et lance la boucle du menu principal.
if __name__ == "__main__":

    # Instanciation des controlleurs
    joueur_controleur = JoueurControleur()
    tournoi_controleur = TournoiControleur()
    tour_controleur = TourControleur()

    # Pour réafficher systématiquement le menu tant que quitter n'est pas choisi
    while True:
        # Affiche le menu et récupère le choix de l’utilisateur
        choix = (
            menu_principal()
        )
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
                elif choix_tournoi == MENU_TERMINER_TOUR:
                    tour_controleur.terminer_tour()
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
                elif choix_rapports == MENU_VISUALISER_TOUR_MATCH_TOURNOI:
                    tournoi_controleur.visualiser_tour_match_tournoi()
                elif choix_rapports == RETOUR_MENU_PRINCIPAL:
                    break
        elif choix == MENU_SAUVEGARDER_CHARGER:
            while True:
                choix_donnees = menu_sauvergarder_charger()
                if choix_donnees == MENU_SAUVEGARDER_DONNEES:
                    tournoi_controleur.sauvegarder_donnees()
                elif choix_donnees == MENU_CHARGER_DONNEES:
                    tournoi_controleur.charger_donnees()
                elif choix_donnees == RETOUR_MENU_PRINCIPAL:
                    break
        elif choix == MENU_QUITTER:
            console.print(
                Panel(
                    "[bold blue]🔚 Fermeture du programme. Merci d'avoir utilisé Let's Roque ![/bold blue]",
                    border_style="blue",
                    expand=False,
                )
            )
            break
        else:
            console.print("[bold red]\n Choix inconnu \n[/bold red]")
