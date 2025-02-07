# from controllers import JoueurControleur
from rich.console import Console
from rich.table import Table


class JoueurVue:
    def __init__(self):
        self.console = Console()

    def render_confirm_ajout_joueur(self, s_nom, s_classement):
        print(f"Joueur ajouté avec succès : {s_nom}, classement {s_classement}\n")

    def voir_joueur(self):
        # Aimplémenter
        pass

    def render_lister_joueur(self, liste_joueur):

        print("La liste des joueurs sont : \n")

        # Création de la table
        table = Table(title="Liste des joueurs")

        # Définir les colonnes
        table.add_column("Nom", justify="center")
        table.add_column("Prénom", justify="center")

        # Couleurs alternées pour chaque ligne
        couleurs_lignes = ["dim cyan", "dim magenta"]

        for i, o_joueur in enumerate(liste_joueur):
            couleur = couleurs_lignes[i % len(couleurs_lignes)]  # Alterner les couleurs
            table.add_row(
                f"[{couleur}]{o_joueur.nom_famille}[/{couleur}]",
                f"[{couleur}]{o_joueur.prenom}[/{couleur}]"
            )

        self.console.print(table)
