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
        """
        Crée un tour pour un tournoi sélectionné et génère les matchs.

        Cette fonction permet à l'utilisateur de créer un nouveau tour pour un tournoi existant.
        Elle s'assure que le tournoi n'a pas atteint son nombre maximal de tours, génère aléatoirement
        des paires de joueurs, et enregistre le tour dans la base de données.

        Args:
            None

        Returns:
            None: Cette fonction enregistre un tour et affiche des informations, 
                mais ne retourne pas de valeur.
        """

        # Liste les tournois existants et demande à l'utilisateur d'en choisir un.
        l_liste_tournois = self.o_gestionnaire_persistance.recuperer_fichiers_tournois()
        i_identifiant_tournoi = self.o_tour_vue.render_choix_tournoi(l_liste_tournois)

        # Récupère l'objet Tournoi
        o_tournoi_choisi = self.o_gestionnaire_persistance.recuperer_objet_tournoi(
            i_identifiant_tournoi
        )

        # Vérifie que le tournoi peut accueillir un nouveau tour.
        if len(o_tournoi_choisi.liste_tours) >= int(o_tournoi_choisi.nombre_tours):
            self.o_tour_vue.render_verification(
                "Ce tournoi a atteint son nombre maximal de tours."
            )
            return

        if len(o_tournoi_choisi.liste_joueurs) == 0:
            self.o_tour_vue.render_verification(
                "Ce tournoi n'a pas encore de joueurs, veuillez inscrire des joueurs avant."
            )
            return

        # Vérifie si des tours existent déjà et si le dernier est en cours ou terminé
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
        # Mélange les joueurs du tournoi et forme des paires pour les matchs.
        l_objets_joueurs = (o_tournoi_choisi.liste_joueurs.copy())
        # On utilise copy() sinon on passe par référence et on modifie la liste du tournoi
        random.shuffle(l_objets_joueurs)  # Mélange aléatoire

        identifiant_match = 1
        # Créer les paires de joueurs et générer les matchs
        while len(l_objets_joueurs) >= 2:
            o_joueur_blanc = l_objets_joueurs.pop()
            o_joueur_noir = l_objets_joueurs.pop()

            o_nouveau_match = Match(
                identifiant_match,
                o_joueur_blanc,
                o_joueur_noir,
            )
            identifiant_match += 1

            # # Associe chaque joueur à son nom complet pour l'affichage.
            # o_joueur_blanc = self.o_gestionnaire_persistance.recuperer_objet_joueur(
            #     p_joueur_blanc
            # )
            # o_joueur_blanc_nom = f"{o_joueur_blanc.nom_famille} {o_joueur_blanc.prenom}"

            # o_joueur_noir = self.o_gestionnaire_persistance.recuperer_objet_joueur(
            #     p_joueur_noir
            # )
            # o_joueur_noir_nom = f"{o_joueur_noir.nom_famille} {o_joueur_noir.prenom}"

            # Affiche les matchs du tour à l'utilisateur via la console.
            self.o_tour_vue.render_visualiser_matchs(
                o_tournoi_choisi.nom_tournoi,
                i_numero_tour,
                identifiant_match - 1,
                o_joueur_blanc,
                o_joueur_noir,
            )

            # Enregistre le tour et ses matchs dans la base de données.
            o_nouveau_tour.liste_matchs.append(o_nouveau_match)

        # Ajoute le tour à la liste des tours du tournoi
        o_tournoi_choisi.liste_tours.append(o_nouveau_tour)

        # Enregistre le tour dans le tournoi
        self.o_gestionnaire_persistance.enregistrer_tour_tournoi(
            o_nouveau_tour, o_tournoi_choisi
        )
        self.o_tour_vue.render_confirmation_ajout_tour(i_numero_tour, o_tournoi_choisi)

    #
    def terminer_tour(self):
        """
        Termine le tour en cours d'un tournoi et enregistre les résultats des matchs.

        Cette fonction permet à l'utilisateur de saisir les résultats des matchs d'un tour en cours.
        Elle met à jour les informations des matchs en remplaçant les identifiants des joueurs par leurs noms
        pour l'affichage en console et enregistre les résultats dans la base de données.

        Args:
            None

        Returns:
            None: Cette fonction effectue des mises à jour dans les fichiers JSON et affiche des informations,
                mais ne retourne aucune valeur.
        """

        # Liste les tournois disponibles et demande à l'utilisateur de choisir un tournoi.
        l_liste_tournois = self.o_gestionnaire_persistance.recuperer_fichiers_tournois()
        i_identifiant_tournoi = self.o_tour_vue.render_choix_tournoi(l_liste_tournois)

        o_tournoi = self.o_gestionnaire_persistance.recuperer_objet_tournoi(i_identifiant_tournoi)

        # Récupère l'objet Tournoi et le dernier tour en cours.
        d_dernier_tour = self.o_gestionnaire_persistance.recuperer_dernier_tour(
                i_identifiant_tournoi
            )

        # Récupère les matchs du tour et remplace les identifiants des joueurs par leurs noms
        # pour l'affichage en console.
        l_objets_matchs = (
            self.o_gestionnaire_persistance.recuperer_liste_objets_matchs(d_dernier_tour)
        )

        # for match in l_objets_matchs:
            # match.joueur_blanc = f"{match.joueur_blanc.prenom} {match.joueur_blanc.nom_famille}"
            # match.joueur_noir = f"{match.joueur_noir.prenom} {match.joueur_noir.nom_famille}"

        # Affiche les matchs et demande à l'utilisateur de saisir les résultats.
        l_resultats = self.o_tour_vue.render_matchs_pour_saisie(o_tournoi, d_dernier_tour, l_objets_matchs)

        # Met à jour et enregistre les résultats des matchs dans le JSON.
        self.o_gestionnaire_persistance.enregistrer_resultat_match(
            l_resultats, i_identifiant_tournoi
        )
