import logger
import datetime
import avanza_api
import apsw
import pandas as pd


def df_to_sql(df: pd.DataFrame, cursor, table_name: str) -> None:
    qs = ','.join(['?'] * len(df.columns))
    cs = ','.join(df.columns.tolist())
    cursor.executemany(f'''insert or ignore into {table_name} ({cs}) values({qs})''', df.values.tolist())


def sql_to_df(cursor, table_name: str) -> pd.DataFrame:
    r = cursor.execute(f'''select * from {table_name}''')
    headers = [x[0] for x in r.getdescription()]
    data = r.fetchall()
    df = pd.DataFrame.from_records(data, columns=headers)
    return df


class Avanza:
    def __init__(self, cache_db: apsw.Connection = None):
        self.is_authed: bool = False
        self.customer_id: str = ''
        self.authentication_session: str = ''
        self.push_subscription_id: str = ''
        self.security_token: str = ''
        if cache_db is None:
            self.cache_db = apsw.Connection(':memory:')
        else:
            self.cache_db = cache_db

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

    def fetch(self):
        cursor = self.cache_db.cursor()

        # Create tables if needed
        cursor.execute('''CREATE TABLE IF NOT EXISTS fund_list(
                orderbook_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )''')
        # Update some index table
        fund_list = avanza_api.get_fund_list()
        orderbook_ids = [int(x['orderbookId']) for x in fund_list]
        names = [x['name'] for x in fund_list]
        data = {'orderbook_id': orderbook_ids, 'name': names}
        df = pd.DataFrame(data, columns=['orderbook_id', 'name'])
        df_to_sql(df, cursor, 'fund_list')

    def get_instrument(self, instrument_id: str, period: str = 'five_years') -> None:
        pass

    def _get_transactions(self, transaction_type: str) -> dict:
        if not self.is_authed:
            return None
        response = avanza_api.get_transactions(transaction_type, self.security_token, self.authentication_session)
        if response is avanza_api.ResponseError:
            return None
        return response

    def get_account_chart(self):
        if not self.is_authed:
            return None

        overview = self._get_overview()
        good_accounts = [x['accountId'] for x in overview['accounts'] if x['accountType'] == 'Investeringssparkonto']
        if len(good_accounts) < 1:
            return None
        account_id = good_accounts[0]

        data = avanza_api.get_account_chart(account_id, self.security_token, self.authentication_session)
        if data is avanza_api.ResponseError:
            return None

        dates = [datetime.datetime.strptime(x['date'], '%Y-%m-%d') for x in data['dataSeries']]
        values = [x['value'] for x in data['dataSeries']]
        return (dates, values)

    def _get_overview(self) -> dict:
        if (not self.is_authed):
            return None
        response = avanza_api.get_overview(self.security_token, self.authentication_session)
        if response is avanza_api.ResponseError:
            return None
        return response

    def _get_account_overview(self, account_id: str) -> dict:
        response = avanza_api.get_account_overview(account_id, self.security_token, self.authentication_session)
        if response is avanza_api.ResponseError:
            return None
        return response

    def get_current_investment(self) -> int:
        if not self.is_authed:
            return None
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
            return None
        overview = self._get_overview()
        sum = 0
        for account in overview['accounts']:
            if account['depositable'] and not account['tradable']:
                sum = sum + account['totalBalance']
        return int(sum)

    def get_own_capital(self) -> int:
        if not self.is_authed:
            return None
        overview = self._get_overview()
        balance = 0
        for account in overview['accounts']:
            if account['depositable']:
                balance = balance + account['ownCapital']
        return int(balance)

    def get_fund_list(self):
        return sql_to_df(self.cache_db.cursor(), 'fund_list')
