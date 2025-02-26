from rich.table import Table
import questionary
from typing import List
from models.tournoi import Tournoi
from views.vue import Vue
import re
from datetime import datetime


class TournoiVue(Vue):
    """Gère l'affichage des informations liées aux tournois avec la bibliothèque Rich."""

    #
    # Surcharge la methode valider_nom() de la classe parente Vue pour accepter les chiffres dans le nom d'un tournoi
    def valider_nom(self, p_saisie):
        """
        Vérifie que la saisie du nom et du prénom est valide.

        Un nom ou un prénom valide :
        - Ne doit pas être vide.
        - Ne doit contenir que des lettres (avec accents), un tiret (-), des chiffres et des espaces.

        Args:
            saisie (str): La valeur saisie par l'utilisateur.

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

        Args:
            p_liste_objets_tournois list[Tournoi]: Liste d'objets tournoi
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
            table.add_row(
                f"[{couleur}]{o_tournoi.identifiant}[/{couleur}]",
                f"[{couleur}]{o_tournoi.nom_tournoi}[/{couleur}]",
                f"[{couleur}]{o_tournoi.date_debut_tournoi}[/{couleur}]",
                f"[{couleur}]{o_tournoi.date_fin_tournoi}[/{couleur}]",
            )

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
        self, p_objet_tournoi: Tournoi
    ) -> None:
        """Affiche les informations du tournoi choisi

        Args:
            p_objet_tournoi Tournoi : objet tournoi
        """

        liste_nom_joueurs = []
        for o_joueur in p_objet_tournoi.liste_joueurs:
            nom_joueur = o_joueur.nom_famille
            prenom_joueur = o_joueur.prenom
            s_joueur = f"{nom_joueur} {prenom_joueur}"
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
            p_objet_tournoi.description if p_objet_tournoi.description else "Aucune description",
        )
        table_tournoi.add_row("\n")
        table_tournoi.add_row("👥 Joueurs", "\n".join(joueur_alpha))

        self.console.print(table_tournoi)

    #
    def render_visualiser_tour_match_tournoi(self, p_objet_tournoi: Tournoi):

        print("\n")
        print(f"🏆 Déroulé du Tournoi {p_objet_tournoi.nom_tournoi}")


        # for o_tour in p_objet_tournoi.liste_tours:
        #     print(o_tour.nom)
        #     print(o_tour.statut)
        #     print(o_tour.date_heure_debut)
        #     print(o_tour.date_heure_fin)

        #     for o_match in o_tour.liste_matchs:
        #         print(o_match.nom_match)
        #         print(o_match.joueur_blanc.nom_famille)
        #         print(o_match.score_blanc)
        #         print(o_match.joueur_noir.nom_famille)
        #         print(o_match.score_noir)
        #         print(o_match.statut)

        for o_tour in p_objet_tournoi.liste_tours:
            table_tour = Table(title=f"🔄 {o_tour.nom} ({o_tour.statut})", title_style="bold magenta", show_header=False,)
            table_tour.add_column("Détail", style="bold white", justify="left")
            table_tour.add_column("Valeur", style="bold cyan", justify="left")

            table_tour.add_row("📅 Début", o_tour.date_heure_debut if o_tour.date_heure_debut else "Non renseigné")
            table_tour.add_row("🗓️  Fin", o_tour.date_heure_fin if o_tour.date_heure_fin else "Non terminé")

            self.console.print(table_tour)
            self.console.print("\n")

            # 🎯 Tableau des matchs de ce tour
            table_matchs = Table(title="⚔️  Matchs du Tour", title_style="bold yellow")
            table_matchs.add_column("🏳️  Joueur Blanc", justify="center", style="bold white")
            table_matchs.add_column("⚖️  Score Blanc", justify="center", style="bold cyan")
            table_matchs.add_column("⚔️  VS", justify="center", style="bold red")
            table_matchs.add_column("⚖️  Score Noir", justify="center", style="bold cyan")
            table_matchs.add_column("🏴 Joueur Noir", justify="center", style="bold white")
            table_matchs.add_column("📌 Statut", justify="center", style="bold green")

            for o_match in o_tour.liste_matchs:
                table_matchs.add_row(
                    f"{o_match.joueur_blanc.nom_famille} {o_match.joueur_blanc.prenom}",
                    str(o_match.score_blanc),
                    "🆚",
                    str(o_match.score_noir),
                    f"{o_match.joueur_noir.nom_famille} {o_match.joueur_noir.prenom}"
                    ,
                    o_match.statut,
                )

            self.console.print(table_matchs)
            self.console.print("\n")

    #
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
            "p_nombre_tour_tournoi": questionary.text(
                "Entrez le nombre de tour du tournoi (4 par défaut) :",
                default=Tournoi.nombre_tours_defaut,
            ).ask(),
            "p_description_tournoi": questionary.text(
                "Entrez la desription du tournoi  :", validate=self.valider_nom
            ).ask(),
        }

        return d_infos_tournoi
