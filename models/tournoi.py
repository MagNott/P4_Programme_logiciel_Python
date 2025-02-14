import os
import re


class Tournoi:
    def __init__(
        self,
        p_identifiant: int,
        p_nom_tournoi: str,
        p_lieu_tournoi: str,
        p_date_debut_tournoi: str,
        p_date_fin_tournoi: str,
        p_nombre_tours: int = 4,
        p_description: str | None = None,
        p_liste_tours: list = [],
    ) -> None:
        """Initialise un tournoi avec ses détails.

        Args:
            p_identifiant (int): Identifiant unique du tournoi.
            p_nom_tournoi (str): Nom du tournoi.
            p_lieu_tournoi (str): Lieu où se déroule le tournoi.
            p_date_debut_tournoi (str): Date de début du tournoi (format JJ/MM/AAAA).
            p_date_fin_tournoi (str): Date de fin du tournoi (format JJ/MM/AAAA).
            p_nombre_tours (int, optional): Nombre total de tours dans le tournoi. Par défaut à 4.
            p_description (str | None, optional): Description optionnelle du tournoi. Par défaut à None.
        """
        self.identifiant = p_identifiant
        self.nom_tournoi = p_nom_tournoi
        self.lieu_tournoi = p_lieu_tournoi
        self.date_debut_tournoi = p_date_debut_tournoi
        self.date_fin_tournoi = p_date_fin_tournoi
        self.nombre_tours = p_nombre_tours
        self.liste_joueurs = []
        self.description = p_description
        self.liste_tours = p_liste_tours

#
    @classmethod
    def generer_identifiant(cls) -> int:
        """Génère un identifiant unique pour un nouveau tournoi.

        Cette méthode recherche les fichiers existants dans le dossier `data/tournaments/`
        et extrait les identifiants numériques des tournois déjà créés.
        Elle attribue ensuite le plus grand identifiant + 1 au prochain tournoi.
        @classmethod → Permet d’appeler cette méthode sans instancier un objet de la classe Tournoi

        Returns:
            int: Nouvel identifiant unique du tournoi.
        """

        # Préparation de la regex pour extraire le numéro du tournoi à partir du nom du fichier
        regex = r"tournoi_(\d+)\.json"
        l_fichiers = os.listdir('data/tournaments')
        identifiants = []

        if not l_fichiers:
            identifiant_a_attribuer = 1
        else:
            for fichier in l_fichiers:
                id = re.search(regex, fichier)
                if id:
                    # group(1) récupère la partie capturée entre les parenthèses de la regex
                    identifiants.append(int(id.group(1)))

            identifiant_maximum = max(identifiants)
            identifiant_a_attribuer = identifiant_maximum + 1

        return identifiant_a_attribuer
