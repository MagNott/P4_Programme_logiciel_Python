from rich.console import Console
import re
from datetime import datetime
import questionary


class Vue:
    """
    Classe parente pour les vues, utilisée pour gérer l'affichage et la validation des saisies utilisateur.

    Cette classe fournit des méthodes pour afficher les interfaces interactives et valider
    les entrées utilisateur, notamment les noms, les dates et la sélection de tournois.
    """

    def __init__(self):
        """Initialise l'affichage en configurant la console Rich pour une sortie stylisée.

        Cette méthode configure la console `Rich` pour permettre un affichage amélioré
        des informations dans le terminal.
        """
        self.console = Console()

#
    # Préparation des méthodes de validation pour la saisie d'un nouveau joueur
    # Elles sont utilisées dans render_saisie_joueur()
    def valider_nom(self, p_saisie: str) -> str | bool:
        """
        Vérifie que la saisie du nom et du prénom est valide.

        Un nom ou un prénom valide :
        - Ne doit pas être vide.
        - Ne doit contenir que des lettres (avec accents), un tiret (-) et des espaces.

        Args:
            saisie (str): La valeur saisie par l'utilisateur.

        Returns:
            str | bool: Un message d'erreur si invalide, sinon `True` si la saisie est correcte.
    """
        if not p_saisie.strip():
            return "Le champ ne peut pas être vide."
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s-]+$", p_saisie):
            return "La saisie ne doit contenir que des lettres, des tirets et des espaces."
        return True

    #
    def valider_date(self, p_saisie: str) -> str | bool:
        """
        Vérifie que la date saisie est valide.

        Une date valide :
        - Suit le format JJ/MM/AAAA.
        - Correspond à une vraie date (ex : 31/02/2023 est invalide).

        Args:
            p_saisie (str): La valeur saisie par l'utilisateur.

        Returns:
            str | bool: Un message d'erreur si invalide, sinon `True` si la saisie est correcte.
        """
        # strptime() peut faire planter le programme si la saisie n'est pas bonne donc il faut utiliser un try/except
        try:
            datetime.strptime(p_saisie, "%d-%m-%Y")
            return True
        except ValueError:
            return "Format invalide ou date incorrecte. Utilisez JJ-MM-AAAA."

#
    def valider_date_fin(self, p_date_fin: str, p_date_debut: str) -> str | bool:
        """
        Vérifie que la date de fin est valide et postérieure à la date de début.

        Cette fonction s'assure d'abord que la date de fin est bien au format attendu et valide,
        puis vérifie qu'elle est égale ou postérieure à la date de début.

        Args:
            p_date_fin (str): La date de fin du tournoi saisie par l'utilisateur.
            p_date_debut (str): La date de début du tournoi pour la comparaison.

        Returns:
            str | bool: Un message d'erreur si invalide, sinon `True` si la saisie est correcte.
        """
        # Vérifier si la date est valide d'abord
        if self.valider_date(p_date_fin) is not True:
            return self.valider_date(p_date_fin)  # Retourner l'erreur de format si nécessaire

        # Convertir en objets datetime pour la comparaison
        date_debut_objet = datetime.strptime(p_date_debut, "%d-%m-%Y")
        date_fin_objet = datetime.strptime(p_date_fin, "%d-%m-%Y")

        if date_fin_objet < date_debut_objet:
            return "La date de fin doit égale ou supérieure à la date de début."
        return True  # La validation est réussie

#
    def render_choix_tournoi(self, p_liste_tournois: list[str]) -> str:
        """Permet à l'utilisateur de choisir un tournoi parmi une liste.

        Cette fonction extrait les identifiants et noms des tournois à partir
        des fichiers JSON disponibles, puis les affiche sous forme de choix interactifs.

        Args:
            liste_tournois (list[str]): Liste des noms de fichiers représentant les tournois disponibles.

        Returns:
            str: Identifiant du tournoi choisi par l'utilisateur, saisi via l'interface interactive.
        """

        # Regex pour extraire l'ID, le nom et la date depuis le nom de fichier
        regex = r"tournoi_(\d+)_([^_]+)_(\d{1,2}-\d{1,2}-\d{4})\.json"

        liste_choix = []
        liste_tournoi_identifiant = {}

        for fichier in p_liste_tournois:
            match = re.match(regex, fichier)
            if match:
                tournoi_id = match.group(1)
                nom_tournoi = match.group(2).replace("_", " ")  # Remettre les espaces
                date_tournoi = match.group(3)

                choix_affichage = f"{tournoi_id} - {nom_tournoi} - {date_tournoi}"
                liste_choix.append(choix_affichage)
                liste_tournoi_identifiant[choix_affichage] = tournoi_id  # Associer le choix à l'ID réel

        # Demander à l'utilisateur de choisir un tournoi dans la liste
        choix_utilisateur = questionary.select(
            "Veuillez choisir un tournoi :", choices=sorted(liste_choix)
        ).ask()

        # Retourner uniquement l'ID du tournoi selectionné
        return liste_tournoi_identifiant[choix_utilisateur]

    #
    def afficher_message(self, p_message: str, p_message_type: str) -> None:
        """
        Affiche un message coloré en fonction du type de message.

        Args:
            p_message (str): Le message à afficher.
            p_message_type (str): Type du message ("success", "error", "info").
                                - "success" (vert) : Succès.
                                - "error" (rouge) : Erreur.
                                - "info" (cyan) : Information.

        Returns:
            None: Affiche le message formaté dans la console.
        """

        p_message = f"\n{p_message}\n"

        if p_message_type == "success":
            self.console.print(p_message, style="bold green")
        elif p_message_type == "error":
            self.console.print(p_message, style="bold red")
        elif p_message_type == "info":
            self.console.print(p_message, style="bold cyan")
        else:
            self.console.print(p_message)
