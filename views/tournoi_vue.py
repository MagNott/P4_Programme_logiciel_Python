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
        return questionary.text("Vueillez choisir un tournoi par son identifiant : ").ask()

    def render_choix_joueur(self, liste_joueurs):
        table = Table(title="Liste des joueurs")
        table.add_column("Identifiant", style="cyan")
        table.add_column("Nom de famille", style="magenta")
        table.add_column("Prénom", style="green")
        table.add_column("Date de naissance", style="blue")

        for joueur in liste_joueurs:
            table.add_row(
                str(joueur["identifiant_national_echec"]),
                joueur["nom_famille"],
                joueur["prenom"],
                joueur["date_naissance"],
            )

        self.console.print(table)
        # récupérer le choix de l'utilisateur
        return questionary.text("Veuillez choisir un joueur par son identifiant : ").ask()

    def lister_tournois():
        # Logique à implémenter plus tard
        pass

    def visualiser_tournoi():
        # Logique à implémenter plus tard
        pass
