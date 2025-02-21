from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary
from models.tournoi import Tournoi


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
        self,
        p_tournoi_choisi,
        p_numero_tour,
        p_identifiant_match,
        p_joueur_blanc,
        p_joueur_noir,
    ) -> None:
        """Affiche les matchs générés pour un tour donné.

        Args:
            p_tour (Tour): Objet contenant les informations du tour et la liste des matchs.
        """
        # self.console.print(
        #     f"\n[bold cyan] Pour le Tour : {p_numero_tour} du Tournoi : {p_tournoi_choisi}[/bold cyan]\n"
        # )
        # self.console.print(
        #     f"\n[bold magenta] Match entre : {p_joueur_blanc} VS {p_joueur_noir})[/bold magenta]\n"
        # )
        self.console.print(
            Panel(
                f"[bold cyan] Match n°{p_identifiant_match} du Round n°{p_numero_tour} du tournoi : {p_tournoi_choisi} [/bold cyan]",
                border_style="cyan",
                expand=False,
            )
        )

        # Création d’un tableau pour l’affichage des joueurs
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("🔹 Joueur Blanc", style="bold white", justify="center")
        table.add_column("VS", style="bold yellow", justify="center")
        table.add_column("🔹 Joueur Noir", style="bold white", justify="center")

        table.add_row(
            f"[cyan]{p_joueur_blanc}[/cyan]",
            "[yellow]⚔️[/yellow]",
            f"[cyan]{p_joueur_noir}[/cyan]",
        )

        self.console.print(table)

    #
    def render_matchs_pour_saisie(self, p_objet_tournoi: Tournoi, p_dernier_tour, p_matchs):

        s_dernier_tour_nom = p_dernier_tour["nom"]
        s_tournoi_nom = p_objet_tournoi.nom_tournoi
        l_resultats = []
        for match in p_matchs:
            self.console.print(
                Panel(
                    f"[bold cyan] Match N°{match.identifiant} : {match.joueur_blanc} ⚔️ {match.joueur_noir} du {s_dernier_tour_nom} du tournoi : {s_tournoi_nom}[/bold cyan]",
                    border_style="cyan",
                    expand=False,
                )
            )

            # self.console.print(
            #     f"\n[bold cyan] Si {match.joueur_blanc} a gagner merci de taper 1"
            # )
            # self.console.print(
            #     f"\n[bold cyan] Si {match.joueur_noir} a gagner merci de taper 2"
            # )
            # self.console.print("\n[bold cyan] Si le match est nul merci de taper 0")

            # resultat_match = questionary.text("Veuillez saisir votre choix: ").ask()

            # if resultat_match == "1":
            #     resultat_score = {
            #         "score_blanc": 1,
            #         "score_noir": 0,
            #         "statut": "Terminé",
            #     }
            # elif resultat_match == "2":
            #     resultat_score = {
            #         "score_blanc": 0,
            #         "score_noir": 1,
            #         "statut": "Terminé",
            #     }
            # elif resultat_match == "3":
            #     resultat_score = {
            #         "score_blanc": 0.5,
            #         "score_noir": 0.5,
            #         "statut": "Terminé",
            #     }

            # Création du tableau des choix
            table = Table(show_header=False, header_style="bold magenta")
            table.add_column("🏆 Choix", style="bold yellow", justify="center")
            table.add_column("📋 Explication", style="bold white", justify="left")

            table.add_row("[1]", f"Victoire de [cyan]{match.joueur_blanc}[/cyan]")
            table.add_row("[2]", f"Victoire de [cyan]{match.joueur_noir}[/cyan]")
            table.add_row("[0]", "Match nul")

            self.console.print(table)

            # Demander le choix utilisateur avec `questionary`
            resultat_match = questionary.select(
                "Veuillez choisir une option",
                choices=["1", "2", "0"],
            ).ask()

            # Associer les scores en fonction du choix utilisateur
            resultat_score = {
                "1": {"score_blanc": 1, "score_noir": 0, "statut": "Terminé"},
                "2": {"score_blanc": 0, "score_noir": 1, "statut": "Terminé"},
                "0": {"score_blanc": 0.5, "score_noir": 0.5, "statut": "Terminé"},
            }[resultat_match]

            l_resultats.append(resultat_score)

        return l_resultats
