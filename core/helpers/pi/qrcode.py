from core.helpers.base.qrcode import BaseQrCodeHelper
from helper.qr_code_helper import str_to_qr_code as parent_str_to_qr_code


class PiQrCodeHelper(BaseQrCodeHelper):
    def str_to_qr_code(self, value):
        return parent_str_to_qr_code(value)
