import json
import requests
from typing import List, Dict
from bs4 import BeautifulSoup
import re


class ResponseError:
    def __init__(self, message=None, statusCode=None, time=None, additional=None, errors=None):
        self.message: str = message
        self.status_code: int = statusCode
        self.time: str = time
        self.additional: Dict[any] = additional
        self.errors: List[any] = errors


class Totp:
    def __init__(self, method=None, transactionId=None):
        self.method: str = method
        self.transaction_id: str = transactionId


class TwoFactorAuthenticationResponse:
    def __init__(self, twoFactorLogin):
        self.two_factor_login = twoFactorLogin


class TotpAuthentication:
    def __init__(self,
                 securityToken=None,
                 authenticationSession=None,
                 customerId=None,
                 pushSubscriptionId=None,
                 registrationComplete=None):
        self.authentication_session: str = authenticationSession
        self.customer_id: str = customerId
        self.push_subscription_id: str = pushSubscriptionId
        self.registration_complete: bool = registrationComplete
        self.security_token: str = securityToken


def authenticate_decoder(dct):
    if 'method' in dct and 'transactionId' in dct:
        return Totp(**dct)
    elif 'twoFactorLogin' in dct:
        return TwoFactorAuthenticationResponse(**dct)
    else:
        return dct


def authenticate(username: str, password: str) -> TwoFactorAuthenticationResponse:
    url = 'https://www.avanza.se/_api/authentication/sessions/usercredentials'
    headers = {'User-Agent': 'Avanza API client/1.3.0', 'Content-Type': 'application/json;charset=UTF-8'}
    data = {'maxInactiveMinutes': 240, 'password': password, 'username': username}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if not response.ok:
        return response.json(object_hook=lambda x: ResponseError(**x))
    return response.json(object_hook=authenticate_decoder)


def verify_totp(totp_code: str, transaction_id: str) -> TotpAuthentication:
    url = 'https://www.avanza.se/_api/authentication/sessions/totp'
    headers = {
        'User-Agent': 'Avanza API client/1.3.0',
        'Content-Type': 'application/json;charset=UTF-8',
        'VND.se.avanza.security-Totp-Transaction-Id': transaction_id
    }
    data = {"maxInactiveMinutes": 240, "method": "TOTP", "totpCode": totp_code}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.ok:
        return response.json(
            object_hook=lambda x: TotpAuthentication(securityToken=response.headers['X-SecurityToken'], **x))
    else:
        return response.json(object_hook=lambda x: ResponseError(**x))


def get_transactions(transaction_type: str, security_token: str, authentication_session: str):
    url = f'''https://www.avanza.se/_mobile/account/transactions/{transaction_type}?from=2000-01-01'''
    headers = {
        'User-Agent': 'Avanza API client/1.3.0',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-SecurityToken': security_token,
        'X-AuthenticationSession': authentication_session
    }
    response = requests.get(url, headers=headers)
    if (response.ok):
        return response.json()
    else:
        return response.json(object_hook=lambda x: ResponseError(**x))


def get_account_overview(account_id: str, security_token: str, authentication_session: str) -> dict:
    url = f'https://www.avanza.se/_mobile/account/{account_id}/overview'
    headers = {
        'User-Agent': 'Avanza API client/1.3.0',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-SecurityToken': security_token,
        'X-AuthenticationSession': authentication_session
    }
    response = requests.get(url, headers=headers)
    if (response.ok):
        return response.json()
    else:
        return response.json(object_hook=lambda x: ResponseError(**x))


def get_overview(security_token, authentication_session) -> dict:
    url = 'https://www.avanza.se/_mobile/account/overview'
    headers = {
        'User-Agent': 'Avanza API client/1.3.0',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-SecurityToken': security_token,
        'X-AuthenticationSession': authentication_session
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        return response.json(object_hook=lambda x: ResponseError(**x))


def get_account_chart(account_id, security_token, authentication_session):
    url = f'''https://www.avanza.se/_mobile/chart/account/{account_id}?timePeriod=one_year'''
    headers = {
        'User-Agent': 'Avanza API client/1.3.0',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-SecurityToken': security_token,
        'X-AuthenticationSession': authentication_session
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        return response.json(object_hook=lambda x: ResponseError(**x))


def get_fund_ids():
    url = 'https://www.avanza.se/fonder/lista.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    ctw = soup.find(id='contentTableWrapper')
    last_page = ctw.find(string=re.compile(r'\s*Sista\s*'))
    if last_page is None:
        return None
    last_page_str = last_page.parent['data-requestedpage']
    if last_page_str is None:
        return None
    to = int(last_page_str)

    fund_ids = []
    for page in range(1, to + 1):
        url = (f'https://www.avanza.se/fonder/lista.html?disableSelection=false&name=&page={page}'
               f'&sortField=NAME&sortOrder=ASCENDING&activeTab=overview')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        ct = soup.find(id='contentTable')
        rows = ct.tbody.find_all('tr')
        data_oids = [x['data-oid'] for x in rows]
        fund_ids.extend(data_oids)

    return fund_ids
