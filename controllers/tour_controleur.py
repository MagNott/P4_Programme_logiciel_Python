from models.tour import Tour
from views.tour_vue import TourVue
from models.gestionnaire_persistance import GestionnairePersistance
from models.match import Match
import random
from models.tournoi import Tournoi
from itertools import combinations, cycle


class TourControleur:
    """
    Contrôleur gérant les interactions entre la vue et le modèle pour les tours.

    Ce contrôleur est responsable :
    - De la génération des tours et des matchs associés.
    - De l'organisation des appariements entre joueurs pour les matchs.
    - De la gestion de l'affichage des informations des tours via la `TourVue`.
    """

    def __init__(self) -> None:
        """
        Initialise le contrôleur des tours.

        Instancie la vue `TourVue` et le gestionnaire de persistance `GestionnairePersistance`
        pour gérer l'affichage et la sauvegarde des tours et matchs.
        """

        self.o_tour_vue = TourVue()
        self.o_gestionnaire_persistance = GestionnairePersistance()

    #
    def creer_tour(self) -> None:
        """
        Crée un tour pour un tournoi sélectionné et génère les matchs.

        Cette méthode commence par vérifier si le tournoi peut encore accueillir un tour et s’il dispose de joueurs
        inscrits. Elle s’assure ensuite qu’aucun tour précédent n’est encore en cours. Une fois ces vérifications
        effectuées, elle crée un nouvel objet Tour, génère les matchs en fonction du tour (premier tour ou suivants),
        puis l'ajoute à la liste des tours du tournoi. Enfin, elle sauvegarde le tour dans la base de données et
        affiche un message de confirmation pour informer l’utilisateur.

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

        if i_numero_tour == 1:
            o_tour = self._generer_premier_tour(o_nouveau_tour, o_tournoi_choisi)
        else:
            o_tour = self._generer_tours_suivants(o_nouveau_tour, o_tournoi_choisi)

        # Ajoute le tour à la liste des tours du tournoi
        o_tournoi_choisi.liste_tours.append(o_tour)

        # Enregistre le tour dans le tournoi
        self.o_gestionnaire_persistance.enregistrer_tour_tournoi(
            o_tour, o_tournoi_choisi
        )
        self.o_tour_vue.render_confirmation_ajout_tour(i_numero_tour, o_tournoi_choisi)

    #
    def terminer_tour(self) -> None:
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

        o_tournoi = self.o_gestionnaire_persistance.recuperer_objet_tournoi(
            i_identifiant_tournoi
        )

        # Récupère l'objet Tournoi et le dernier tour en cours.
        d_dernier_tour = self.o_gestionnaire_persistance.recuperer_dernier_tour(
            i_identifiant_tournoi
        )

        # Récupère les matchs du tour et remplace les identifiants des joueurs par leurs noms
        # pour l'affichage en console.
        l_objets_matchs = self.o_gestionnaire_persistance.recuperer_liste_objets_matchs(
            d_dernier_tour
        )

        # Affiche les matchs et demande à l'utilisateur de saisir les résultats.
        l_resultats = self.o_tour_vue.render_matchs_pour_saisie(
            o_tournoi, d_dernier_tour, l_objets_matchs
        )

        # Met à jour et enregistre les résultats des matchs dans le JSON.
        self.o_gestionnaire_persistance.enregistrer_resultat_match(
            l_resultats, i_identifiant_tournoi
        )

    #
    # METHODES PRIVEES
    #
    def _gerer_match_tour(
        self,
        p_objet_tournoi: Tournoi,
        p_objet_tour: Tour,
        p_identifiant_match: int,
        p_identifiant_joueur1: int,
        p_identifiant_joueur2: int,
    ) -> int:
        """
        Génère un match entre deux joueurs pour un tour donné.

        Cette méthode :
        - Crée un objet `Match` entre les deux joueurs.
        - L'affiche dans la console via `TourVue`.
        - Ajoute le match à la liste des matchs du tour.

        Args:
            p_objet_tournoi (Tournoi): Objet tournoi contenant les informations du tournoi.
            p_objet_tour (Tour): Objet tour auquel ajouter le match.
            p_identifiant_match (int): Identifiant unique du match.
            p_identifiant_joueur1 (int): Identifiant du premier joueur.
            p_identifiant_joueur2 (int): Identifiant du deuxième joueur.

        Returns:
            int: Le nouvel identifiant du prochain match.
        """

        o_nouveau_match = Match(
            p_identifiant_match,
            self.o_gestionnaire_persistance.recuperer_objet_joueur(
                p_identifiant_joueur1
            ),
            self.o_gestionnaire_persistance.recuperer_objet_joueur(
                p_identifiant_joueur2
            ),
        )
        p_identifiant_match += 1

        self.o_tour_vue.render_visualiser_matchs(
            p_objet_tournoi.nom_tournoi,
            p_objet_tour.identifiant,
            p_identifiant_match - 1,
            self.o_gestionnaire_persistance.recuperer_objet_joueur(
                p_identifiant_joueur1
            ),
            self.o_gestionnaire_persistance.recuperer_objet_joueur(
                p_identifiant_joueur2
            ),
        )

        # Enregistre le tour et ses matchs dans la base de données.
        p_objet_tour.liste_matchs.append(o_nouveau_match)

        return p_identifiant_match

    #
    def _generer_premier_tour(self, p_objet_tour, p_tournoi_choisi):
        """
        Génère aléatoirement les matchs du premier tour d'un tournoi.

        Cette méthode :
        - Mélange la liste des joueurs du tournoi.
        - Associe les joueurs par paires pour créer des matchs.
        - Affiche les matchs générés.
        - Ajoute les matchs au tour.

        Args:
            p_objet_tour (Tour): Objet tour où enregistrer les matchs.
            p_tournoi_choisi (Tournoi): Objet tournoi concerné.

        Returns:
            Tour: Le tour mis à jour avec les matchs générés.
        """

        # Mélange les joueurs du tournoi et forme des paires pour les matchs.
        l_objets_joueurs = p_tournoi_choisi.liste_joueurs.copy()
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

            self.o_tour_vue.render_visualiser_matchs(
                p_tournoi_choisi.nom_tournoi,
                1,
                identifiant_match - 1,
                o_joueur_blanc,
                o_joueur_noir,
            )

            # Enregistre le tour et ses matchs dans la base de données
            p_objet_tour.liste_matchs.append(o_nouveau_match)

        return p_objet_tour

    #
    def _generer_tours_suivants(
        self, p_objet_tour: Tour, p_objet_tournoi_choisi: Tournoi
    ) -> Tour:
        """
        Génère les tours suivants en fonction des scores et des matchs déjà joués.

        Cette méthode :
        - Trie les joueurs en fonction de leurs scores.
        - Génère des appariements en évitant que les mêmes joueurs ne s'affrontent plusieurs fois.
        - Ajoute les nouveaux matchs au tour et les affiche.

        Args:
            p_objet_tour (Tour): Objet tour où enregistrer les nouveaux matchs.
            p_objet_tournoi_choisi (Tournoi): Tournoi en cours.

        Returns:
            Tour: Le tour mis à jour avec les matchs générés.
        """

        d_scores_joueurs = self.o_gestionnaire_persistance.recuepere_score_joueurs(
            p_objet_tournoi_choisi.identifiant
        )

        d_joueurs_tries = dict(
            sorted(d_scores_joueurs.items(), key=lambda item: item[1], reverse=True)
        )

        l_joueur_tries = list(d_joueurs_tries.keys())
        circular_list = cycle(l_joueur_tries)  # Crée une liste infinie

        paires_possibles = list(combinations(d_joueurs_tries.keys(), 2))
        paires_possible_sets = []
        for paire in paires_possibles:
            paires_possible_sets.append(frozenset(paire))

        l_match_joues = []
        for o_tour in p_objet_tournoi_choisi.liste_tours:
            for o_match in o_tour.liste_matchs:
                i_joueur_blanc = o_match.joueur_blanc.identifiant_tinydb
                i_joueur_noir = o_match.joueur_noir.identifiant_tinydb

                l_match_joues.append(frozenset([i_joueur_blanc, i_joueur_noir]))
                if frozenset([i_joueur_blanc, i_joueur_noir]) in paires_possible_sets:
                    paires_possible_sets.remove(
                        frozenset([i_joueur_blanc, i_joueur_noir])
                    )

        compteur = 0
        l_paires = []
        identifiant_match = 1

        while len(paires_possible_sets) >= 1 and len(l_joueur_tries) > 0:
            i_joueur1 = next(circular_list)
            i_joueur2 = next(circular_list)  # Par défaut, on prend le joueur suivant

            if len(l_joueur_tries) < compteur:
                compteur = 0
            else:
                compteur += 1

            set_paire_courante = frozenset([i_joueur1, i_joueur2])

            if (
                set_paire_courante in paires_possible_sets
            ):  # Vérifie si la paire n'a jamais été jouée
                l_paires.append([i_joueur1, i_joueur2])  # Ajoute la paire
                paires_possible_sets.remove(
                    set_paire_courante
                )  # Enregistre la paire pour éviter les doublons
                l_joueur_tries.remove(i_joueur1)
                l_joueur_tries.remove(i_joueur2)

                identifiant_match = self._gerer_match_tour(
                    p_objet_tournoi_choisi,
                    p_objet_tour,
                    identifiant_match,
                    i_joueur1,
                    i_joueur2,
                )

            else:
                # Si on ne trouve pas de paire, on évite la boucle infinie
                compteur += 1
                if compteur >= len(l_joueur_tries):
                    break  # Condition de sortie

        # On utilise une copie pour ne pas modifier la liste en cours d'itération
        joueurs_a_tester = l_joueur_tries[:]

        # On parcourt les joueurs restants pour former des paires valides
        for i in range(len(l_joueur_tries) - 1):
            for j in range(i + 1, len(l_joueur_tries)):  # Toujours après `i`
                i_joueur1 = joueurs_a_tester[i]
                i_joueur2 = joueurs_a_tester[j]

                set_paire_courante = frozenset([i_joueur1, i_joueur2])

                # Vérifie si cette paire peut être jouée
                if (
                    set_paire_courante in paires_possible_sets
                    and i_joueur1 in l_joueur_tries
                    and i_joueur2 in l_joueur_tries
                ):
                    # Ajoute la paire et la retire des sets disponibles
                    l_paires.append([i_joueur1, i_joueur2])
                    paires_possible_sets.remove(set_paire_courante)

                    # Supprime les joueurs appariés pour éviter de les réutiliser
                    l_joueur_tries.remove(i_joueur1)
                    l_joueur_tries.remove(i_joueur2)

                    identifiant_match = self._gerer_match_tour(
                        p_objet_tournoi_choisi,
                        p_objet_tour,
                        identifiant_match,
                        i_joueur1,
                        i_joueur2,
                    )

        random.shuffle(l_joueur_tries)  # Mélange aléatoire

        # Créer les paires de joueurs et générer les matchs
        while len(l_joueur_tries) >= 2:
            i_joueur1 = l_joueur_tries.pop()
            i_joueur2 = l_joueur_tries.pop()

            identifiant_match = self._gerer_match_tour(
                p_objet_tournoi_choisi,
                p_objet_tour,
                identifiant_match,
                i_joueur1,
                i_joueur2,
            )

        return p_objet_tour
