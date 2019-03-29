import unittest
import totp
from avanza import Avanza


class TestTotp(unittest.TestCase):
    def test_totp(self):
        a: str = totp.totp('JBSWY3DPEHPK3PXP', 6, 30, 1553624198)
        self.assertEqual(a, '020400')


class TestAvanzaApi(unittest.TestCase):
    def test_login(self):
        avanza_client = Avanza()
        self.assertEqual(avanza_client.login('username', 'password', 'totp'), False)


if __name__ == '__main__':
    unittest.main()
