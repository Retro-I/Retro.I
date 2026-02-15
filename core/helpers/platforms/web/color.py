from core.helpers.base.color import BaseColorHelper


class WebColorHelper(BaseColorHelper):
    def to_rgb(self, hex_value):
        return "#00FF00"

    def extract_color(self, img_src):
        return "#00FF00"
