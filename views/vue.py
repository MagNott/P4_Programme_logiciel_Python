from rich.console import Console
import re
from datetime import datetime
import questionary


class Vue:
    """Classe parente pour les vues"""

    def __init__(self):
        """Initialise l'affichage en configurant la console Rich pour une sortie stylisée."""
        self.console = Console()

#
    # Préparation des méthodes de validation pour la saisie d'un nouveau joueur
    # Elles sont utilisées dans render_saisie_joueur()
    def valider_nom(self, p_saisie):
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
    def valider_date(self, p_saisie):
        """
        Vérifie que la date saisie est valide.

        Une date valide :
        - Suit le format JJ/MM/AAAA.
        - Correspond à une vraie date (ex : 31/02/2023 est invalide).

        Args:
            saisie (str): La valeur saisie par l'utilisateur.

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
    def valider_date_fin(self, p_date_fin, p_date_debut):
        """Valide que la date de fin est postérieure à la date de début."""
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

        Args:
            liste_tournois (list[str]): Liste des noms de fichiers représentant les tournois disponibles.

        Returns:
            str: Identifiant du tournoi choisi par l'utilisateur, saisi via l'interface interactive.
        """

        regex = r"tournoi_(\d+)_([^_]+)_(\d{2}-\d{2}-\d{4})\.json"

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

        # Retourner uniquement l'ID du tournoi
        return liste_tournoi_identifiant[choix_utilisateur]
