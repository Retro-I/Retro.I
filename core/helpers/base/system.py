class BaseSystemHelper:
    def shutdown_system(self):
        raise NotImplementedError

    def restart_system(self):
        raise NotImplementedError

    def stop_app(self):
        raise NotImplementedError

    def restart_app(self):
        raise NotImplementedError

    def change_revision(self, revision):
        raise NotImplementedError

    def cancel_revision_update(self):
        raise NotImplementedError

    def get_cpu_temp(self):
        raise NotImplementedError

    def get_curr_date(self):
        raise NotImplementedError

    def get_download_rate(self):
        raise NotImplementedError

    def get_img_path(self, img_src):
        raise NotImplementedError

    def is_party_mode(self):
        raise NotImplementedError

    def open_keyboard(self):
        raise NotImplementedError

    def close_keyboard(self):
        raise NotImplementedError

    def get_current_ssid(self):
        raise NotImplementedError

    def get_ip_address(self):
        raise NotImplementedError

    def get_hostname(self):
        raise NotImplementedError

    def get_network_config(self):
        raise NotImplementedError

    def change_screen_brightness(self, value):
        raise NotImplementedError

    def get_curr_brightness(self):
        raise NotImplementedError
