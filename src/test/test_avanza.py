import unittest
import totp
import settings
import test.settings_mock
from unittest.mock import patch
import avanza
import test.requests_mock
import pandas as pd
import json
import datetime as dt
from freezegun import freeze_time


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
        avanza_client = avanza.Avanza()
        fund_list = avanza_client.get_fund_list()
        self.assertTrue(type(fund_list) is pd.DataFrame)

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_fetch_fund_list(self):
        avanza_client = avanza.Avanza()
        self.assertEqual(len(avanza_client.get_fund_list()), 0)
        avanza_client.fetch_fund_list()
        self.assertEqual(len(avanza_client.get_fund_list()), 2)

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_fetch_instrument_chart(self):
        orderbook_id = 377804
        avanza_client = avanza.Avanza()
        with self.assertRaises(ValueError):
            avanza_client.fetch_instrument_chart(orderbook_id)
        avanza_client.fetch_fund_list()
        with freeze_time(lambda: dt.datetime(2019, 12, 28)):
            avanza_client.fetch_instrument_chart(orderbook_id)

        c = avanza_client.cache_db.cursor()
        a = c.execute('select * from fund_chart where orderbook_id=377804').fetchall()
        self.assertEqual(len(a), 1776)
        self.assertEqual(a[-1][1], '2019-12-23T00:00:00+01:00')
        self.assertAlmostEqual(a[-1][2], 2.0873)

        avanza_client2 = avanza.Avanza()
        avanza_client2.fetch_fund_list()
        with freeze_time(lambda: dt.datetime(2018, 9, 24)):
            avanza_client2.fetch_instrument_chart(377804)
        c2 = avanza_client2.cache_db.cursor()
        a2 = c2.execute('select * from fund_chart where orderbook_id=377804').fetchall()
        self.assertEqual(a2[-2][1], '2018-09-21T00:00:00+02:00')
        self.assertAlmostEqual(a2[-2][2], 1.8557)

        with freeze_time(lambda: dt.datetime(2019, 12, 28)):
            avanza_client2.fetch_instrument_chart(377804)
        a3 = c2.execute('select * from fund_chart where orderbook_id=377804').fetchall()
        self.assertEqual(len(a), len(a3))
        self.assertEqual(a, a3)

        # test empty
        with freeze_time(lambda: dt.datetime(2019, 12, 29)):
            avanza_client.fetch_instrument_chart(377804)
        a4 = c.execute('select * from fund_chart where orderbook_id=377804').fetchall()
        self.assertEqual(a, a4)

    @freeze_time("2019-12-28")
    @patch('requests.get', new=test.requests_mock.request_get)
    def test_fetch_all(self):
        avanza_client = avanza.Avanza()
        avanza_client.fetch_all()
        c = avanza_client.cache_db.cursor()
        funds = c.execute("SELECT * FROM fund_list LIMIT 2").fetchall()
        self.assertEqual(len(funds), 2)
        charts = c.execute("SELECT * FROM fund_chart LIMIT 10").fetchall()
        self.assertEqual(len(charts), 10)

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_append_fund_chart(self):
        with open('test/data/fund_chart_377804_20121020_20131015.json') as f:
            chart1_org = json.load(f)
        with open('test/data/fund_chart_377804_20131016_20141011.json') as f:
            chart2_org = json.load(f)
        chart3 = chart1_org.copy()
        chart3['toDate'] = '2013-10-13'

        chart1_fix = chart1_org.copy()
        chart2_fix = chart2_org.copy()
        chart1_fix['dataSerie'] = avanza._dataserie_strip_none(chart1_org['dataSerie'])
        chart2_fix['dataSerie'] = avanza._dataserie_strip_none(chart2_org['dataSerie'])

        # test not overlapping date exception
        with self.assertRaises(ValueError):
            avanza._append_fund_chart(chart3, chart2_fix)

        # test simple output format
        chart_sum = avanza._append_fund_chart(chart1_fix, chart2_fix)

        self.assertEqual(chart_sum['fromDate'], chart1_fix['fromDate'])
        self.assertEqual(chart_sum['toDate'], chart2_fix['toDate'])
        self.assertEqual(chart_sum['id'], chart1_fix['id'])
        self.assertEqual(chart_sum['name'], chart2_fix['name'])
        self.assertEqual(chart_sum['dataSerie'][-1]['x'], chart2_fix['dataSerie'][-1]['x'])
        self.assertEqual(chart_sum['dataSerie'][0]['x'], chart1_fix['dataSerie'][0]['x'])
        self.assertEqual(len(chart_sum['dataSerie']), len(chart1_fix['dataSerie']) + len(chart2_fix['dataSerie']))

        # test simple data
        chart1_short = chart1_fix.copy()
        chart2_short = chart2_fix.copy()
        chart1_short['dataSerie'] = [{'x': 0, 'y': 0.00}, {'x': 1, 'y': 50.00}]
        chart2_short['dataSerie'] = [{'x': 2, 'y': 0.00}, {'x': 3, 'y': 100.00}]

        chart_sum = avanza._append_fund_chart(chart1_short, chart2_short)
        self.assertEqual(chart_sum['dataSerie'][2]['y'], 50.0)
        self.assertEqual(chart_sum['dataSerie'][3]['y'], 200.0)

        # test append overlapping
        d1 = chart1_fix['dataSerie']
        mid_timestamp = (d1[0]['x'] + d1[-1]['x']) / 2
        d1_half = [x for x in d1 if x['x'] <= mid_timestamp]
        chart4 = chart1_fix.copy()
        chart4['toDate'] = dt.date.fromtimestamp(mid_timestamp / 1000).isoformat()
        chart4['dataSerie'] = d1_half
        with self.assertRaises(ValueError):
            avanza._append_fund_chart(chart4, chart1_fix)
