import unittest
import totp
import settings
import settings_mock
from unittest.mock import patch
import avanza
import requests_mock
import pandas as pd


class TestAvanza(unittest.TestCase):
    __cfg = {}
    @classmethod
    @patch('settings.read_settings', new=settings_mock.read_settings)
    def setUpClass(cls):
        cls.__cfg = settings.read_settings('settings.json')

    @patch('requests.post', new=requests_mock.request_post)
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

    @patch('requests.get', new=requests_mock.request_get)
    def test_get_fund_list(self):
        avanza_client = avanza.Avanza()
        fund_list = avanza_client.get_fund_list()
        self.assertTrue(type(fund_list) is pd.DataFrame)

    @patch('requests.get', new=requests_mock.request_get)
    def test_fetch(self):
        avanza_client = avanza.Avanza()
        avanza_client.fetch()
        self.assertTrue(True)
