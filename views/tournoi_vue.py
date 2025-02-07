# from controllers import TournoiControleur
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class TournoiVue:
    def __init__(self):
        self.console = Console()

    def render_confirm_ajout_joueur(
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

    def lister_tournois():
        # Logique à implémenter plus tard
        pass

    def visualiser_tournoi():
        # Logique à implémenter plus tard
        pass
