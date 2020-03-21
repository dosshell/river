import unittest
import totp
import settings
from unittest.mock import patch
import avanza
import test.requests_mock
import pandas as pd
import json
import datetime as dt
from freezegun import freeze_time
import os


class TestAvanza(unittest.TestCase):
    __cfg: settings.Settings = settings.Settings()

    @classmethod
    def setUpClass(cls):
        cls.__cfg.avanza_username = '123456'
        cls.__cfg.avanza_password = 'secret'
        cls.__cfg.avanza_private_key = 'JBSWY3DPEHPK3PXP'

    @patch('requests.post', new=test.requests_mock.request_post)
    def test_login(self):
        totp_code = totp.totp(self.__cfg.avanza_private_key)
        self.assertIsNotNone(totp_code)
        avanza_client = avanza.Avanza()
        self.assertIsNotNone(avanza_client)
        self.assertTrue(avanza_client.login(self.__cfg.avanza_username, self.__cfg.avanza_password, totp_code))

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_get_fund_list(self):
        avanza_client = avanza.Avanza()
        fund_list = avanza_client.get_fund_list()
        self.assertTrue(type(fund_list) is pd.DataFrame)

    @freeze_time("2019-12-28")
    @patch('requests.get', new=test.requests_mock.request_get)
    def test_fetch_fund_list(self):
        avanza_client = avanza.Avanza()
        self.assertEqual(len(avanza_client.get_fund_list()), 0)
        avanza_client.fetch_fund_list()
        fund_list = avanza_client.get_fund_list()
        self.assertEqual(len(fund_list), 2)

        avanza_client2 = avanza.Avanza()
        avanza_client2.fetch_fund_list(blacklist=[377804])
        fund_list2 = avanza_client2.get_fund_list()
        self.assertEqual(len(fund_list2), 1)

    @freeze_time("2019-12-28")
    @patch('requests.get', new=test.requests_mock.request_get)
    def test_aquire_start_date(self):
        orderbook_ids = {
            32: dt.date(1998, 12, 31),
            35: dt.date(1994, 1, 10),
            38: dt.date(1998, 4, 22),
            351: dt.date(2015, 12, 11)
        }
        for k, v in orderbook_ids.items():
            self.assertEqual(avanza._aquire_start_date(k), v)

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_fetch_instrument_chart(self):
        orderbook_id = 377804
        avanza_client = avanza.Avanza()

        # test that we can not fetch instruments before fund list
        with self.assertRaises(ValueError):
            avanza_client.fetch_instrument_chart(orderbook_id)

        # test to fetch fund list and instruments
        with freeze_time(lambda: dt.datetime(2019, 12, 28)):
            avanza_client.fetch_fund_list()
            avanza_client.fetch_instrument_chart(orderbook_id)

        c = avanza_client.cache_db.cursor()
        ds_fullfetch = c.execute(f'select * from fund_chart where orderbook_id={orderbook_id}').fetchall()
        self.assertEqual(len(ds_fullfetch), 1781)
        self.assertEqual(ds_fullfetch[-1][1], '2019-12-27T00:00:00+01:00')
        self.assertAlmostEqual(ds_fullfetch[-1][2], 2.085)

        # test partial appending
        avanza_client2 = avanza.Avanza()
        with freeze_time(lambda: dt.datetime(2019, 12, 28)):
            avanza_client2.fetch_fund_list()
        with freeze_time(lambda: dt.datetime(2018, 9, 24)):
            avanza_client2.fetch_instrument_chart(orderbook_id)
        c2 = avanza_client2.cache_db.cursor()
        a2 = c2.execute(f'select * from fund_chart where orderbook_id={orderbook_id}').fetchall()
        self.assertEqual(a2[-2][1], '2018-09-21T00:00:00+02:00')
        self.assertAlmostEqual(a2[-2][2], 1.8557)

        with freeze_time(lambda: dt.datetime(2019, 12, 28)):
            avanza_client2.fetch_instrument_chart(orderbook_id)
        ds_doublefetch = c2.execute(f'select * from fund_chart where orderbook_id={orderbook_id}').fetchall()
        self.assertEqual(len(ds_fullfetch), len(ds_doublefetch))
        self.assertEqual(ds_fullfetch, ds_doublefetch)

        # test no append
        with freeze_time(lambda: dt.datetime(2019, 12, 29)):
            avanza_client.fetch_instrument_chart(orderbook_id)
        a4 = c.execute(f'select * from fund_chart where orderbook_id={orderbook_id}').fetchall()
        self.assertEqual(ds_fullfetch, a4)

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

    @freeze_time("2019-12-28")
    @patch('requests.get', new=test.requests_mock.request_get)
    def test_get_fund_chart(self):
        avanza_client = avanza.Avanza()
        avanza_client.fetch_all()
        chart = avanza_client.get_fund_chart(377804)
        self.assertGreater(len(chart), 0)
        self.assertIs(type(chart), pd.DataFrame)

    @patch('requests.get', new=test.requests_mock.request_get)
    def test_append_fund_chart(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/data'
        with open(dir_path + '/fund_chart_377804_2012-10-20_2013-10-15.json') as f:
            chart1_org = json.load(f)
        with open(dir_path + '/fund_chart_377804_2013-10-16_2014-10-11.json') as f:
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
