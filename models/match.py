class Match:
    """Représente un match entre deux joueurs lors d'un tout dans un tournoi d'échecs."""

    def __init__(
        self,
        p_identifiant: int,
        p_joueur_blanc: str,
        p_joueur_noir: str,
        p_score_blanc: float = 0.0,
        p_score_noir: float = 0.0,
        p_statut: str = "En cours",
    ):
        """Initialise un match avec les joueurs, leur score et le statut.

        Args:
            p_identifiant (int): Identifiant unique du match.
            p_joueur_blanc (str): Nom ou identifiant du joueur blanc.
            p_joueur_noir (str): Nom ou identifiant du joueur noir.
            p_score_blanc (float, optional): Score du joueur blanc (par défaut 0).
            p_score_noir (float, optional): Score du joueur noir (par défaut 0).
            p_statut (str, optional): Statut du match ("En cours", "Terminé"). Par défaut, "En cours".
        """
        self.identifiant = p_identifiant
        self.joueur_blanc = p_joueur_blanc
        self.joueur_noir = p_joueur_noir
        self.score_blanc = p_score_blanc
        self.score_noir = p_score_noir
        self.statut = p_statut
        self.nom_match = f"Match {p_identifiant} - {p_joueur_blanc} VS {p_joueur_noir}"
