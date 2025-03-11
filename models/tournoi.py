from pathlib import Path
import re


class Tournoi:
    # Attribut de classe pour y accéder de partout
    nombre_tours_defaut: int = "4"

    def __init__(
        self,
        p_identifiant: int,
        p_nom_tournoi: str,
        p_lieu_tournoi: str,
        p_date_debut_tournoi: str,
        p_date_fin_tournoi: str,
        p_nombre_tours: int = None,
        p_description: str | None = None,
        p_liste_tours: list = [],
        p_liste_joueurs: list = [],
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
        self.nombre_tours = p_nombre_tours if p_nombre_tours is not None else Tournoi.nombre_tours_defaut
        self.liste_joueurs = p_liste_joueurs
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
        regex = r"tournoi_(\d+)_.*\.json"
        dossier_tournois = Path("data/tournaments")
        identifiants = []

        # Liste les fichiers dans le dossier `data/tournaments`
        o_iter_fichiers = dossier_tournois.iterdir()

        for fichier in o_iter_fichiers:
            if fichier.is_file():
                id_tournoi = re.search(regex, fichier.name)
                if id:
                    # group(1) récupère la partie capturée entre les parenthèses de la regex
                    identifiants.append(int(id_tournoi.group(1)))

        # return identifiant_a_attribuer
        if not identifiants:
            return 1  # Premier tournoi
        else:
            return max(identifiants) + 1  # Prochain ID disponible
