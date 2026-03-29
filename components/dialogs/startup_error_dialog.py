import flet as ft

from core.factories.settings_factories import create_startup_error_settings


class StartupErrorDialog(ft.AlertDialog):
    text = ft.Text("")

    def __init__(self):
        super().__init__()

        self.startup_error_settings = create_startup_error_settings()

        self.title = ft.Text("Fehler beim Herunterladen des letzten Updates")
        self.content = self.text
        self.modal = True
        self.actions = [
            ft.FilledButton("Ok", on_click=lambda e: self.close_dialog())
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    def open_dialog(self):
        err = self.startup_error_settings.startup_error()
        self.text.value = err if err is not None else "Unbekannter Fehler"
        self.text.update()
        self.open = True
        self.update()

        self.startup_error_settings.reset_startup_error()

    def close_dialog(self):
        self.open = False
        self.update()
