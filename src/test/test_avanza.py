import unittest
import warnings
import totp
import settings
from avanza import Avanza


class TestAvanzaApi(unittest.TestCase):
    __is_template = False
    __cfg = {}
    @classmethod
    def setUpClass(cls):
        cls.__cfg = settings.load_settings('settings.json')
        if (cls.__cfg['AvanzaUsername'] == 'Your Avanza username'):
            cls.__is_template = True

        if not cls.__is_template:
            cls.avanza_client = Avanza()
        else:
            warnings.warn("Can not test Avanza with template settings.")

    def step0_test_login(self):
        if not self.__is_template:
            username = self.__cfg['AvanzaUsername']
            password = self.__cfg['AvanzaPassword']
            priv_key = self.__cfg['AvanzaPrivateKey']
            totp_code = totp.totp(priv_key)
            self.assertTrue(self.avanza_client.login(
                username, password, totp_code))

    def step1_test_overview(self):
        overview = self.avanza_client.get_overview()
        self.assertIsNotNone(overview)
        for account in overview['accounts']:
            self.assertIsNotNone(self.avanza_client.get_account_overview(account['accountId']))
