import requests
import json


class Avanza:
    def __init__(self):
        is_authed: bool = False           # noqa: F841
        customer_id: str = ''             # noqa: F841
        authentication_session: str = ''  # noqa: F841
        push_subscription_id: str = ''    # noqa: F841
        security_token: str = ''          # noqa: F841

    def login(self, username: str, password: str, totp_code: str) -> bool:
        if not all([username, password, totp_code]):
            return False
        url = 'https://www.avanza.se/_api/authentication/sessions/usercredentials'
        headers = {
            'User-Agent': 'Avanza/se.avanzabank.androidapplikation (3.21.2 (585); Android 6.0)',
            'Content-Type': 'application/json; charset=UTF-8'
        }
        data = {}
        data['maxInactiveMinutes'] = 240
        data['password'] = password
        data['username'] = username
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.ok:
            return True
        elif response.status_code == 401:
            return False
        else:
            raise ValueError('Some error here', response.status_code)

    def get_instrument(self, instrument_id: str, period: str = 'five_years') -> None:
        pass

    def get_all_instrument_ids(self) -> None:
        pass

    def get_all_instruments(self) -> None:
        pass
