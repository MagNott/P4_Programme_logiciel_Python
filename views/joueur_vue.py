from rich.table import Table
import questionary
import re
from views.vue import Vue


class JoueurVue(Vue):
    """Gère l'affichage des informations liées aux joueurs avec la bibliothèque Rich."""

    #
    def valider_identifiant_echec(self, saisie):
        """
        Vérifie que l'identifiant national d'échecs est valide.

        Un identifiant valide :
        - Commence par 2 lettres majuscules ou minuscules.
        - Est suivi de 5 chiffres.

        Exemple valide : "AB12345"

        Args:
            saisie (str): La valeur saisie par l'utilisateur.

        Returns:
            str | bool: Un message d'erreur si invalide, sinon `True` si la saisie est correcte.
        """
        if not re.match(r"^[A-Za-z]{2}\d{5}$", saisie):
            return "Format invalide, doit contenir 2 lettres au début suivi de 5 chiffres. Exemple valide : AB12345."
        return True

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

        d_infos_joueur["p_identifiant"] = questionary.text(
            "Entrez l'identifiant national d'échec : ",
            validate=self.valider_identifiant_echec,
        ).ask()
        d_infos_joueur["p_nom"] = questionary.text(
            "Entrez le nom du joueur : ", validate=self.valider_nom
        ).ask()
        d_infos_joueur["p_prenom"] = questionary.text(
            "Entrez le prénom du joueur : ", validate=self.valider_nom
        ).ask()
        d_infos_joueur["p_date_naissance"] = questionary.text(
            "Entrez la date de naissance du joueur JJ-MM-AAAA : ",
            validate=self.valider_date,
        ).ask()
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
        """Affiche la liste des joueurs trié par ordre alphabétique sous forme de tableau dans la console.

        Args:
            p_liste_joueur (list): Liste des objets Joueur contenant les informations des joueurs.

        Returns:
            None: Cette méthode affiche uniquement le tableau dans la console.
        """

        # Trie par ordre alphabétique de nom et prénom
        joueurs_trie_nom_prenom = sorted(
            p_liste_joueur, key=lambda joueur: (joueur.nom_famille, joueur.prenom)
        )

        # Création de la table
        table = Table(title="\n 🏅 Liste des joueurs", title_style="bold blue")

        # Définir les colonnes
        table.add_column("Id Echec", justify="center")
        table.add_column("Nom", justify="center")
        table.add_column("Prénom", justify="center")
        table.add_column("Date de naissance", justify="center")
        table.add_column("Score", justify="center")

        # Couleurs alternées pour chaque ligne
        couleurs_lignes = ["cyan", "magenta"]

        for i, o_joueur in enumerate(joueurs_trie_nom_prenom):
            couleur = couleurs_lignes[i % len(couleurs_lignes)]  # Alterner les couleurs
            table.add_row(
                f"[{couleur}]{o_joueur.identifiant_national_echec}[/{couleur}]",
                f"[{couleur}]{o_joueur.nom_famille}[/{couleur}]",
                f"[{couleur}]{o_joueur.prenom}[/{couleur}]",
                f"[{couleur}]{o_joueur.date_naissance}[/{couleur}]",
                f"[{couleur}]{o_joueur.score:.1f}[/{couleur}]",
                # Pour garder un chiffre après la virgule : :.1f
                # : indique un formatage spécial, .1 pour garder 1 chiffre, f pour float
            )
        self.console.print(table)
