from rich.console import Console
from rich.table import Table


class JoueurVue:
    """Gère l'affichage des informations liées aux joueurs avec la bibliothèque Rich."""

    def __init__(self):
        """Initialise l'affichage en configurant la console Rich pour une sortie stylisée."""
        self.console = Console()

#
    def render_saisie_joueur(self) -> dict:
        """Affiche des invites de commande pour saisir les informations d'un joueur et retourne les valeurs saisies.

        Cette méthode demande à l'utilisateur d'entrer les informations d'un joueur
        via une saisie dans le terminal et les stocke dans un dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les informations suivantes :
                - "p_identifiant" (str) : Identifiant national d'échecs du joueur.
                - "p_nom" (str) : Nom de famille du joueur.
                - "p_prenom" (str) : Prénom du joueur.
                - "p_date_naissance" (str) : Date de naissance du joueur (format JJ/MM/AAAA).
        """
        d_infos_joueur = {}
        d_infos_joueur["p_identifiant"] = self.console.input(
            "Entrez l'identifiant national d'échec : "
        )
        d_infos_joueur["p_nom"] = self.console.input("Entrez le nom du joueur : ")
        d_infos_joueur["p_prenom"] = self.console.input("Entrez le prénom du joueur : ")
        d_infos_joueur["p_date_naissance"] = self.console.input(
            "Entrez la date de naissance du joueur JJ/MM/AAAA : "
        )
        return d_infos_joueur

#
    def render_confirm_ajout_joueur(
        self, p_identifiant: str, p_nom: str, p_prenom: str, p_date_naissance: str
    ) -> None:
        """Affiche un message de confirmation après l'ajout d'un joueur.

        Args:
            p_identifiant (str): Identifiant national d'échecs du joueur.
            p_nom (str): Nom de famille du joueur.
            p_prenom (str): Prénom du joueur.
            p_date_naissance (str): Date de naissance du joueur au format "JJ/MM/AAAA".

        Returns:
            None: Cette méthode n'a pas de valeur de retour, elle affiche uniquement le message dans la console.
        """
        self.console.print(
            f"\n[bold green]Joueur ajouté avec succès :[/bold green] "
            f"[cyan]{p_identifiant}[/cyan] - [magenta]{p_nom} {p_prenom}[/magenta] "
            f"(Né(e) le [yellow]{p_date_naissance}[/yellow])\n"
        )

#
    def render_lister_joueur(self, p_liste_joueur: list) -> None:
        """Affiche la liste des joueurs sous forme de tableau dans la console.

        Args:
            p_liste_joueur (list): Liste des objets Joueur contenant les informations des joueurs.

        Returns:
            None: Cette méthode affiche uniquement le tableau dans la console.
        """
        # Création de la table
        table = Table(title="\n Liste des joueurs")

        # Définir les colonnes
        table.add_column("Identifiant", justify="center")
        table.add_column("Nom", justify="center")
        table.add_column("Prénom", justify="center")
        table.add_column("Date de naissance", justify="center")

        # Couleurs alternées pour chaque ligne
        couleurs_lignes = ["dim cyan", "dim magenta"]

        for i, o_joueur in enumerate(p_liste_joueur):
            couleur = couleurs_lignes[i % len(couleurs_lignes)]  # Alterner les couleurs
            table.add_row(
                f"[{couleur}]{o_joueur.identifiant_national_echec}[/{couleur}]",
                f"[{couleur}]{o_joueur.nom_famille}[/{couleur}]",
                f"[{couleur}]{o_joueur.prenom}[/{couleur}]",
                f"[{couleur}]{o_joueur.date_naissance}[/{couleur}]",
            )
        self.console.print(table)
