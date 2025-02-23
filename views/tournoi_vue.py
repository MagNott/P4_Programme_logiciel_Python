from rich.table import Table
import questionary
from typing import List
from models.tournoi import Tournoi
from views.vue import Vue
from datetime import datetime
import re


class TournoiVue(Vue):
    """Gère l'affichage des informations liées aux tournois avec la bibliothèque Rich."""

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

        table = Table(title="\n✅ Tournoi ajouté avec succès", title_style="bold green", show_header=False)
        table.add_column("Info", style="bold white", justify="left")
        table.add_column("Tournoi", style="bold cyan", justify="left")

        table.add_row("🏆 Nom du tournoi", p_nom_tournoi)
        table.add_row("📍 Lieu", p_lieu_tournoi)
        table.add_row("📅 Début", p_date_debut_tournoi)
        table.add_row("📅 Fin", p_date_fin_tournoi)
        table.add_row("🔄 Nombre de tours", str(p_nombre_tour_tournoi))
        table.add_row("📝 Description", p_description_tournoi if p_description_tournoi else "Aucune description")

        self.console.print(table)

#
    def render_lister_tournois(self, p_liste_tournois: list[str]) -> None:
        """Affiche la liste des tournois enregistrés dans la base de données.

        Args:
            p_liste_tournois (list[dict[str, str]]): Liste de string contenant les informations des tournois.
        """

        table = Table(title="\n 🏆 Liste des Tournois", title_style="bold green")

        table.add_column("ID", style="bold cyan", justify="center")
        table.add_column("Nom du tournoi", style="bold white", justify="left")
        table.add_column("Date de début", style="bold magenta", justify="center")

        # Regex pour extraire les infos depuis le nom de fichier
        regex = r"tournoi_(\d+)_([^_]+)_(\d{2}-\d{2}-\d{4})\.json"

        for tournoi in p_liste_tournois:

            # Extraction des infos avec la regex
            match = re.match(regex, tournoi)
            if match:
                tournoi_id = match.group(1)
                nom_tournoi = match.group(2).replace("_", " ")  # Remettre les espaces
                date_debut = match.group(3)

                # jouter une ligne au tableau
                table.add_row(tournoi_id, nom_tournoi, date_debut)

        self.console.print(table)

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
        joueurs_affiches_str = "Pas de joueurs inscrits"

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

    def valider_nombre_tour(self, p_saisie):
        """
        Vérifie que la saisie du nombre de tour est valide.

        Un nom ou un prénom valide :
        - Ne doit pas être vide.
        - Ne doit contenir que des lettres (avec accents), un tiret (-) et des espaces.

        Args:
            saisie (str): La valeur saisie par l'utilisateur.

        Returns:
            str | bool: Un message d'erreur si invalide, sinon `True` si la saisie est correcte.
    """
        if not p_saisie.isdigit() or p_saisie == 0:
            return "Il faut saisir un chiffre et qu'il soit supérieur à 0."
        return True

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
        # Demander la date de début du tournoi d'abord
        p_date_debut_tournoi = questionary.text(
            "Entrez la date du début du tournoi (JJ-MM-AAAA) :",
            validate=self.valider_date
        ).ask()

        d_infos_tournoi = {
            "p_nom_tournoi": questionary.text(
                "Entrez le nom du tournoi  :", validate=self.valider_nom
            ).ask(),
            "p_lieu_tournoi": questionary.text(
                "Entrez le lieu du tournoi  :", validate=self.valider_nom
            ).ask(),
            "p_date_debut_tournoi": p_date_debut_tournoi,
            "p_date_fin_tournoi": questionary.text(
                "Entrez la date de fin du tournoi (JJ-MM-AAAA) :",
                validate=lambda date_fin: self.valider_date_fin(date_fin, p_date_debut_tournoi)
            ).ask(),
            "p_nombre_tour_tournoi": questionary.text(
                "Entrez le nombre de tour du tournoi (4 par défaut) :", default=Tournoi.nombre_tours_defaut,
            ).ask(),
            "p_description_tournoi": questionary.text(
                "Entrez la desription du tournoi  :", validate=self.valider_nom
            ).ask(),
        }

        return d_infos_tournoi
