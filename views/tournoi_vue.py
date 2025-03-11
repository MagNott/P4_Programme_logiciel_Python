from rich.table import Table
import questionary
from typing import List
from models.tournoi import Tournoi
from views.vue import Vue
import re
from datetime import datetime


class TournoiVue(Vue):
    """
    Gère l'affichage des informations liées aux tournois avec la bibliothèque Rich.

    Cette classe hérite de `Vue` et fournit des méthodes pour :
    - Afficher des informations sur les tournois (liste, détails, matches...).
    - Valider les saisies utilisateur spécifiques aux tournois.
    - Gérer les interactions via `questionary`.
    """

    #
    # Surcharge la methode valider_nom() de la classe parente Vue pour accepter les chiffres dans le nom d'un tournoi
    def valider_nom(self, p_saisie: str) -> str | bool:
        """
        Vérifie que la saisie du nom d'un tournoi est valide.

        Un nom de tournoi valide :
        - Ne doit pas être vide.
        - Ne doit contenir que des lettres (avec accents), des chiffres, des tirets (-) et des espaces.

        Args:
            p_saisie (str): La valeur saisie par l'utilisateur.

        Returns:
            str | bool: Un message d'erreur si invalide, sinon `True` si la saisie est correcte.
        """

        if not p_saisie.strip():
            return "Le champ ne peut pas être vide."
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s-]+$", p_saisie):
            return (
                "La saisie ne doit contenir que des lettres, des tirets et des espaces."
            )

        return True

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
        Returns:
            None
        """

        table = Table(
            title="\n✅ Tournoi ajouté avec succès",
            title_style="bold green",
            show_header=False,
        )
        table.add_column("Info", style="bold white", justify="left")
        table.add_column("Tournoi", style="bold cyan", justify="left")

        table.add_row("🏆 Nom du tournoi", p_nom_tournoi)
        table.add_row("📍 Lieu", p_lieu_tournoi)
        table.add_row("📅 Début", p_date_debut_tournoi)
        table.add_row("📅 Fin", p_date_fin_tournoi)
        table.add_row("🔄 Nombre de tours", str(p_nombre_tour_tournoi))
        table.add_row(
            "📝 Description",
            p_description_tournoi if p_description_tournoi else "Aucune description",
        )

        self.console.print(table)

    #
    def render_lister_tournois(self, p_liste_objets_tournois: list[Tournoi]) -> None:
        """Affiche la liste des tournois enregistrés dans la base de données.

        Les tournois sont triés par date de début avant affichage.

        Args:
            p_liste_objets_tournois (list[Tournoi]): Liste d'objets tournoi

        Returns:
            None
        """
        # Range les tournois par ordre croissant de date
        p_liste_objets_tournois = sorted(
            p_liste_objets_tournois,
            key=lambda tournoi: datetime.strptime(
                tournoi.date_debut_tournoi, "%d-%m-%Y"
            ),
        )

        table = Table(title="\n 🏆 Liste des Tournois", title_style="bold blue")

        table.add_column("ID", style="bold cyan", justify="center")
        table.add_column("Nom du tournoi", style="bold white", justify="left")
        table.add_column("Date de début", style="bold magenta", justify="center")
        table.add_column("Date de fin", style="bold magenta", justify="center")

        # Couleurs alternées pour chaque ligne
        couleurs_lignes = ["cyan", "magenta"]

        for i, o_tournoi in enumerate(p_liste_objets_tournois):
            couleur = couleurs_lignes[i % len(couleurs_lignes)]

            # Reformater les dates pour forcer les 0 initiaux
            date_debut = datetime.strptime(
                o_tournoi.date_debut_tournoi, "%d-%m-%Y"
            ).strftime("%d-%m-%Y")
            date_fin = datetime.strptime(
                o_tournoi.date_fin_tournoi, "%d-%m-%Y"
            ).strftime("%d-%m-%Y")

            table.add_row(
                f"[{couleur}]{o_tournoi.identifiant}[/{couleur}]",
                f"[{couleur}]{o_tournoi.nom_tournoi}[/{couleur}]",
                f"[{couleur}]{date_debut}[/{couleur}]",
                f"[{couleur}]{date_fin}[/{couleur}]",
            )

        self.console.print(table)

    #
    def render_impossible_inscription(self, p_nom_tournoi: Tournoi) -> None:
        """
        Affiche un message d'erreur si l'inscription au tournoi est impossible.

        Args:
            p_nom_tournoi (Tournoi): L'objet tournoi concerné.

        Returns:
            None
        """
        message = (
            f"\n [bold red] Le tournoi {p_nom_tournoi} a déjà commencé, "
            "il n'est pas possible d'y inscrire des joueurs !\n[/bold red]"
        )
        self.console.print(message)

    #
    def render_choix_joueur(
        self, p_liste_joueurs: List[dict], p_objet_tournoi: Tournoi
    ) -> List[str]:
        """
        Affiche la liste des joueurs disponibles et permet à l'utilisateur d'en choisir plusieurs.

        Args:
            p_liste_joueurs (list[dict]): Liste des joueurs disponibles sous forme de dictionnaires
            p_objet_tournoi (Tournoi): L'objet tournoi auquel les joueurs seront inscrits.

        Returns:
            list[str]: Liste des identifiants des joueurs sélectionnés par l'utilisateur.
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

        nombre_joueurs = questionary.text(
            "Combien de joueurs souhaitez-vous inscrire à ce tournoi (nombres paires):",
            validate=self._valider_nombre_joueurs,
        ).ask()

        for _ in range(int(nombre_joueurs)):
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
    def render_choix_nombre_tour(self, p_objet_tournoi: Tournoi) -> int:
        """
        Affiche une invite pour permettre à l'utilisateur de choisir le nombre de tours du tournoi.

        Cette méthode utilise `questionary` pour demander à l'utilisateur de saisir le nombre de tours
        du tournoi. Une validation est effectuée pour s'assurer que l'entrée est un entier valide
        supérieur à zéro. La valeur choisie est ensuite assignée à l'attribut `nombre_tours` de l'objet
        `Tournoi` et retournée sous forme d'entier.

        Args:
            p_objet_tournoi (Tournoi): L'objet tournoi dont on souhaite paramétrer le nombre de tours.

        Returns:
            int: Le nombre de tours sélectionné par l'utilisateur.
        """

        s_nombre_tours = questionary.text(
                "Entrez le nombre de tour du tournoi (4 par défaut) :",
                default=str(Tournoi.nombre_tours_defaut), validate=self.valider_nombre_tour
            ).ask()

        return int(s_nombre_tours)

    #
    def render_visualiser_tournoi(
        self, p_objet_tournoi: Tournoi, p_scores_joueurs: dict
    ) -> None:
        """
        Affiche les détails d'un tournoi sélectionné, y compris les joueurs et leurs scores.

        Args:
            p_objet_tournoi (Tournoi): L'objet tournoi à afficher.
            p_scores_joueurs (dict): Dictionnaire des scores des joueurs.

        Returns:
            None
        """

        liste_nom_joueurs = []
        for o_joueur in p_objet_tournoi.liste_joueurs:
            nom_joueur = o_joueur.nom_famille
            prenom_joueur = o_joueur.prenom
            i_score_joueur = p_scores_joueurs[o_joueur.identifiant_tinydb]
            s_joueur = f"{nom_joueur} {prenom_joueur} - {i_score_joueur} point(s)"
            liste_nom_joueurs.append(s_joueur)

        joueur_alpha = sorted(liste_nom_joueurs)

        print("\n")
        table_tournoi = Table(
            title="🏆 Informations du Tournoi",
            title_style="bold blue",
            show_header=False,
        )

        table_tournoi.add_column("Détail", style="bold white", justify="left")
        table_tournoi.add_column("Valeur", style="bold cyan", justify="left")

        table_tournoi.add_row("🏷️  Nom", p_objet_tournoi.nom_tournoi)
        table_tournoi.add_row("📍 Lieu", p_objet_tournoi.lieu_tournoi)
        table_tournoi.add_row("📅 Début", p_objet_tournoi.date_debut_tournoi)
        table_tournoi.add_row("🗓️  Fin", p_objet_tournoi.date_fin_tournoi)
        table_tournoi.add_row("🔄 Nombre de tours", str(p_objet_tournoi.nombre_tours))
        table_tournoi.add_row(
            "📝 Description",
            (
                p_objet_tournoi.description
                if p_objet_tournoi.description
                else "Aucune description"
            ),
        )
        table_tournoi.add_row("\n")
        table_tournoi.add_row("👥 Joueurs", "\n".join(joueur_alpha))

        self.console.print(table_tournoi)

    #
    def render_visualiser_tour_match_tournoi(self, p_objet_tournoi: Tournoi) -> None:
        """
        Affiche le déroulé des tours et des matchs du tournoi sélectionné.

        Args:
            p_objet_tournoi (Tournoi): L'objet tournoi à afficher.

        Returns:
            None
        """

        print("\n")
        print(f"🏆 Déroulé du Tournoi {p_objet_tournoi.nom_tournoi}")

        for o_tour in p_objet_tournoi.liste_tours:
            table_tour = Table(
                title=f"🔄 {o_tour.nom} ({o_tour.statut})",
                title_style="bold magenta",
                show_header=False,
            )
            table_tour.add_column("Détail", style="bold white", justify="left")
            table_tour.add_column("Valeur", style="bold cyan", justify="left")

            table_tour.add_row(
                "📅 Début",
                o_tour.date_heure_debut if o_tour.date_heure_debut else "Non renseigné",
            )
            table_tour.add_row(
                "🗓️  Fin",
                o_tour.date_heure_fin if o_tour.date_heure_fin else "Non terminé",
            )

            self.console.print(table_tour)
            self.console.print("\n")

            # 🎯 Tableau des matchs de ce tour
            table_matchs = Table(title="⚔️  Matchs du Tour", title_style="bold yellow")
            table_matchs.add_column(
                "🏳️  Joueur Blanc", justify="center", style="bold white"
            )
            table_matchs.add_column(
                "⚖️  Score Blanc", justify="center", style="bold cyan"
            )
            table_matchs.add_column("⚔️  VS", justify="center", style="bold red")
            table_matchs.add_column(
                "⚖️  Score Noir", justify="center", style="bold cyan"
            )
            table_matchs.add_column(
                "🏴 Joueur Noir", justify="center", style="bold white"
            )
            table_matchs.add_column("📌 Statut", justify="center", style="bold green")

            for o_match in o_tour.liste_matchs:
                table_matchs.add_row(
                    f"{o_match.joueur_blanc.nom_famille} {o_match.joueur_blanc.prenom}",
                    str(o_match.score_blanc),
                    "🆚",
                    str(o_match.score_noir),
                    f"{o_match.joueur_noir.nom_famille} {o_match.joueur_noir.prenom}",
                    o_match.statut,
                )

            self.console.print(table_matchs)
            self.console.print("\n")

    #
    def valider_nombre_tour(self, p_saisie: str) -> str | bool:
        """
        Vérifie que la saisie du nombre de tours est valide.

        Un nombre de tours valide :
        - Doit être un chiffre.
        - Doit être supérieur à 0.

        Args:
            p_saisie (str): La valeur saisie par l'utilisateur.

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
            validate=self.valider_date,
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
                validate=lambda date_fin: self.valider_date_fin(
                    date_fin, p_date_debut_tournoi
                ),
            ).ask(),
            "p_nombre_tour_tournoi": "A déterminer",
            "p_description_tournoi": questionary.text(
                "Entrez la desription du tournoi  :", validate=self.valider_nom
            ).ask(),
        }

        return d_infos_tournoi

    #
    # METHODES PRIVEES
    #
    def _valider_nombre_joueurs(self, p_saisie: str) -> str | bool:
        """
        Vérifie que l'entrée est un nombre pair valide pour le nombre de joueurs.

        Args:
            p_saisie (str): La valeur saisie par l'utilisateur.

        Returns:
            str | bool: Un message d'erreur si invalide, sinon `True` si la saisie est correcte.
        """

        if not p_saisie.isdigit():
            return "Veuillez entrer un **nombre valide** (chiffres uniquement)."

        nombre = int(p_saisie)

        if nombre % 2 != 0:
            return "Le nombre doit être **pair**."

        if nombre < 2:
            return "Il doit y avoir au **moins 2 joueurs**."

        return True
