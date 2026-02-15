class BaseColorHelper:
    def to_rgb(self, hex_value):
        raise NotImplementedError

    def extract_color(self, img_src):
        raise NotImplementedError
