import os

from helper.Constants import Constants


class SplashscreenHelper:
    def get_splashscreens(self) -> list[str]:
        filenames = [
            f
            for f in os.listdir(Constants.splashscreen_path())
            if os.path.isfile(os.path.join(Constants.splashscreen_path(), f))
        ]
        return sorted(filenames)

    def update_splashscreen(self, splashscreen="splash.png"):
        splashscreen_path = f"{Constants.splashscreen_path()}/{splashscreen}"
        os.system(f"sh {Constants.pwd()}/scripts/update_system_splash.sh {splashscreen_path}")
