from models.gestionnaire_persistance import GestionnairePersistance
from views.sauvegarde_vue import SauvegardeVue
from pathlib import Path


class SauvegardeControleur:
    """Contrôleur gérant les interactions entre la vue et le modèle gestionnaire persistance pour les sauvegardes."""

    """Contrôleur gérant les interactions entre la vue et le modèle GestionnairePersistance pour les sauvegardes.

    Ce contrôleur permet de sauvegarder et restaurer les données en interagissant avec la vue et le gestionnaire
    de persistance. Il envoie des messages de confirmation à la vue pour affichage
    et assure la validation des actions effectuées.
    """

    def __init__(self) -> None:
        """I
        nitialise le contrôleur de la sauvegarde avec la vue et le gestionnaire de persistance.
        """

        self.o_sauvegarde_vue = SauvegardeVue()
        self.o_gestionnaire_persistance = GestionnairePersistance()

    #
    def sauvegarder_donnees(self) -> None:
        """
        Effectue une sauvegarde des données et affiche un message de confirmation.

        Cette méthode demande au gestionnaire de persistance d'effectuer une sauvegarde et récupère
        un message de confirmation ou d'erreur. Elle affiche ensuite ce message via la vue.

        Returns:
            None: Cette méthode effectue une sauvegarde et affiche un message, mais ne retourne pas de valeur.
        """

        message, message_type = self.o_gestionnaire_persistance.effectuer_sauvegarde()
        self.o_sauvegarde_vue.afficher_message(message, message_type)

    #
    def charger_donnees(self) -> None:
        """
         Affiche les sauvegardes disponibles et permet de restaurer une sauvegarde choisie par l'utilisateur.

        Cette méthode récupère la liste des sauvegardes disponibles, demande à l'utilisateur d'en choisir une via
        la vue et demande confirmation avant de la restaurer. Elle affiche ensuite un message de confirmation
        ou d'erreur.

        Returns:
            None: Cette méthode effectue une restauration et affiche un message, mais ne retourne pas de valeur.
        """

        dossier_sauvegarde = Path(__file__).parent.parent / "sauvegarde"
        sauvegardes = []
        for dossier in dossier_sauvegarde.iterdir():
            if dossier.is_dir():
                sauvegardes.append(dossier.name)

        if not sauvegardes:
            message = "❌ Aucune sauvegarde disponible."
            message_type = "error"
            self.o_sauvegarde_vue.afficher_message(message, message_type)
            return

        choix_sauvegarde = self.o_sauvegarde_vue.demander_sauvegarde_a_restaurer(
            sauvegardes
        )

        if choix_sauvegarde is None:
            return  # L'utilisateur a annulé

        # Demande confirmation avant de restaurer
        confirmation = self.o_sauvegarde_vue.confirmer_restaurer_sauvegarde()

        if not confirmation:
            message = "Opération annulée. Les données n'ont pas été modifiées."
            message_type = "info"
            self.o_sauvegarde_vue.afficher_message(message, message_type)
            return

        # Restaure la sauvegarde si l'utilisateur a confirmé
        message, message_type = self.o_gestionnaire_persistance.restaurer_sauvegarde(
            choix_sauvegarde
        )
        self.o_sauvegarde_vue.afficher_message(message, message_type)
