from views.vue import Vue
import questionary


class SauvegardeVue(Vue):
    """Gère l'affichage des informations liées aux tournois avec la bibliothèque Rich."""

#
    def afficher_message_sauvegarde(self, p_message, p_message_type):

        p_message = f"\n{p_message}\n"

        if p_message_type == "success":
            self.console.print(p_message, style="bold green")
        elif p_message_type == "error":
            self.console.print(p_message, style="bold red")
        elif p_message_type == "info":
            self.console.print(p_message, style="bold cyan")
        else:
            self.console.print(p_message)

#
    def demander_sauvegarde_a_restaurer(self, p_sauvegardes):
        if not p_sauvegardes:
            return None  # Aucune sauvegarde disponible

        return questionary.select(
            "Choisissez une sauvegarde à restaurer :", choices=p_sauvegardes
        ).ask()

#
    def confirmer_restaurer_sauvegarde(self):

        self.console.print("\n[bold orange3]⚠️  Attention : Restaurer cette sauvegarde remplacera les données actuelles ![/bold orange3]")
        self.console.print("[bold orange3]Cette action est **IRRÉVERSIBLE**. Voulez-vous continuer ?[/bold orange3]\n")

        # ✅ Demande de confirmation avec questionary
        return questionary.confirm("Confirmez-vous la restauration ?").ask()
