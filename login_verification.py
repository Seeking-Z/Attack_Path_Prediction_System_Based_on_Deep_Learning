import pyotp
import qrcode
import base64
from io import BytesIO


class TwoStepVerification():
    """进行二步验证的类"""
    def __init__(self):
        """初始化"""

    def get_sec(self):
        return pyotp.random_base32()
