import unittest
import warnings
import totp
from avanza import Avanza
from settings import is_template as is_template_settings
from settings import config as cfg


class TestAvanzaApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.avanza_client = Avanza()
        if (is_template_settings):
            warnings.warn("Can not test Avanza with template settings.")

    def step0_test_login(self):
        if (not is_template_settings):
            username = cfg['AvanzaUsername']
            password = cfg['AvanzaPassword']
            priv_key = cfg['AvanzaPrivateKey']

            totp_code = totp.totp(priv_key)
            self.assertTrue(self.avanza_client.login(
                username, password, totp_code))

    def step1_test_overview(self):
        overview = self.avanza_client.get_overview()
        self.assertIsNotNone(overview)
        for account in overview['accounts']:
            self.assertIsNotNone(self.avanza_client.get_account_overview(account['accountId']))
