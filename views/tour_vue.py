from rich.console import Console
from rich.table import Table
import questionary


class TourVue:
    """Gère l'affichage des informations liées aux tour avec la bibliothèque Rich."""

    def __init__(self):
        """Initialise l'affichage en configurant la console Rich pour une sortie stylisée."""
        self.console = Console()

#
    def render_choix_tournoi(self, p_liste_tournois: list[str]) -> str:
        """Permet à l'utilisateur de choisir un tournoi parmi une liste.

        Args:
            p_liste_tournois (list[str]): Liste des noms de fichiers des tournois disponibles.

        Returns:
            str: Identifiant du tournoi choisi par l'utilisateur.
        """
        table = Table(title="Liste des tournois")
        table.add_column("Nom du tournoi")

        for tournoi in p_liste_tournois:
            table.add_row(tournoi)

        self.console.print(table)

        return questionary.text("Veuillez choisir un tournoi par son identifiant : ").ask()

#
    def render_confirmation_ajout_tour(self, p_numero_tour: str, p_tournoi_choisi) -> None:
        """Affiche un message à l'utilisateur.

        Args:
            p_message (str): Message à afficher.
        """
        self.console.print(f"\n[bold green] Le round {p_numero_tour} ajouté au tournoi {p_tournoi_choisi.nom_tournoi}. [/bold green]\n")

#
    def render_verification_tour_max(self, p_message: str) -> None:
        """Affiche un message d'erreur lorsque le nombre maximal de tours est atteint.

        Args:
            p_message (str): Message d'information à afficher.
        """
        self.console.print(f"\n[bold red]{p_message}[/bold red]\n")

#
    def render_tour_en_cours(self, p_nom_tournoi: str, p_nom_tour: str) -> None:
        """Affiche un message si un tour est encore en cours dans un tournoi.

        Args:
            p_nom_tournoi (str): Nom du tournoi concerné.
            p_nom_tour (str): Nom du tour en cours.
        """
        self.console.print(
            f"[bold yellow] Impossible de créer un nouveau tour.[/bold yellow]\n"
            f"Le tournoi [bold cyan]{p_nom_tournoi}[/bold cyan] a encore un tour en cours :\n"
            f"[bold red]{p_nom_tour}[/bold red].\n"
            f"Veuillez d'abord saisir les résultats des matchs avant de continuer.\n"
        )
