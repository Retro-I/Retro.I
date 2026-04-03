class BaseSplashscreenHelper:
    def get_splashscreens(self) -> list[str]:
        raise NotImplementedError

    def update_splashscreen(self, splashscreen):
        raise NotImplementedError
