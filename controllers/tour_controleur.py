from models.tour import Tour
from views.tour_vue import TourVue
from models.gestionnaire_persistance import GestionnairePersistance


class TourControleur:
    """Contrôleur gérant les interactions entre la vue et le modèle pour les tours."""

    def __init__(self) -> None:
        """Initialise le contrôleur du tour avec la vue et le gestionnaire de persistance."""
        self.o_tour_vue = TourVue()
        self.o_gestionnaire_persistance = GestionnairePersistance()

#
    def creer_tour(self) -> None:
        """Crée un tour pour un tournoi choisi par l'utilisateur et l'enregistre."""

        # Lister les tournois existants
        l_liste_tournois = self.o_gestionnaire_persistance.lister_tournois()
        i_identifiant_tournoi = self.o_tour_vue.render_choix_tournoi(l_liste_tournois)

        # Récupérer l'objet Tournoi
        o_tournoi_choisi = self.o_gestionnaire_persistance.recuperer_objet_tournoi(i_identifiant_tournoi)

        # Vérifier s'il y a de la place pour un nouveau tour
        if len(o_tournoi_choisi.liste_tours) >= int(o_tournoi_choisi.nombre_tours):
            self.o_tour_vue.render_verification_tour_max("Ce tournoi a atteint son nombre maximal de tours.")
            return

            # Vérifier si des tours existent déjà et si le dernier est en cours ou terminé
        if o_tournoi_choisi.liste_tours:
            d_dernier_tour = o_tournoi_choisi.liste_tours[-1]
            # Vérifier si le dernier tour est encore "En cours"
            if d_dernier_tour.statut == "En cours":
                self.o_tour_vue.render_tour_en_cours(
                    o_tournoi_choisi.nom_tournoi,
                    d_dernier_tour.nom
                )
                return  # Stopper la fonction
        # Si le dernier tour est terminé, on incrémente son identifiant
            i_numero_tour = d_dernier_tour.identifiant + 1
        else:
            i_numero_tour = 1  # Premier tour

        # Création du tour
        o_nouveau_tour = Tour(
            p_identifiant=i_numero_tour, 
            p_nom=f"Round {i_numero_tour}",
            p_tournoi=o_tournoi_choisi
            )

        # Ajouter le tour à la liste des tours du tournoi
        o_tournoi_choisi.liste_tours.append(o_nouveau_tour)

        # Enregistrer le tour dans le tournoi
        self.o_gestionnaire_persistance.enregistrer_tour_tournoi(o_nouveau_tour, o_tournoi_choisi)
        self.o_tour_vue.render_confirmation_ajout_tour(i_numero_tour, o_tournoi_choisi)
