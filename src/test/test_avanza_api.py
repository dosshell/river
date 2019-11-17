import unittest
from unittest.mock import patch
import avanza_api
import test.requests_mock
import datetime


class TestAvanzaApi(unittest.TestCase):
    @patch('requests.post', new=test.requests_mock.request_post)
    def test_login(self):
        auth = avanza_api.authenticate('123456', 'secret')
        self.assertTrue(hasattr(auth, 'two_factor_login'))

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_get_fund_list(self):
        fund_list = avanza_api.get_fund_list()
        self.assertGreaterEqual(len(fund_list), 2)
        self.assertEqual(fund_list[0]['name'], 'Avanza 75')
        self.assertEqual(fund_list[1]['orderbookId'], 944976)

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_get_fund(self):
        fund = avanza_api.get_fund(377804)
        self.assertEqual(type(fund), dict)
        self.assertEqual(int(fund['id']), 377804)

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_get_chart(self):
        fund = avanza_api.get_fund_chart(377804, '2012-01-01', '2020-01-01')
        self.assertEqual(type(fund), dict)

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_get_fund_chart_helper(self):
        fund = avanza_api.get_fund_chart_helper(377804, datetime.date(2012, 1, 1), datetime.date(2020, 1, 1))
        self.assertGreaterEqual(len(fund['dataSerie']), 500)
