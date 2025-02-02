class Tournoi:
    def __init__(
        self,
        p_nom_tournoi,
        p_lieu_tournoi,
        p_date_debut_tournoi,
        p_date_fin_tournoi,
        p_numero_tour_actuel,
        p_nombre_tours=4,
        p_description=None,
    ):
        self.identifiant = 0  # A définir
        self.nom_tournoi = p_nom_tournoi
        self.lieu_tournoi = p_lieu_tournoi
        self.date_debut_tournoi = p_date_debut_tournoi
        self.date_fin_tournoi = p_date_fin_tournoi
        self.nombre_tours = p_nombre_tours
        self.numero_tour_actuel = p_numero_tour_actuel
        self.liste_tours = []
        self.liste_joueur = []
        self.description = p_description

    # Fonctionnalités prévues dans le diagramme de classe qu'il faudra mettre dans les bonnes parties modèle,
    # vue ou controleur

    def creer_tournoi(self):
        # Logique à implémenter plus tard
        pass

    def lister_joueur_tournoi(self):
        # Logique à implémenter plus tard
        pass

    def generer_paires(self):
        # Logique à implémenter plus tard
        pass

    def selectionner_joueur(self):
        # Logique à implémenter plus tard
        pass
