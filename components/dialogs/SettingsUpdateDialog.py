import subprocess
from enum import Enum

import flet as ft

from components.dialogs.DownloadDialog import DownloadDialog
from components.dialogs.ErrorDialog import ErrorDialog
from helper.RevisionHelper import RevisionHelper
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
revision_helper = RevisionHelper()


class RevisionType(Enum):
    BRANCH = "BRANCH"
    TAG = "TAG"


class SettingsUpdateDialog(ft.AlertDialog):
    branches_list = ft.ListView()
    tags_list = ft.ListView()

    def __init__(self):
        super().__init__()
        self.download_dialog = DownloadDialog()
        self.error_dialog = ErrorDialog()
        self.title = ft.Text(
            spans=[
                ft.TextSpan("Aktueller Stand: "),
                ft.TextSpan(self.get_current_revision(), style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
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
        self.open = True
        self.update()

    def fill_branches_list(self):
        branches = revision_helper.get_branches()

        self.branches_list.controls.clear()
        self.branches_list.controls = self._get_items(branches, RevisionType.BRANCH)
        self.branches_list.update()

    def fill_tags_list(self):
        tags = revision_helper.get_tags()

        self.tags_list.controls.clear()
        self.tags_list.controls = self._get_items(tags, RevisionType.TAG)
        self.tags_list.update()

    def _get_items(self, revisions: list[str], revision_type: RevisionType):
        return [
            ft.TextButton(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.DONE, visible=(r == self.get_current_revision())),
                            ft.Text(r, size=18),
                        ],
                    ),
                ),
                on_click=lambda e, revision=r: self.on_revision_click(revision, revision_type),
            )
            for r in revisions
        ]

    def on_revision_click(self, revision, revision_type):
        self.download_dialog.open_dialog(revision)
        try:
            result = subprocess.run(
                ["bash", "./scripts/update_project.sh", revision],
                capture_output=True,
                text=True,
                check=True,  # raises CalledProcessError if script exits non-zero
            )
            print("✅ Script output:\n", result.stdout)
            self.download_dialog.close_dialog()
        except subprocess.CalledProcessError as e:
            print("Script failed!")
            print("Exit code:", e.returncode)
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
            self.download_dialog.close_dialog()
            self.error_dialog.open_dialog(e.stdout)

    def get_current_revision(self):
        return revision_helper.get_current_revision()
