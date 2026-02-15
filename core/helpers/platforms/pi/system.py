from core.helpers.base.system import BaseSystemHelper
from helper.SystemHelper import SystemHelper


class PiSystemHelper(BaseSystemHelper):
    def __init__(self):
        self.helper = SystemHelper()

    def shutdown_system(self):
        self.helper.shutdown_system()

    def restart_system(self):
        self.helper.shutdown_system()

    def stop_app(self):
        self.helper.stop_app()

    def restart_app(self):
        self.helper.stop_app()

    def change_revision(self, revision):
        self.helper.change_revision(revision)

    def cancel_revision_update(self):
        self.helper.cancel_revision_update()

    def get_cpu_temp(self):
        return self.helper.get_cpu_temp()

    def get_curr_date(self):
        return self.helper.get_curr_date()

    def get_download_rate(self):
        return self.helper.get_download_rate()

    def get_img_path(self, img_src):
        return self.helper.get_img_path(img_src)

    def is_party_mode(self):
        return self.helper.is_party_mode()

    def open_keyboard(self):
        self.helper.open_keyboard()

    def close_keyboard(self):
        self.helper.close_keyboard()

    def get_current_ssid(self):
        return self.helper.get_current_ssid()

    def get_ip_address(self):
        return self.helper.get_ip_address()

    def get_hostname(self):
        return self.helper.get_hostname()

    def get_network_config(self):
        return self.helper.get_network_config()

    def change_screen_brightness(self, brightness):
        self.helper.change_screen_brightness(brightness)

    def get_curr_brightness(self):
        return self.helper.get_curr_brightness()
