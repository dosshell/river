import unittest
import totp
import warnings
from settings import config as cfg
from avanza import Avanza


class TestTotp(unittest.TestCase):
    def test_totp(self):
        a: str = totp.totp('JBSWY3DPEHPK3PXP', 6, 30, 1553624198)
        self.assertEqual(a, '020400')


class TestAvanzaApi(unittest.TestCase):
    def test_login(self):
        avanza_client = Avanza()
        username = cfg['AvanzaUsername']
        password = cfg['AvanzaPassword']
        priv_key = cfg['AvanzaPrivateKey']
        if (all([username, password, priv_key])):
            totp_code = totp.totp(priv_key)
            avanza_client.login(username, password, totp_code)
        else:
            warnings.warn("Complete credentials was not given, ignoring avanza test")


if __name__ == '__main__':
    unittest.main()
