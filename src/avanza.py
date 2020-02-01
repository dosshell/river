import logger
import datetime as dt
import avanza_api
import apsw
import db_utils
import pandas as pd
import numpy as np
from dateutil import tz
from dateutil.parser import isoparse
from typing import List


class Avanza:
    def __init__(self, cache_db: str = ':memory:'):
        self.is_authed: bool = False
        self.customer_id: str = ''
        self.authentication_session: str = ''
        self.push_subscription_id: str = ''
        self.security_token: str = ''
        self.cache_db = apsw.Connection(cache_db)
        db_utils.create_tables(self.cache_db)

    def _get_transactions(self, transaction_type: str) -> dict:
        if not self.is_authed:
            raise ValueError("Not authenticated")
        return avanza_api.get_transactions(transaction_type, self.security_token, self.authentication_session)

    def _get_overview(self) -> dict:
        if not self.is_authed:
            raise ValueError("Not authenticated")
        return avanza_api.get_overview(self.security_token, self.authentication_session)

    def _get_account_overview(self, account_id: str) -> dict:
        if not self.is_authed:
            raise ValueError("Not authenticated")
        return avanza_api.get_account_overview(account_id, self.security_token, self.authentication_session)

    def login(self, username: str, password: str, totp_code: str) -> bool:
        auth_response = avanza_api.authenticate(username, password)
        if type(auth_response) is avanza_api.ResponseError:
            if auth_response.status_code == 401:
                logger.error("Access denied. Response code from avanza was 401")
                return False
            else:
                logger.error("Authentication failed. Response code from avanza was " + str(auth_response.status_code))
                return False

        totp_response = avanza_api.verify_totp(totp_code, auth_response.two_factor_login.transaction_id)

        if type(totp_response) is avanza_api.ResponseError:
            logger.error(f"""2FA failed. Used key {totp_code}. Response code was """ + str(totp_response.status_code))
            return False

        self.is_authed = True
        self.customer_id = totp_response.customer_id
        self.authentication_session = totp_response.authentication_session
        self.push_subscription_id = totp_response.push_subscription_id
        self.security_token = totp_response.security_token
        return True

    def fetch_all(self, blacklist: List[int] = []) -> None:
        self.fetch_fund_list(blacklist)
        fund_list = self.get_fund_list()
        for i, n in fund_list.iterrows():
            logger.log(f"""fetching ({i+1}/{len(fund_list)}) {n['orderbook_id']} {n['name']}""")
            self.fetch_instrument_chart(n['orderbook_id'])

    def fetch_fund_list(self, blacklist: List[int] = []) -> None:
        logger.log("Fetch fund list")
        fund_list = avanza_api.get_fund_list()
        fund_list2 = avanza_api.get_fund_list()

        if fund_list != fund_list2:
            raise ValueError("Fund list data changed during fetch")

        filtred_fund_list = [x for x in fund_list if x['orderbookId'] not in blacklist]

        skipping = []
        # fix broken avanza start_date
        for i in range(len(filtred_fund_list)):
            logger.log(f'''Fetch start_date ({i+1}/{len(filtred_fund_list)}) for '''
                       f'''{filtred_fund_list[i]['orderbookId']} "{filtred_fund_list[i]['name']}"''')
            start_date = _aquire_start_date(filtred_fund_list[i]['orderbookId'])
            if start_date is not None:
                filtred_fund_list[i]['startDate'] = start_date.isoformat()
            else:
                logger.log(f'''Skipping {filtred_fund_list[i]['orderbookId']} "{filtred_fund_list[i]['name']}"'''
                           f''' due to no data''')
                skipping.append(filtred_fund_list[i]['orderbookId'])

        fund_list_values = [(x['orderbookId'], x['name'], x['startDate'], 1) for x in filtred_fund_list
                            if x['orderbookId'] not in skipping]
        db_utils.tuplelist_to_sql(self.cache_db, 'fund_list', fund_list_values)

    def fetch_instrument_chart(self, orderbook_id: int) -> None:
        # get latest update date
        c = self.cache_db.cursor()
        f = c.execute("SELECT * from fund_list WHERE orderbook_id=?", [orderbook_id]).fetchone()
        if f is None:
            raise ValueError(f"""Unknown orderbook_id: {orderbook_id}""")
        last_update = c.execute("SELECT * from fund_chart WHERE orderbook_id=? ORDER BY DATE(x) DESC LIMIT 1",
                                [orderbook_id]).fetchone()

        # build first fund_chart_data
        if last_update is None:
            fund_start_date = f[2]
            head = avanza_api.get_fund_chart(orderbook_id, fund_start_date, fund_start_date)
            head['name'] = f[1]  # fix avanza encoding bug
            if len(head['dataSerie']) == 0:
                raise ValueError("There are no entry at start date")
            if head['dataSerie'][0]['y'] is None:
                raise ValueError("Start value of fund is none")  # todo: check if this is possible
            if head['dataSerie'][0]['y'] != 0:
                logger.log(f"""Warning: Start value of fund {orderbook_id} "{f[1]}" is """
                           f"""not zero ({head['dataSerie'][0]['y']})""")
                head['dataSerie'][0]['y'] = 0
        else:
            d = isoparse(last_update[1])
            x = int(d.timestamp() * 1000)
            y = (last_update[2] - 1) * 100
            head = {
                'fromDate': d.date().isoformat(),
                'toDate': d.date().isoformat(),
                'id': str(f[0]),
                'name': f[1],
                'dataSerie': [{
                    'x': x,
                    'y': y
                }]
            }

        # start appending
        stop_date = dt.date.today()
        start_date = dt.datetime.strptime(head['toDate'], "%Y-%m-%d").date() + dt.timedelta(days=1)
        days = (stop_date - start_date).days

        for n in range(0, days, 361):
            start = start_date + dt.timedelta(days=n)
            stop = start_date + dt.timedelta(n + 360)
            if stop > stop_date:
                stop = stop_date
            b = avanza_api.get_fund_chart(orderbook_id, start.isoformat(), stop.isoformat())
            b['name'] = f[1]  # fix avanza encoding bug
            b['dataSerie'] = _dataserie_strip_none(b['dataSerie'])
            head = _append_fund_chart(head, b)

        # insert "head" to sql db
        fund_chart_values = [(orderbook_id, _timestamp_to_datetime(v['x']).isoformat(), round(v['y'] / 100 + 1, 8))
                             for v in head['dataSerie']]
        db_utils.tuplelist_to_sql(self.cache_db, 'fund_chart', fund_chart_values)

    def get_fund_chart(self, orderbook_id: int) -> pd.DataFrame:
        return db_utils.sql_to_df(self.cache_db, 'fund_chart')

    def get_account_chart(self) -> pd.DataFrame:
        if not self.is_authed:
            raise ValueError("Not authenticated")

        overview = self._get_overview()
        good_accounts = [x['accountId'] for x in overview['accounts'] if x['accountType'] == 'Investeringssparkonto']
        if len(good_accounts) < 1:
            return None
        account_id = good_accounts[0]

        data = avanza_api.get_account_chart(account_id, self.security_token, self.authentication_session)

        data = [(dt.datetime.strptime(x['date'], '%Y-%m-%d'), x['value']) for x in data['dataSeries']]
        df = pd.DataFrame.from_records(data, columns=['date', 'value'])
        return df

    def get_current_investment(self) -> int:
        if not self.is_authed:
            raise ValueError("Not authenticated")
        overview = self._get_overview()
        depositables = []
        for account in overview['accounts']:
            if account['depositable'] and account['tradable']:
                depositables.append(account['accountId'])

        transactions = self._get_transactions('deposit-withdraw')
        sum = 0
        for transaction in transactions['transactions']:
            if transaction['account']['id'] in depositables:
                sum = sum + transaction['amount']
        return int(sum)

    def get_value_in_the_mattress(self) -> int:
        if not self.is_authed:
            raise ValueError("Not authenticated")
        overview = self._get_overview()
        sum = 0
        for account in overview['accounts']:
            if account['depositable'] and not account['tradable']:
                sum = sum + account['totalBalance']
        return int(sum)

    def get_own_capital(self) -> int:
        if not self.is_authed:
            raise ValueError("Not authenticated")
        overview = self._get_overview()
        balance = 0
        for account in overview['accounts']:
            if account['depositable']:
                balance = balance + account['ownCapital']
        return int(balance)

    def get_fund_list(self) -> pd.DataFrame:
        return db_utils.sql_to_df(self.cache_db, 'fund_list')


