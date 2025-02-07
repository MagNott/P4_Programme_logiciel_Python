# from controllers import JoueurControleur
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class JoueurVue:
    def __init__(self):
        self.console = Console()

    def render_confirm_ajout_joueur(
        self, s_identifiant, s_nom, s_prenom, s_date_naissance
    ):
        self.console.print(f"""\n[bold green]Joueur ajouté avec succès : 
            {s_identifiant}, 
            {s_nom}, 
            {s_prenom}, 
            {s_date_naissance}[/bold green]\n"""
        )

    def voir_joueur(self):
        # Aimplémenter
        pass

    def render_lister_joueur(self, liste_joueur):

        # Création de la table
        table = Table(title="\n Liste des joueurs")

        # Définir les colonnes
        table.add_column("Identifiant", justify="center")
        table.add_column("Nom", justify="center")
        table.add_column("Prénom", justify="center")
        table.add_column("Date de naissance", justify="center")

        # Couleurs alternées pour chaque ligne
        couleurs_lignes = ["dim cyan", "dim magenta"]

        for i, o_joueur in enumerate(liste_joueur):
            couleur = couleurs_lignes[i % len(couleurs_lignes)]  # Alterner les couleurs
            table.add_row(
                f"[{couleur}]{o_joueur.identifiant_national_echec}[/{couleur}]",
                f"[{couleur}]{o_joueur.nom_famille}[/{couleur}]",
                f"[{couleur}]{o_joueur.prenom}[/{couleur}]",
                f"[{couleur}]{o_joueur.date_naissance}[/{couleur}]",
            )

        self.console.print(table)
