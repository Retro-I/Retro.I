from core.helpers.base.color import BaseColorHelper


class PiColorHelper(BaseColorHelper):
    def __init__(self):
        self.helper = PiColorHelper()

    def to_rgb(self, hex_value):
        return self.helper.to_rgb(hex_value)

    def extract_color(self, img_src):
        return self.helper.extract_color(img_src)
