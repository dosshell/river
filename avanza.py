import requests
import json
import unittest
from settings import config as cfg
from settings import is_template as is_template_settings
import totp
import warnings


class Avanza:
    def __init__(self):
        self.is_authed: bool = False
        self.customer_id: str = ''
        self.authentication_session: str = ''
        self.push_subscription_id: str = ''
        self.security_token: str = ''

    def login(self, username: str, password: str, totp_code: str) -> bool:
        if not all([username, password, totp_code]):
            return False
        url = 'https://www.avanza.se/_api/authentication/sessions/usercredentials'
        headers = {
            'User-Agent': 'Avanza/se.avanzabank.androidapplikation (3.21.2 (585); Android 6.0)',
            'Content-Type': 'application/json; charset=UTF-8'
        }
        data = {
            'maxInactiveMinutes': 240,
            'password': password,
            'username': username
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 401:
            return False
        elif not response.ok:
            raise ValueError('Some error here', response.status_code)
        if not response.headers['Content-Type'] == 'application/json;charset=utf-8':
            return False

        content = json.loads(response.content)
        transaction_id = content['twoFactorLogin']['transactionId']
        url = 'https://www.avanza.se/_api/authentication/sessions/totp'
        headers = {
            'User-Agent': 'Avanza/se.avanzabank.androidapplikation (3.21.2 (585); Android 6.0)',
            'Content-Type': 'application/json; charset=UTF-8',
            'VND.se.avanza.security-Totp-Transaction-Id': transaction_id
        }
        data = {
            "maxInactiveMinutes": 240,
            "method": "TOTP",
            "totpCode": totp_code
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if not response.ok:
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

    def get_overview(self) -> dict:
        if (not self.is_authed):
            return None
        url = 'https://www.avanza.se/_mobile/account/overview'
        headers = {
            'User-Agent': 'Avanza/se.avanzabank.androidapplikation (3.21.2 (585); Android 6.0)',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-SecurityToken': self.security_token,
            'X-AuthenticationSession': self.authentication_session
        }
        response = requests.get(url, headers=headers)
        if (response.ok):
            return json.loads(response.content)
        else:
            return None

    def get_account_overview(self, account_id: str) -> dict:
        if (not self.is_authed):
            return None

        url = f'https://www.avanza.se/_mobile/account/{account_id}/overview'
        headers = {
            'User-Agent': 'Avanza/se.avanzabank.androidapplikation (3.21.2 (585); Android 6.0)',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-SecurityToken': self.security_token,
            'X-AuthenticationSession': self.authentication_session
        }
        response = requests.get(url, headers=headers)
        if (response.ok):
            return json.loads(response.content)
        else:
            return None


class TestAvanzaApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.avanza_client = Avanza()
        if (is_template_settings):
            warnings.warn("Can not test Avanza with template settings.")

    def step0_test_login(self):
        if (not is_template_settings):
            username = cfg['AvanzaUsername']
            password = cfg['AvanzaPassword']
            priv_key = cfg['AvanzaPrivateKey']

            totp_code = totp.totp(priv_key)
            self.assertTrue(self.avanza_client.login(
                username, password, totp_code))

    def step1_test_overview(self):
        overview = self.avanza_client.get_overview()
        self.assertIsNotNone(overview)
        for account in overview['accounts']:
            self.assertIsNotNone(self.avanza_client.get_account_overview(account['accountId']))
