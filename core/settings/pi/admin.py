from core.settings.base.admin import BaseAdminSettings
from helper.admin_helper import AdminHelper


class PiAdminSettings(BaseAdminSettings):
    def __init__(self):
        self.settings = AdminHelper()

    def get_admin_password(self) -> str:
        pass

    def validate_admin_password(self, input_var) -> bool:
        pass
