from core.helpers.base.system import BaseSystemHelper


class WebSystemHelper(BaseSystemHelper):
    def shutdown_system(self):
        pass

    def restart_system(self):
        pass

    def stop_app(self):
        pass

    def restart_app(self):
        pass

    def change_revision(self, revision):
        pass

    def cancel_revision_update(self):
        pass

    def get_cpu_temp(self):
        return 0.0

    def get_curr_date(self):
        pass

    def get_download_rate(self):
        return 0.0

    def get_img_path(self, img_src):
        return img_src

    def is_party_mode(self):
        return False

    def open_keyboard(self):
        pass

    def close_keyboard(self):
        pass

    def get_current_ssid(self):
        pass

    def get_ip_address(self):
        return "127.0.0.1"

    def get_hostname(self):
        return ""

    def get_network_config(self):
        return {}

    def change_screen_brightness(self, value):
        pass

    def get_curr_brightness(self):
        return 100
