# from controllers import TournoiControleur
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary


class TournoiVue:
    def __init__(self):
        self.console = Console()

    def render_confirm_ajout_tournoi(
        self,
        s_nom_tournoi,
        s_lieu_tournoi,
        s_date_debut_tournoi,
        s_date_fin_tournoi,
        s_nombre_tour_tournoi,
        s_description_tournoi,
    ):
        self.console.print(
            f"""\n[bold green]Tournoi ajouté avec succès : 
            {s_nom_tournoi},
            {s_lieu_tournoi},
            {s_date_debut_tournoi},
            {s_date_fin_tournoi},
            {s_nombre_tour_tournoi},
            {s_description_tournoi},
            [/bold green]\n"""
        )

    def render_choix_tournoi(self, liste_tournois):
        table = Table(title="Liste des tournois")
        table.add_column("nom du tournoi")

        for tournoi in liste_tournois:
            table.add_row(tournoi)

        self.console.print(table)
        # récupérer le choix de l'utilisateur
        return questionary.text("Veuillez choisir un tournoi par son identifiant : ").ask()

    def render_choix_joueur(self, liste_joueurs):
        table = Table(title="Liste des joueurs")
        table.add_column("Choix", justify="center")
        table.add_column("Id echec", justify="center")
        table.add_column("Nom de famille", justify="center")
        table.add_column("Prénom", justify="center")
        table.add_column("Date de naissance", justify="center")

        # Couleurs alternées pour chaque ligne
        couleurs_lignes = ["dim cyan", "dim magenta"]

        for i, joueur in enumerate(liste_joueurs):
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
            joueur = questionary.text("\n Veuillez choisir un joueur par son identifiant : ").ask()
            l_choix_joueur.append(joueur)
            self.console.print(f"\n [bold green] Joueur {joueur} ajouté à la liste.\n[/bold green]")
            compteur += 1
        return l_choix_joueur

    def render_visualiser_tournoi(self, p_tournoi, p_joueurs_db):
        """Affiche les informations du tournoi choisi.
        Args:
            p_tournoi (Dictionnaire): Dictionnaire tournoi
            p_joueurs_db (list): Liste des joueurs
        """
        liste_joueurs_ids = p_tournoi[0]["liste_joueurs"]

        joueurs_affiches = []
        # Faire correspondre l'id du joueur avec ses données
        for joueur_id in liste_joueurs_ids:
            for joueur in p_joueurs_db:
                if joueur["id_tinydb"] == joueur_id:
                    joueurs_affiches.append(f"{joueur['nom_famille']} {joueur['prenom']}")

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
