import requests
import json
import logger
import datetime


class Avanza:
    def __init__(self):
        self.is_authed: bool = False
        self.customer_id: str = ''
        self.authentication_session: str = ''
        self.push_subscription_id: str = ''
        self.security_token: str = ''

    def login(self, username: str, password: str, totp_code: str) -> bool:
        if not all([username, password, totp_code]):
            logger.error("Username, password or totp_code is missing")
            return False

        url = 'https://www.avanza.se/_api/authentication/sessions/usercredentials'
        headers = {
            'User-Agent': 'Avanza/se.avanzabank.androidapplikation (3.21.2 (585); Android 6.0)',
            'Content-Type': 'application/json; charset=UTF-8'
        }
        data = {'maxInactiveMinutes': 240, 'password': password, 'username': username}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 401:
            logger.error("Access denied. Response code from avanza was 401")
            return False
        elif not response.ok:
            logger.error("Authentication failed. Response code from avanza was " + str(response.status_code))
            return False
        if not response.headers['Content-Type'] == 'application/json;charset=utf-8':
            logger.error("Authentication error. Content-Type from avanza was not as expected, got " +
                         response.headers['Content-Type'])
            return False

        content = json.loads(response.content)
        transaction_id = content['twoFactorLogin']['transactionId']
        url = 'https://www.avanza.se/_api/authentication/sessions/totp'
        headers = {
            'User-Agent': 'Avanza/se.avanzabank.androidapplikation (3.21.2 (585); Android 6.0)',
            'Content-Type': 'application/json; charset=UTF-8',
            'VND.se.avanza.security-Totp-Transaction-Id': transaction_id
        }
        data = {"maxInactiveMinutes": 240, "method": "TOTP", "totpCode": totp_code}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if not response.ok:
            logger.error(f"""2FA failed. Used key {totp_code}. Response code was """ + str(response.status_code))
            return False
        content = json.loads(response.content)

        self.is_authed = True
        self.customer_id = content['customerId']
        self.authentication_session = content['authenticationSession']
        self.push_subscription_id = content['pushSubscriptionId']
        self.security_token = response.headers['X-SecurityToken']
        return True

    def get_instrument(self, instrument_id: str, period: str = 'five_years') -> None:
        pass

    def get_all_instrument_ids(self) -> None:
        pass

    def get_all_instruments(self) -> None:
        pass

    def _get_transactions(self, transaction_type: str) -> dict:
        if not self.is_authed:
            return None
        url = f'''https://www.avanza.se/_mobile/account/transactions/{transaction_type}?from=2000-01-01'''
        headers = {
            'User-Agent': 'Avanza API client/1.3.0',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-SecurityToken': self.security_token,
            'X-AuthenticationSession': self.authentication_session
        }
        response = requests.get(url, headers=headers)
        if (response.ok):
            return json.loads(response.content)
        else:
            return None

    def get_account_chart(self):
        if not self.is_authed:
            return None

        overview = self._get_overview()
        good_accounts = [x['accountId'] for x in overview['accounts'] if x['accountType'] == 'Investeringssparkonto']
        if len(good_accounts) < 1:
            return None
        account_id = good_accounts[0]

        url = f'''https://www.avanza.se/_mobile/chart/account/{account_id}?timePeriod=one_year'''
        headers = {
            'User-Agent': 'Avanza API client/1.3.0',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-SecurityToken': self.security_token,
            'X-AuthenticationSession': self.authentication_session
        }
        response = requests.get(url, headers=headers)
        if not response.ok:
            return None

        data = json.loads(response.content)
        dates = [datetime.datetime.strptime(x['date'], '%Y-%m-%d') for x in data['dataSeries']]
        values = [x['value'] for x in data['dataSeries']]
        return (dates, values)

    def _get_overview(self) -> dict:
        if (not self.is_authed):
            return None
        url = 'https://www.avanza.se/_mobile/account/overview'
        headers = {
            'User-Agent': 'Avanza API client/1.3.0',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-SecurityToken': self.security_token,
            'X-AuthenticationSession': self.authentication_session
        }
        response = requests.get(url, headers=headers)
        if response.ok:
            return json.loads(response.content)
        else:
            return None

    def _get_account_overview(self, account_id: str) -> dict:
        if not self.is_authed:
            return None

        url = f'https://www.avanza.se/_mobile/account/{account_id}/overview'
        headers = {
            'User-Agent': 'Avanza API client/1.3.0',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-SecurityToken': self.security_token,
            'X-AuthenticationSession': self.authentication_session
        }
        response = requests.get(url, headers=headers)
        if (response.ok):
            return json.loads(response.content)
        else:
            return None

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
