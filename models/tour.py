from models.tournoi import Tournoi


class Tour:
    """Représente un tour dans un tournoi d'échecs."""

    def __init__(
        self,
        p_identifiant: int,
        p_nom: str,
        p_tournoi: Tournoi,
        p_statut="En cours",
        p_date_heure_debut=None,
        p_date_heure_fin=None,
    ):
        """Initialise un tour avec son identifiant, nom et statut.

        Args:
            p_identifiant (int): Numéro du tour dans le tournoi.
            p_nom (str): Nom du tour (ex: "Round 1", "Round 2").
        """
        self.identifiant = p_identifiant
        self.nom = p_nom
        self.statut = p_statut
        self.liste_matchs = []
        self.date_heure_debut = p_date_heure_debut
        self.date_heure_fin = p_date_heure_fin
        self.tournoi = p_tournoi
