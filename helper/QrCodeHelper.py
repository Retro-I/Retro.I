import base64
from io import BytesIO

import qrcode


def str_to_qr_code(value):
    qr = qrcode.make(value)
    buffered = BytesIO()
    qr.save(buffered, format="JPEG")
    s1 = base64.b64encode(buffered.getvalue())
    b64_string = s1.decode("utf-8")
    return b64_string
