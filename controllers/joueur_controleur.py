from models import Joueur
from views import JoueurVue
from tinydb import TinyDB, Query

import questionary


class JoueurControleur:
    def __init__(self):
        self.o_joueur_vue = JoueurVue()
        self.db = TinyDB('db.json')

    def ajouter_joueur(self):
        # Poser les questions pour obtenir les informations du joueur
        s_nom = questionary.text("Entrez le nom du joueur :").ask()
        s_prenom = questionary.text("Entrez le prenom du joueur :").ask()

        o_joueur_modele = Joueur(s_nom, s_prenom)
        # Joueur.liste_joueur.append(o_joueur_modele)
        self.db.insert({'nom_famille': o_joueur_modele.nom_famille, 'prenom': o_joueur_modele.prenom})

        JoueurVue.render_confirm_ajout_joueur(s_nom, s_prenom)

    def lister_joueurs(self):
        # JoueurVue.render_lister_joueur(Joueur.liste_joueur)
        joueurs_documents = self.db.all()

        # Convertir chaque document en une instance de Joueur
        joueurs = [
            Joueur(
                p_nom_famille=doc["nom_famille"],
                p_prenom=doc["prenom"]
            ) for doc in joueurs_documents
        ]

        self.o_joueur_vue.render_lister_joueur(joueurs)
