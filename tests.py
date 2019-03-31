import unittest
import totp
import os
from avanza import Avanza


class TestTotp(unittest.TestCase):
    def test_totp(self):
        a: str = totp.totp('JBSWY3DPEHPK3PXP', 6, 30, 1553624198)
        self.assertEqual(a, '020400')


class TestAvanzaApi(unittest.TestCase):
    def test_login(self):
        avanza_client = Avanza()
        username = os.getenv('river_username')
        password = os.getenv('river_password')
        priv_key = os.getenv('river_priv_key')
        self.assertTrue(all([username, password, priv_key]))
        totp_code = totp.totp(priv_key)
        avanza_client.login(username, password, totp_code)
        # self.assertTrue(avanza_client.login(username, password, totp_code))


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
