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

        return questionary.text(
            "Veuillez choisir un tournoi par son identifiant : "
        ).ask()

    #
    def render_confirmation_ajout_tour(
        self, p_numero_tour: str, p_tournoi_choisi
    ) -> None:
        """Affiche un message à l'utilisateur.

        Args:
            p_message (str): Message à afficher.
        """
        self.console.print(
            f"\n[bold green] Le round {p_numero_tour} ajouté au tournoi {p_tournoi_choisi.nom_tournoi}. [/bold green]\n"
        )

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

    #
    def render_visualiser_matchs(
        self, p_tournoi_choisi, p_numero_tour, p_joueur_blanc, p_joueur_noir
    ) -> None:
        """Affiche les matchs générés pour un tour donné.

        Args:
            p_tour (Tour): Objet contenant les informations du tour et la liste des matchs.
        """
        self.console.print(
            f"\n[bold cyan] Pour le Tour : {p_numero_tour} du Tournoi : {p_tournoi_choisi}[/bold cyan]\n"
        )
        self.console.print(
            f"\n[bold magenta] Match entre : {p_joueur_blanc} VS {p_joueur_noir})[/bold magenta]\n"
        )

    #
    def render_matchs_pour_saisie(self, l_matchs):

        l_resultats = []
        for match in l_matchs:
            self.console.print(
                f"\n[bold cyan] pour le match {match.nom_match} merci de saisir les résultats"
            )
            self.console.print(
                f"\n[bold cyan] Si {match.joueur_blanc} a gagner merci de taper 1"
            )
            self.console.print(
                f"\n[bold cyan] Si {match.joueur_noir} a gagner merci de taper 2"
            )
            self.console.print("\n[bold cyan] Si le match est nul merci de taper 0")

            resultat_match = questionary.text("Veuillez saisir votre choix: ").ask()

            if resultat_match == "1":
                resultat_score = {"score_blanc": 1, "score_noir": 0, "statut": "Terminé"}
            elif resultat_match == "2":
                resultat_score = {"score_blanc": 0, "score_noir": 1, "statut": "Terminé"}
            elif resultat_match == "3":
                resultat_score = {"score_blanc": 0.5, "score_noir": 0.5, "statut": "Terminé"}

            l_resultats.append(resultat_score)

        return l_resultats
