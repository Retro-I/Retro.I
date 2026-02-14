import flet as ft

from components.VolumeInputField import VolumeInputField
from components.VolumeStepInputField import VolumeStepInputField
from core.factories.audio_factory import create_audio_state
from helper.Audio import Audio
from helper.Stations import Stations

stations_helper = Stations()


class SettingsAudioDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.audio_state = create_audio_state()

        self.audio_dropdown = ft.Dropdown(
            editable=True,
            label="Ausgabegeräte",
            options=self.get_audio_output_options(),
            on_change=self.on_audio_output_change,
            value=self.get_default_option(),
            expand=True,
        )

        self.title = ft.Text("Audio")
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                self.audio_dropdown,
                ft.Divider(),
                VolumeInputField(),
                ft.Divider(),
                VolumeStepInputField(),
                ft.Divider(),
                ft.Switch(
                    "Lieblingsradiosender nach Systemstart abspielen",
                    label_style=ft.TextStyle(size=18),
                    on_change=lambda e: self.toggle_enable_autoplay(),
                    value=self.audio_state.is_default_station_autoplay_enabled(),
                ),
            ],
        )

    def toggle_enable_autoplay(self):
        self.audio_state.toggle_default_station_autoplay()

    def get_audio_output_options(self):
        sinks = self.audio_state.get_audio_sinks()
        return [
            ft.DropdownOption(
                key=sink["id"],
                text=f'{sink["id"]} - {sink["name"]}',
            )
            for sink in sinks
        ]

    def get_default_option(self):
        sink = self.audio_state.get_current_audio_sink()
        return sink["id"] if sink is not None else None

    def on_audio_output_change(self, e):
        sink_id = e.control.value
        self.audio_state.set_audio_output(sink_id)

    def open_dialog(self):
        self.open = True
        self.audio_dropdown.value = self.get_default_option()
        self.audio_dropdown.update()
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
