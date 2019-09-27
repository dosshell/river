import unittest
import totp
import settings
import settings_mock
from unittest.mock import patch


class TestAvanza(unittest.TestCase):
    __cfg = {}
    @classmethod
    @patch('settings.read_settings', new=settings_mock.read_settings)
    def setUpClass(cls):
        cls.__cfg = settings.read_settings('settings.json')

    def test_login(self):
        username = self.__cfg['AvanzaUsername']
        password = self.__cfg['AvanzaPassword']
        priv_key = self.__cfg['AvanzaPrivateKey']
        totp_code = totp.totp(priv_key)
        self.assertEqual(username, '123456')
        self.assertEqual(password, 'secret')
        self.assertIsNotNone(totp_code)
