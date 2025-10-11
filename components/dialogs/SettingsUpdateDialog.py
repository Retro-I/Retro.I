import subprocess
from enum import Enum

import flet as ft

from components.dialogs.DownloadDialog import DownloadDialog
from components.dialogs.ErrorDialog import ErrorDialog
from components.dialogs.SettingsShutdownDialog import SettingsShutdownDialog
from helper.PageState import PageState
from helper.RevisionHelper import RevisionHelper
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
revision_helper = RevisionHelper()


class SettingsUpdateDialog(ft.AlertDialog):
    branches_list = ft.ListView()
    tags_list = ft.ListView()

    curr_revision_span = ft.TextSpan("", style=ft.TextStyle(weight=ft.FontWeight.BOLD))

    def __init__(self):
        super().__init__()
        self.download_dialog = DownloadDialog()
        self.error_dialog = ErrorDialog()
        self.settings_shutdown_dialog = SettingsShutdownDialog()

        PageState.page.add(self.download_dialog)
        PageState.page.add(self.error_dialog)
        PageState.page.add(self.settings_shutdown_dialog)

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
                            content=self.branches_list,
                        ),
                        ft.Tab(
                            text="            Tags            ",  # TODO - Workaround :D
                            content=self.tags_list,
                        ),
                    ],
                    expand=True,
                ),
            ],
        )

    def open_dialog(self):
        self.fill_branches_list()
        self.fill_tags_list()
        self.curr_revision_span.text = self._get_current_revision()
        self.curr_revision_span.update()
        self.open = True
        self.update()

    def fill_branches_list(self):
        branches = revision_helper.get_branches()

        self.branches_list.controls.clear()
        self.branches_list.controls = self._get_items(branches)
        self.branches_list.update()

    def fill_tags_list(self):
        tags = revision_helper.get_tags()

        self.tags_list.controls.clear()
        self.tags_list.controls = self._get_items(tags)
        self.tags_list.update()

    def _get_items(self, revisions: list[str]):
        return [
            ft.TextButton(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.DONE, visible=(r == self._get_current_revision())),
                            ft.Text(r, size=18),
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
            subprocess.run(
                ["bash", "scripts/update_project.sh", revision],
                capture_output=True,
                text=True,
                check=True,
            )
            self.settings_shutdown_dialog.open_dialog()
        except subprocess.CalledProcessError as e:
            print("Script failed!")
            print("Exit code:", e.returncode)
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
            self.error_dialog.open_dialog(e.stderr)
        self.download_dialog.close_dialog()

    def _get_current_revision(self):
        return revision_helper.get_current_revision()
