class BaseStartupErrorSettings:
    def get_settings(self):
        raise NotImplementedError

    def is_startup_error(self):
        raise NotImplementedError

    def startup_error(self) -> str:
        raise NotImplementedError

    def write_startup_error(self, message: str = ""):
        raise NotImplementedError

    def reset_startup_error(self):
        raise NotImplementedError
