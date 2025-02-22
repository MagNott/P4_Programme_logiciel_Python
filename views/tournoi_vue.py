from rich.console import Console
from rich.table import Table
import questionary
from typing import List
from models.tournoi import Tournoi


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

    def render_lister_tournois(self, p_liste_tournois: list[dict[str, str]]) -> None:
        """Affiche la liste des tournois enregistrés dans la base de données.

        Args:
            p_liste_tournois (list[dict[str, str]]): Liste de dictionnaires contenant les informations des tournois.
        """

        table = Table(title="Liste des tournois")
        table.add_column("nom du tournoi")

        for tournoi in p_liste_tournois:
            table.add_row(tournoi)

        self.console.print(table)

    #
    def render_choix_tournoi(self, p_liste_tournois: list[str]) -> str:
        """Permet à l'utilisateur de choisir un tournoi parmi une liste.

        Args:
            liste_tournois (list[str]): Liste des noms de fichiers représentant les tournois disponibles.

        Returns:
            str: Identifiant du tournoi choisi par l'utilisateur, saisi via l'interface interactive.
        """

        self.render_lister_tournois(p_liste_tournois)

        # récupérer le choix de l'utilisateur
        return questionary.text(
            "Veuillez choisir un tournoi par son identifiant : "
        ).ask()

    #
    def render_impossible_inscription(self, p_nom_tournoi: Tournoi):
        self.console.print(
                f"\n [bold red] Le tournoi {p_nom_tournoi} a déjà commencé, il n'est pas possible d'y inscrire des joueurs !\n[/bold red]"
            )

    #
    def render_choix_joueur(
        self, p_liste_joueurs: List[dict], p_objet_tournoi: Tournoi
    ) -> List[str]:
        """Affiche la liste des joueurs disponibles et permet à l'utilisateur d'en choisir 4.

        Args:
            p_liste_joueurs (List[dict]): Liste des joueurs disponibles,
                chaque joueur étant représenté sous forme de dictionnaire
                avec les clés 'id_tinydb', 'identifiant_national_echec',
                'nom_famille', 'prenom' et 'date_naissance'.

        Returns:
            List[str]: Liste contenant les identifiants des joueurs sélectionnés par l'utilisateur.
        """

        # Trie par ordre alphabétique de nom et prénom
        joueurs_trie_nom_prenom = sorted(
            p_liste_joueurs,
            key=lambda joueur: (joueur["nom_famille"], joueur["prenom"]),
        )

        liste_choix = []

        for i, joueur in enumerate(joueurs_trie_nom_prenom):

            liste_choix.append(
                f"{i+1} - {joueur['nom_famille']} {joueur['prenom']} {joueur['identifiant_national_echec']}"
            )

        l_choix_joueur = []

        for _ in range(4):
            joueur = questionary.select(
                "Veuillez choisir un joueur parmi la liste :", choices=liste_choix
            ).ask()
            joueur_sans_numero = joueur.split(" - ", 1)[1]

            self.console.print(
                f"\n [bold green] {joueur_sans_numero} ajouté au tournoi {p_objet_tournoi.nom_tournoi}!\n[/bold green]"
            )

            identifiant_choisi = joueur.split(" - ")[0]
            print(identifiant_choisi)

            l_choix_joueur.append(identifiant_choisi)

            # Enleve le joueur qui vient d'être choisi pour éviter qu'il ne soit choisi à nouveau
            liste_choix.remove(joueur)

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
