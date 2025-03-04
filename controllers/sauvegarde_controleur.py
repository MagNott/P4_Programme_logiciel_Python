from models.gestionnaire_persistance import GestionnairePersistance
from views.sauvegarde_vue import SauvegardeVue
from pathlib import Path


class SauvegardeControleur:
    """Contrôleur gérant les interactions entre la vue et le modèle gestionnaire persistance pour les sauvegardes."""

    def __init__(self) -> None:
        """Initialise le contrôleur de la sauvegarde avec la vue et le gestionnaire de persistance."""
        self.o_sauvegarde_vue = SauvegardeVue()
        self.o_gestionnaire_persistance = GestionnairePersistance()

#
    def sauvegarder_donnees(self):

        message, message_type = self.o_gestionnaire_persistance.effectuer_sauvegarde()
        self.o_sauvegarde_vue.afficher_message_sauvegarde(message, message_type)

#
    def charger_donnees(self):
        dossier_sauvegarde = Path(__file__).parent.parent / "sauvegarde"
        sauvegardes = []
        for dossier in dossier_sauvegarde.iterdir():
            if dossier.is_dir():
                sauvegardes.append(dossier.name)

        if not sauvegardes:
            message = "❌ Aucune sauvegarde disponible.", "error"
            message_type = "error"
            self.o_vue.afficher_message_sauvegarde(message, message_type)
            return

        choix_sauvegarde = self.o_sauvegarde_vue.demander_sauvegarde_a_restaurer(sauvegardes)

        if choix_sauvegarde is None:
            return  # L'utilisateur a annulé
        
        # Demande confirmation avant de restaurer
        confirmation = self.o_sauvegarde_vue.confirmer_restaurer_sauvegarde()

        if not confirmation:
            message = "Opération annulée. Les données n'ont pas été modifiées."
            message_type = "info"
            self.o_sauvegarde_vue.afficher_message_sauvegarde(message, message_type)
            return

        # Restaure la sauvegarde si l'utilisateur a confirmé
        message, message_type = self.o_gestionnaire_persistance.restaurer_sauvegarde(choix_sauvegarde)
        self.o_sauvegarde_vue.afficher_message_sauvegarde(message, message_type)
