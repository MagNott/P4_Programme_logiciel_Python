from models.tour import Tour
from views.tour_vue import TourVue
from models.gestionnaire_persistance import GestionnairePersistance
from models.match import Match
import random


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
        o_tournoi_choisi = self.o_gestionnaire_persistance.recuperer_objet_tournoi(
            i_identifiant_tournoi
        )

        # Vérifier s'il y a de la place pour un nouveau tour
        if len(o_tournoi_choisi.liste_tours) >= int(o_tournoi_choisi.nombre_tours):
            self.o_tour_vue.render_verification_tour_max(
                "Ce tournoi a atteint son nombre maximal de tours."
            )
            return

            # Vérifier si des tours existent déjà et si le dernier est en cours ou terminé
        if o_tournoi_choisi.liste_tours:
            d_dernier_tour = o_tournoi_choisi.liste_tours[-1]
            # Vérifier si le dernier tour est encore "En cours"
            if d_dernier_tour.statut == "En cours":
                self.o_tour_vue.render_tour_en_cours(
                    o_tournoi_choisi.nom_tournoi, d_dernier_tour.nom
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
            p_tournoi=o_tournoi_choisi,
        )

        # Récupérer les joueurs du tournoi et les mélanger
        l_joueurs = (
            o_tournoi_choisi.liste_joueurs.copy()
        )  # copy() sinon on passe par référence et on modifie la liste du tournoi
        random.shuffle(l_joueurs)  # Mélange aléatoire

        identifiant_match = 1
        # Créer les paires de joueurs et générer les matchs
        while len(l_joueurs) >= 2:
            p_joueur_blanc = l_joueurs.pop()
            p_joueur_noir = l_joueurs.pop()

            o_nouveau_match = Match(
                identifiant_match,
                p_joueur_blanc,
                p_joueur_noir,
            )
            identifiant_match += 1

            o_joueur_blanc = self.o_gestionnaire_persistance.recuperer_objet_joueur(
                p_joueur_blanc
            )
            o_joueur_blanc_nom = f"{o_joueur_blanc.nom_famille} {o_joueur_blanc.prenom}"

            o_joueur_noir = self.o_gestionnaire_persistance.recuperer_objet_joueur(
                p_joueur_noir
            )
            o_joueur_noir_nom = f"{o_joueur_noir.nom_famille} {o_joueur_noir.prenom}"

            # l_objets_match = self.o_gestionnaire_persistance.recuperer_liste_objets_matchs(i_identifiant_tournoi)
            self.o_tour_vue.render_visualiser_matchs(
                i_identifiant_tournoi,
                i_numero_tour,
                identifiant_match - 1,
                o_joueur_blanc_nom,
                o_joueur_noir_nom,
            )

            o_nouveau_tour.liste_matchs.append(o_nouveau_match)

        # Ajouter le tour à la liste des tours du tournoi
        o_tournoi_choisi.liste_tours.append(o_nouveau_tour)

        # Enregistrer le tour dans le tournoi
        self.o_gestionnaire_persistance.enregistrer_tour_tournoi(
            o_nouveau_tour, o_tournoi_choisi
        )
        self.o_tour_vue.render_confirmation_ajout_tour(i_numero_tour, o_tournoi_choisi)

    #
    def terminer_tour(self):

        # Lister les tournois existants
        l_liste_tournois = self.o_gestionnaire_persistance.lister_tournois()
        i_identifiant_tournoi = self.o_tour_vue.render_choix_tournoi(l_liste_tournois)

        o_tournoi = self.o_gestionnaire_persistance.recuperer_objet_tournoi(i_identifiant_tournoi)

        d_dernier_tour = self.o_gestionnaire_persistance.recuperer_dernier_tour(
                i_identifiant_tournoi
            )

        l_objets_matchs = (
            self.o_gestionnaire_persistance.recuperer_liste_objets_matchs(d_dernier_tour)
        )

        for match in l_objets_matchs:
            o_joueur_blanc = self.o_gestionnaire_persistance.recuperer_objet_joueur(match.joueur_blanc)
            o_joueur_noir = self.o_gestionnaire_persistance.recuperer_objet_joueur(match.joueur_noir)

            match.joueur_blanc = f"{o_joueur_blanc.prenom} {o_joueur_blanc.nom_famille}"
            match.joueur_noir = f"{o_joueur_noir.prenom} {o_joueur_noir.nom_famille}"

        l_resultats = self.o_tour_vue.render_matchs_pour_saisie(o_tournoi, d_dernier_tour, l_objets_matchs)

        self.o_gestionnaire_persistance.enregistrer_resultat_match(
            l_resultats, i_identifiant_tournoi
        )
