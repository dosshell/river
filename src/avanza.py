import logger
import datetime as dt
import avanza_api
import apsw
import db_utils
import pandas as pd


class Avanza:
    def __init__(self, cache_db: str = ':memory:'):
        self.is_authed: bool = False
        self.customer_id: str = ''
        self.authentication_session: str = ''
        self.push_subscription_id: str = ''
        self.security_token: str = ''
        self.cache_db = apsw.Connection(cache_db)

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

    def fetch(self) -> None:
        # fetch fund_list
        logger.log("Fetch fund list")
        cursor = self.cache_db.cursor()
        db_utils.create_tables(cursor)
        # new_fund_list = avanza_api.get_fund_list()
        # new_fund_list_values = [(x['orderbookId'], x['name'], x['startDate']) for x in new_fund_list]
        # db_utils.tuplelist_to_sql(cursor, 'fund_list', new_fund_list_values)

        logger.log("Fetch chart list")
        # fetch fund_chart
        all_fund_list = db_utils.sql_to_df(cursor, 'fund_list')
        total_rows = len(all_fund_list.index)
        for index, row in all_fund_list.iterrows():
            logger.log(f'''Fetching: {index}/{total_rows} ({row['orderbook_id']}) "{row['name']}""''')
            orderbook_id = row['orderbook_id']
            last_update_str = cursor.execute(
                f'''SELECT MAX(x) as last_update from fund_chart WHERE orderbook_id={orderbook_id}''').fetchone()[0]
            start_date = dt.datetime.strptime(row['start_date'], "%Y-%m-%d").date()
            if last_update_str is None:
                from_date = start_date
            else:
                from_date = dt.datetime.strptime(last_update_str, '%Y-%m-%dT%H:%M:%S').date()
            d = avanza_api.get_fund_chart_helper(orderbook_id, from_date, dt.date.today(), start_date=start_date)
            new_fund_chart_values = [(orderbook_id, dt.datetime.utcfromtimestamp(v['x'] / 1000).isoformat(), v['y'])
                                     for v in d['dataSerie']]
            db_utils.tuplelist_to_sql(cursor, 'fund_chart', new_fund_chart_values)
        logger.log("fetch done")

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
        return db_utils.sql_to_df(self.cache_db.cursor(), 'fund_list')
