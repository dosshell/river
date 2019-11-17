import unittest
import totp
import settings
import test.settings_mock
from unittest.mock import patch
import avanza
import test.requests_mock
import pandas as pd
import apsw


class TestAvanza(unittest.TestCase):
    __cfg = {}
    @classmethod
    @patch('settings.read_settings', new=test.settings_mock.read_settings)
    def setUpClass(cls):
        cls.__cfg = settings.read_settings('settings.json')

    @patch('requests.post', new=test.requests_mock.request_post)
    def test_login(self):
        username = self.__cfg['AvanzaUsername']
        password = self.__cfg['AvanzaPassword']
        priv_key = self.__cfg['AvanzaPrivateKey']
        totp_code = totp.totp(priv_key)
        self.assertEqual(username, '123456')
        self.assertEqual(password, 'secret')
        self.assertIsNotNone(totp_code)
        avanza_client = avanza.Avanza()
        self.assertIsNotNone(avanza_client)
        self.assertTrue(avanza_client.login(username, password, totp_code))

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_get_fund_list(self):
        test_db = apsw.Connection('test/data/test.db')
        avanza_client = avanza.Avanza(test_db)
        fund_list = avanza_client.get_fund_list()
        self.assertTrue(type(fund_list) is pd.DataFrame)

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_fetch(self):
        test_db = apsw.Connection('test/data/test.db')
        avanza_client = avanza.Avanza(test_db)
        avanza_client.fetch()
        fund_list = avanza_client.get_fund_list()
        self.assertGreaterEqual(len(fund_list), 2)
