import os
import re

class Tournoi:
    def __init__(
        self,
        p_nom_tournoi,
        p_lieu_tournoi,
        p_date_debut_tournoi,
        p_date_fin_tournoi,
        p_nombre_tours=4,
        p_description=None,
    ):
        self.identifiant = self.generer_identifiant()
        self.nom_tournoi = p_nom_tournoi
        self.lieu_tournoi = p_lieu_tournoi
        self.date_debut_tournoi = p_date_debut_tournoi
        self.date_fin_tournoi = p_date_fin_tournoi
        self.nombre_tours = p_nombre_tours
        self.numero_tour_actuel = 1
        self.liste_tours = []
        self.liste_joueur = []
        self.description = p_description

    # Fonctionnalités prévues dans le diagramme de classe qu'il faudra mettre dans les bonnes parties modèle,
    # vue ou controleur

    def generer_identifiant(self):
        regex = r"tournoi_(\d+)\.json"
        a_fichiers = os.listdir('data/tournaments')
        identifiants = []

        if not a_fichiers:
            identifiant_a_attribuer = 1
        else:
            for fichier in a_fichiers:
                id = re.search(regex, fichier)
                if id:
                    identifiants.append(int(id.group(1)))

            identifiant_maximum = max(identifiants)
            identifiant_a_attribuer = identifiant_maximum + 1

        return identifiant_a_attribuer

    
    def lister_joueur_tournoi(self):
        # Logique à implémenter plus tard
        pass

    def generer_paires(self):
        # Logique à implémenter plus tard
        pass

    def selectionner_joueur(self):
        # Logique à implémenter plus tard
        pass
