from core.helpers.base.color import BaseColorHelper
from helper.ColorHelper import ColorHelper


class PiColorHelper(BaseColorHelper):
    def __init__(self):
        self.helper = ColorHelper()

    def to_rgb(self, hex_value):
        return self.helper.to_rgb(hex_value)

    def extract_color(self, img_src):
        return self.helper.extract_color(img_src)
