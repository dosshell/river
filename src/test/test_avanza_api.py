import unittest
from unittest.mock import patch
import avanza_api
import requests_mock
import datetime


class TestAvanzaApi(unittest.TestCase):
    @patch('requests.post', new=requests_mock.request_post)
    def test_login(self):
        auth = avanza_api.authenticate('123456', 'secret')
        self.assertTrue(hasattr(auth, 'two_factor_login'))

    @patch('requests.get', new=requests_mock.request_get)
    def test_get_fund_list(self):
        fund_list = avanza_api.get_fund_list()
        self.assertGreaterEqual(len(fund_list), 80)
        self.assertEqual(fund_list[2]['name'], 'AGCM Asia Growth RC SEK')
        self.assertEqual(fund_list[55]['orderbookId'], 736)

    @patch('requests.get', new=requests_mock.request_get)
    def test_get_fund(self):
        fund = avanza_api.get_fund(1949)
        self.assertEqual(type(fund), dict)

    @patch('requests.get', new=requests_mock.request_get)
    def test_get_chart(self):
        fund = avanza_api.get_chart(1949, '2010-01-01', '2011-01-01')
        self.assertEqual(type(fund), dict)

    @patch('requests.get', new=requests_mock.request_get)
    def test_get_chart_helper(self):
        fund = avanza_api.get_chart_helper(1949, datetime.date(2010, 5, 16), datetime.date(2012, 3, 11))
        self.assertGreaterEqual(len(fund['dataSerie']), 500)
