from rich.table import Table
from rich.panel import Panel
import questionary
from models.tournoi import Tournoi
from views.vue import Vue


class TourVue(Vue):
    """Gère l'affichage des informations liées aux tour avec la bibliothèque Rich."""

    #
    # def render_choix_tournoi(self, p_liste_tournois: list[str]) -> str:
    #     """Permet à l'utilisateur de choisir un tournoi parmi une liste.

    #     Args:
    #         p_liste_tournois (list[str]): Liste des noms de fichiers des tournois disponibles.

    #     Returns:
    #         str: Identifiant du tournoi choisi par l'utilisateur.
    #     """
    #     table = Table(title="Liste des tournois")
    #     table.add_column("Nom du tournoi")

    #     for tournoi in p_liste_tournois:
    #         table.add_row(tournoi)

    #     self.console.print(table)

    #     return questionary.text(
    #         "Veuillez choisir un tournoi par son identifiant : "
    #     ).ask()

    #
    def render_confirmation_ajout_tour(
        self,
        p_numero_tour: str,
        p_tournoi_choisi: Tournoi
    ) -> None:
        """
        Affiche un message confirmant l'ajout d'un tour à un tournoi.

        Cette fonction affiche un message de confirmation en console lorsque
        l'utilisateur ajoute un nouveau round à un tournoi existant.

        Args:
            p_numero_tour (str): Numéro du round ajouté.
            p_tournoi_choisi (Tournoi): Objet Tournoi auquel le round a été ajouté.

        Returns:
            None: Cette fonction affiche uniquement un message en console.
        """
        self.console.print(
            f"\n[bold green] Le round {p_numero_tour} ajouté au tournoi {p_tournoi_choisi.nom_tournoi}. [/bold green]\n"
        )

    #
    def render_verification(self, p_message: str) -> None:
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
        p_tournoi_choisi: str,
        p_numero_tour: int,
        p_identifiant_match: int,
        p_objet_joueur_blanc: str,
        p_objet_joueur_noir: str,
    ) -> None:
        """
        Affiche les informations d'un match généré pour un tour donné.

        Cette fonction affiche le match et leur joueurs sous forme de tableau avec `rich`.

        Args:
            p_tournoi_choisi (str): Nom du tournoi en cours.
            p_numero_tour (int): Numéro du round en cours.
            p_identifiant_match (int): Identifiant unique du match.
            p_joueur_blanc (str): Nom du joueur ayant les pièces blanches.
            p_joueur_noir (str): Nom du joueur ayant les pièces noires.

        Returns:
            None: Cette fonction affiche le match en console et ne retourne rien.
        """
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
            f"[cyan]{p_objet_joueur_blanc.nom_famille} {p_objet_joueur_blanc.prenom}[/cyan]",
            "[yellow]⚔️[/yellow]",
            f"[cyan]{p_objet_joueur_noir.nom_famille} {p_objet_joueur_noir.prenom}[/cyan]",
        )

        self.console.print(table)

    #
    def render_matchs_pour_saisie(
        self,
        p_objet_tournoi: Tournoi,
        p_dernier_tour: dict,
        p_objets_matchs: list
    ) -> list[dict]:
        """
        Affiche les matchs en attente de saisie des résultats et recueille la saisie utilisateur du résultat.

        Cette fonction affiche chaque match du tour actuel avec une mise en forme `rich`,
        en indiquant les joueurs et le numéro du match. L'utilisateur peut saisir le résultat
        du match via un choix interactif.

        Args:
            p_objet_tournoi (Tournoi): Objet contenant les informations du tournoi.
            p_dernier_tour (dict): Dictionnaire contenant les informations du dernier tour en cours.
            p_matchs (list): Liste des objets Match correspondant aux matchs du tour actuel.

        Returns:
            list[dict]: Une liste de dictionnaires contenant les résultats des matchs.
                        Chaque dictionnaire contient:
                        - "score_blanc" (float): Score attribué au joueur blanc.
                        - "score_noir" (float): Score attribué au joueur noir.
                        - "statut" (str): Indique si le match est terminé.
        """

        s_dernier_tour_nom = p_dernier_tour["nom"]
        s_tournoi_nom = p_objet_tournoi.nom_tournoi
        l_resultats = []
        for o_match in p_objets_matchs:

            texte = (f"[bold cyan] Match N°{o_match.identifiant} : {o_match.joueur_blanc.nom_famille} {o_match.joueur_blanc.prenom} ⚔️  {o_match.joueur_noir.nom_famille} {o_match.joueur_noir.prenom}\n"
                     f"du {s_dernier_tour_nom} du tournoi : {s_tournoi_nom}[/bold cyan]")

            self.console.print(Panel(texte, border_style="cyan", expand=False,))

            # Création du tableau des choix
            table = Table(show_header=False, header_style="bold magenta")
            table.add_column("🏆 Choix", style="bold yellow", justify="center")
            table.add_column("📋 Explication", style="bold white", justify="left")

            table.add_row("[1]", f"Victoire de [cyan]{o_match.joueur_blanc.nom_famille} {o_match.joueur_blanc.prenom}[/cyan]")
            table.add_row("[2]", f"Victoire de [cyan]{o_match.joueur_noir.nom_famille} {o_match.joueur_noir.prenom}[/cyan]")
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
