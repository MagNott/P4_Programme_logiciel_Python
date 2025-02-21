

class Joueur:
    """Représente un joueur d'échecs avec son identité et son identifiant national d'échec."""

    def __init__(
        self,
        p_identifiant_national_echec: str,
        p_nom_famille: str,
        p_prenom: str,
        p_date_naissance: str,
        p_identifiant_tinydb: int = None,
        p_score: float = 0,
    ) -> None:
        """Initialise un joueur avec ses informations.

        Args:
            p_identifiant (str): Identifiant national d'échecs du joueur.
            p_nom (str): Nom de famille du joueur.
            p_prenom (str): Prénom du joueur.
            p_date_naissance (str): Date de naissance du joueur (format JJ/MM/AAAA).
        """
        self.identifiant_national_echec = p_identifiant_national_echec
        self.nom_famille = p_nom_famille
        self.prenom = p_prenom
        self.date_naissance = p_date_naissance
        self.identifiant_tinydb = p_identifiant_tinydb
        self.score = p_score
