import base64
import json

from core.helper_factories import create_settings_sync_helper
from core.settings.base.admin import BaseAdminSettings
from helper.constants import Constants


class AdminHelper(BaseAdminSettings):
    SETTING = "admin-password.json"
    SETTINGS_PATH = f"{Constants.settings_path()}/{SETTING}"

    def __init__(self):
        self.settings_sync_helper = create_settings_sync_helper()

    def get_admin_password(self) -> str:
        settings = self.get_settings()
        decoded_bytes = base64.b64decode(settings["adminPassword"])
        return decoded_bytes.decode("utf-8")

    def validate_admin_password(self, input_val: str) -> bool:
        return input_val == self.get_admin_password()

    def get_settings(self):
        def _get_data():
            with open(self.SETTINGS_PATH) as file:
                data = json.load(file)
                return data

        try:
            return _get_data()
        except Exception:
            self.settings_sync_helper.reset_settings_file(self.SETTING)
            return _get_data()
