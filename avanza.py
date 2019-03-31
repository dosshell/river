import requests
import json


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