def _timestamp_to_datetime(avanza_timestamp: int) -> dt.datetime:
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Stockholm')
    time = dt.datetime.utcfromtimestamp(avanza_timestamp / 1000).replace(tzinfo=from_zone).astimezone(to_zone)
    return time


def _aquire_start_date(orderbook_id: int) -> dt.date:
    fund_data = avanza_api.get_fund_chart(orderbook_id, '1900-01-01', dt.date.today().isoformat())
    ds = _dataserie_strip_none(fund_data['dataSerie'])
    if len(ds) < 1:
        return None
    first_time = _timestamp_to_datetime(ds[0]['x'])
    start = first_time.date() - dt.timedelta(days=180)
    stop = first_time.date() + dt.timedelta(days=180)
    fund_data2 = avanza_api.get_fund_chart(orderbook_id, start.isoformat(), stop.isoformat())
    ds2 = _dataserie_strip_none(fund_data2['dataSerie'])
    start_time = _timestamp_to_datetime(ds2[0]['x'])
    return start_time.date()


def _dataserie_strip_none(data_serie: dict) -> dict:
    i = 0
    for n in range(len(data_serie)):
        if data_serie[n]['y'] is not None:
            break
        else:
            i = i + 1
    return data_serie[i:]


def _append_fund_chart(chart1: dict, chart2: dict) -> dict:
    t1 = dt.datetime.strptime(chart1['toDate'], '%Y-%m-%d').date()
    t2 = dt.datetime.strptime(chart2['fromDate'], '%Y-%m-%d').date()

    t2_should = t1 + dt.timedelta(days=1)
    if t2 != t2_should:
        raise ValueError("Time periods is not adjacent")
    if chart1['id'] != chart2['id']:
        raise ValueError("Id does not match")
    if chart1['name'] != chart2['name']:
        raise ValueError("Name does not match")
    if None in [x['y'] for x in chart1['dataSerie']]:
        raise ValueError("None type in chart1 is not supported")
    if None in [x['y'] for x in chart2['dataSerie']]:
        raise ValueError("None type in chart2 is not supported")

    d1 = chart1['dataSerie']
    d2_e = chart2['dataSerie']

    tx = d1[-1]['x']
    d2 = [x for x in d2_e if x['x'] > tx]
    x2 = [x['x'] for x in d2 if x['x'] > tx]

    y1 = np.array([x['y'] for x in d1])
    y2 = np.array([x['y'] for x in d2])

    c = y1[-1] / 100 + 1
    y2_c = y2 / 100 + 1
    y2_cn = np.multiply(y2_c, c)
    y2_n = (y2_cn - 1) * 100

    d2_n = [{'x': x[0], 'y': x[1]} for x in zip(x2, y2_n)]

    merged = {
        "id": chart1['id'],
        "dataSerie": d1 + d2_n,
        "name": chart1['name'],
        "fromDate": chart1['fromDate'],
        "toDate": chart2['toDate']
    }

    return merged
