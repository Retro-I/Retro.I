import subprocess

import flet as ft

from components.dialogs.DownloadDialog import DownloadDialog
from components.dialogs.ErrorDialog import ErrorDialog
from components.dialogs.SuccessDialog import SuccessDialog
from components.Scrollbar import with_scrollbar_space
from helper.PageState import PageState
from helper.RevisionHelper import RevisionHelper
from helper.SettingsSyncHelper import SettingsSyncHelper
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
settings_sync_helper = SettingsSyncHelper()
revision_helper = RevisionHelper()


class SettingsUpdateDialog(ft.AlertDialog):
    branches_list = with_scrollbar_space(ft.ListView(visible=False, expand=True))
    tags_list = with_scrollbar_space(ft.ListView(visible=False, expand=True))

    branches_loading_spinner = ft.ProgressRing()
    tags_loading_spinner = ft.ProgressRing()

    curr_revision_span = ft.TextSpan("", style=ft.TextStyle(weight=ft.FontWeight.BOLD))

    def __init__(self):
        super().__init__()
        self.download_dialog = DownloadDialog()
        self.error_dialog = ErrorDialog()
        self.success_dialog = SuccessDialog()

        PageState.page.add(self.download_dialog)
        PageState.page.add(self.error_dialog)
        PageState.page.add(self.success_dialog)

        self.title = ft.Text(
            spans=[
                ft.TextSpan("Aktueller Stand: "),
                self.curr_revision_span,
            ]
        )
        self.content = ft.Column(
            width=500,
            tight=True,
            controls=[
                ft.Divider(),
                ft.Tabs(
                    animation_duration=300,
                    tab_alignment=ft.TabAlignment.CENTER,
                    tabs=[
                        ft.Tab(
                            text="          Branches          ",  # TODO - Workaround :D
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    self.branches_list,
                                    self.branches_loading_spinner,
                                ],
                            ),
                        ),
                        ft.Tab(
                            text="            Tags            ",  # TODO - Workaround :D
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    self.tags_list,
                                    self.tags_loading_spinner,
                                ],
                            ),
                        ),
                    ],
                    expand=True,
                ),
            ],
        )

    def open_dialog(self):
        self.open = True
        self.update()

        self.reload()

        self.fill_branches_list()
        self.fill_tags_list()
        self.curr_revision_span.text = self._get_current_revision()
        self.curr_revision_span.update()

        self.reload(show_spinner=False)

    def fill_branches_list(self):
        branches = revision_helper.get_branches()

        self.branches_list.controls.clear()
        self.branches_list.controls = self._get_items(branches)

    def fill_tags_list(self):
        tags = revision_helper.get_tags()

        self.tags_list.controls.clear()
        self.tags_list.controls = self._get_items(tags)

    def reload(self, show_spinner: bool = True):
        self.branches_loading_spinner.visible = show_spinner
        self.branches_loading_spinner.update()

        self.branches_list.visible = not show_spinner
        self.branches_list.update()

        self.tags_loading_spinner.visible = show_spinner
        self.tags_loading_spinner.update()

        self.tags_list.visible = not show_spinner
        self.tags_list.update()

    def _get_items(self, revisions: list[dict]):
        return [
            ft.TextButton(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.DONE,
                                visible=(r["name"] == self._get_current_revision()),
                            ),
                            ft.Text(
                                r["name"], size=18, overflow=ft.TextOverflow.ELLIPSIS, expand=True
                            ),
                            ft.Text(r["date"], size=16),
                        ],
                    ),
                ),
                on_click=lambda e, revision=r: self.on_revision_click(revision),
            )
            for r in revisions
        ]

    def on_revision_click(self, revision):
        self.download_dialog.open_dialog(revision)
        try:
            system_helper.change_revision(revision["name"])
            settings_sync_helper.validate_and_repair_all_settings()
            self.success_dialog.open_dialog(
                "Updates",
                f'Updates für "{revision["name"]}" erfolgreich heruntergeladen!',
                show_icon=True,
            )
        except subprocess.CalledProcessError as e:
            print("Script failed!")
            print("Exit code:", e.returncode)
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
            self.error_dialog.open_dialog(e.stderr, show_icon=True)
        self.download_dialog.close_dialog()

    def _get_current_revision(self):
        return revision_helper.get_current_revision()
