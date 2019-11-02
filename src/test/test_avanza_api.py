import unittest
from unittest.mock import patch
import avanza_api
import requests_mock


class TestAvanzaApi(unittest.TestCase):
    @patch('requests.post', new=requests_mock.request_post)
    def test_login(self):
        auth = avanza_api.authenticate('123456', 'secret')
        self.assertTrue(hasattr(auth, 'two_factor_login'))

    @patch('requests.get', new=requests_mock.request_get)
    def test_get_fund_list(self):
        fund_list = avanza_api.get_fund_list()
        self.assertEqual(len(fund_list), 60)
        self.assertEqual(fund_list[2]['name'], 'AGCM Asia Growth RC SEK')
        self.assertEqual(fund_list[55]['orderbookId'], 736)
