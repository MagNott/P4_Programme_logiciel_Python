from views.vue import Vue
import questionary


class SauvegardeVue(Vue):
    """
    Gère l'affichage et les interactions liées aux sauvegardes.

    Cette classe permet d'afficher des messages de sauvegarde/restauration,
    de demander à l'utilisateur de choisir une sauvegarde, et de confirmer la restauration.

    Hérite de:
        Vue: Classe parente fournissant les fonctionnalités d'affichage via la bibliothèque Rich.
    """

#
    def afficher_message_sauvegarde(self, p_message: str, p_message_type: str) -> None:
        """
        Affiche un message coloré en fonction du type de message.

        Args:
            p_message (str): Le message à afficher.
            p_message_type (str): Type du message ("success", "error", "info").
                                - "success" (vert) : Succès.
                                - "error" (rouge) : Erreur.
                                - "info" (cyan) : Information.

        Returns:
            None: Affiche le message formaté dans la console.
        """

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
    def demander_sauvegarde_a_restaurer(self, p_sauvegardes: list[str]) -> str | None:
        """
        Demande à l'utilisateur de choisir une sauvegarde à restaurer.

        Args:
            p_sauvegardes (list[str]): Liste des sauvegardes disponibles.

        Returns:
            str | None: Le nom de la sauvegarde choisie par l'utilisateur,
                        ou `None` si aucune sauvegarde n'est disponible.
        """
        if not p_sauvegardes:
            return None  # Aucune sauvegarde disponible

        return questionary.select(
            "Choisissez une sauvegarde à restaurer :", choices=p_sauvegardes
        ).ask()

#
    def confirmer_restaurer_sauvegarde(self) -> bool:
        """
        Affiche un avertissement et demande confirmation avant de restaurer une sauvegarde.

        Returns:
            bool: `True` si l'utilisateur confirme la restauration,
                `False` s'il annule l'action.
        """

        self.console.print("\n[bold orange3]⚠️  Attention : Restaurer cette sauvegarde "
                           "remplacera les données actuelles ![/bold orange3]")
        self.console.print("[bold orange3]Cette action est **IRRÉVERSIBLE**. Voulez-vous continuer ?[/bold orange3]\n")

        # Demande de confirmation avec questionary
        return questionary.confirm("Confirmez-vous la restauration ?").ask()
