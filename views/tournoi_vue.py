from rich.console import Console
from rich.table import Table
import questionary
from typing import List


class TournoiVue:
    """Gère l'affichage des informations liées aux tournois avec la bibliothèque Rich."""

    def __init__(self):
        """Initialise l'affichage en configurant la console Rich pour une sortie stylisée."""
        self.console = Console()

    #
    def render_confirm_ajout_tournoi(
        self,
        p_nom_tournoi: str,
        p_lieu_tournoi: str,
        p_date_debut_tournoi: str,
        p_date_fin_tournoi: str,
        p_nombre_tour_tournoi: int,
        p_description_tournoi: str,
    ) -> None:
        """Permet à l'utilisateur d'avoir la confirmation que l'ajout du tournoi a été fait.

        Args:
            p_nom_tournoi (str): Nom du tournoi saisi par l'utilisateur.
            p_lieu_tournoi (str): Lieu où se déroulera le tournoi.
            p_date_debut_tournoi (str): Date de début du tournoi au format JJ/MM/AAAA.
            p_date_fin_tournoi (str): Date de fin du tournoi au format JJ/MM/AAAA.
            p_nombre_tour_tournoi (str): Nombre de tour du tournoi.
            p_description_tournoi (str): Description ou informations supplémentaires sur le tournoi.
        """

        self.console.print(
            f"""\n[bold green]Tournoi ajouté avec succès :
            {p_nom_tournoi},
            {p_lieu_tournoi},
            {p_date_debut_tournoi},
            {p_date_fin_tournoi},
            {p_nombre_tour_tournoi},
            {p_description_tournoi},
            [/bold green]\n"""
        )

    #
    def render_choix_tournoi(self, p_liste_tournois: list[str]) -> str:
        """Permet à l'utilisateur de choisir un tournoi parmi une liste.

        Args:
            liste_tournois (list[str]): Liste des noms de fichiers représentant les tournois disponibles.

        Returns:
            str: Identifiant du tournoi choisi par l'utilisateur, saisi via l'interface interactive.
        """

        table = Table(title="Liste des tournois")
        table.add_column("nom du tournoi")

        for tournoi in p_liste_tournois:
            table.add_row(tournoi)

        self.console.print(table)
        # récupérer le choix de l'utilisateur
        return questionary.text(
            "Veuillez choisir un tournoi par son identifiant : "
        ).ask()

    #
    def render_choix_joueur(self, p_liste_joueurs: List[dict]) -> List[str]:
        """Affiche la liste des joueurs disponibles et permet à l'utilisateur d'en choisir 4.

        Args:
            p_liste_joueurs (List[dict]): Liste des joueurs disponibles,
                chaque joueur étant représenté sous forme de dictionnaire
                avec les clés 'id_tinydb', 'identifiant_national_echec',
                'nom_famille', 'prenom' et 'date_naissance'.

        Returns:
            List[str]: Liste contenant les identifiants des joueurs sélectionnés par l'utilisateur.
        """
        table = Table(title="Liste des joueurs")
        table.add_column("Choix", justify="center")
        table.add_column("Id echec", justify="center")
        table.add_column("Nom de famille", justify="center")
        table.add_column("Prénom", justify="center")
        table.add_column("Date de naissance", justify="center")

        # Liste de couleurs alternées pour chaque ligne de présentation en tableau
        couleurs_lignes = ["dim cyan", "dim magenta"]

        for i, joueur in enumerate(p_liste_joueurs):
            couleur = couleurs_lignes[i % len(couleurs_lignes)]  # Alterner les couleurs
            table.add_row(
                f"[{couleur}]{str(joueur['id_tinydb'])}[/{couleur}]",
                f"[{couleur}]{str(joueur['identifiant_national_echec'])}[/{couleur}]",
                f"[{couleur}]{joueur['nom_famille']}[/{couleur}]",
                f"[{couleur}]{joueur['prenom']}[/{couleur}]",
                f"[{couleur}]{joueur['date_naissance']}[/{couleur}]",
            )

        self.console.print(table)

        l_choix_joueur = []
        compteur = 0
        while compteur < 4:
            joueur = questionary.text(
                "\n Veuillez choisir un joueur par son identifiant : "
            ).ask()
            l_choix_joueur.append(joueur)
            self.console.print(
                f"\n [bold green] Joueur {joueur} ajouté à la liste.\n[/bold green]"
            )
            compteur += 1
        return l_choix_joueur

    #
    def render_visualiser_tournoi(
        self, p_tournoi: list[dict[str, str]], p_joueurs_db: list[dict[str, str]]
    ) -> None:
        """Affiche les informations du tournoi choisi.

        Args:
            p_tournoi (list[dict[str, str]]): Liste contenant un dictionnaire avec les informations du tournoi.
            p_joueurs_db (list[dict[str, str]]): Liste de dictionnaires représentant les joueurs enregistrés.
        """

        # Le tournoi est stocké sous forme de liste contenant un unique dictionnaire (p_tournoi[0]
        # est utilisé pour accéder aux données)
        liste_joueurs_ids = p_tournoi[0]["liste_joueurs"]
        joueurs_affiches = []

        # Faire correspondre l'id du joueur avec ses données
        for joueur_id in liste_joueurs_ids:
            for joueur in p_joueurs_db:
                if joueur["id_tinydb"] == int(joueur_id):
                    joueurs_affiches.append(
                        f"{joueur['nom_famille']} {joueur['prenom']}"
                    )
            joueurs_affiches_str = ", ".join(joueurs_affiches)

        self.console.print(
            f"""\n[bold green]Contenu du tournoi : [/bold green]
            Nom : [bold green]{p_tournoi[0]["nom_tournoi"]}[/bold green],
            Lieu : [bold green]{p_tournoi[0]["lieu_tournoi"]}[/bold green],
            Date début : [bold green]{p_tournoi[0]["date_debut_tournoi"]}[/bold green],
            Date fin : [bold green]{p_tournoi[0]["date_fin_tournoi"]}[/bold green],
            Nombre de tours : [bold green]{p_tournoi[0]["nombre_tours"]}[/bold green],
            Liste des joueurs : [bold green]{joueurs_affiches_str}[/bold green]
            Description : [bold green]{p_tournoi[0]["description"]}[/bold green],
            \n"""
        )

    #
    def render_saisie_tournoi(self) -> dict:
        """Affiche les invites de saisie pour récolter les informations d'un tournoi et retourne les valeurs saisies.

        Cette méthode demande à l'utilisateur de renseigner plusieurs informations
        sur le tournoi via des invites interactives (questionary).
        Les réponses sont stockées dans un dictionnaire et retournées.

        Returns:
            dict: Un dictionnaire contenant les informations suivantes du tournoi :
                - "p_nom_tournoi" (str) : Nom du tournoi saisi par l'utilisateur.
                - "p_lieu_tournoi" (str) : Lieu où se déroule le tournoi.
                - "p_date_debut_tournoi" (str) : Date de début du tournoi (format JJ/MM/AAAA).
                - "p_date_fin_tournoi" (str) : Date de fin du tournoi (format JJ/MM/AAAA).
                - "p_nombre_tour_tournoi" (str) : Nombre total de tours dans le tournoi.
                - "p_description_tournoi" (str) : Description facultative du tournoi.
        """

        d_infos_tournoi = {
            "p_nom_tournoi": questionary.text("Entrez le nom du tournoi  :").ask(),
            "p_lieu_tournoi": questionary.text("Entrez le lieu du tournoi  :").ask(),
            "p_date_debut_tournoi": questionary.text(
                "Entrez la date du début du tournoi  JJ/MM/AAAA :"
            ).ask(),
            "p_date_fin_tournoi": questionary.text(
                "Entrez la date de fin du tournoi  :"
            ).ask(),
            "p_nombre_tour_tournoi": questionary.text(
                "Entrez le nombre de tour du tournoi  :"
            ).ask(),
            "p_description_tournoi": questionary.text(
                "Entrez la desription du tournoi  :"
            ).ask(),
        }

        return d_infos_tournoi
