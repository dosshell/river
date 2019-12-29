import json
import requests
from typing import List, Dict


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


def raise_error(response_error: ResponseError):
    raise ValueError(
        f'''{response_error.time}: "{response_error.message}"; "{response_error.status_code}";
        "{str(response_error.additional)}";
        "{str(response_error.errors)}"'''
    )


def authenticate(username: str, password: str) -> TwoFactorAuthenticationResponse:
    url = 'https://www.avanza.se/_api/authentication/sessions/usercredentials'
    headers = {'User-Agent': 'Avanza API client/1.3.0', 'Content-Type': 'application/json;charset=UTF-8'}
    data = {'maxInactiveMinutes': 240, 'password': password, 'username': username}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.ok:
        return response.json(object_hook=authenticate_decoder)
    else:
        raise_error(response.json(object_hook=lambda x: ResponseError(**x)))


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
        raise_error(response.json(object_hook=lambda x: ResponseError(**x)))


def get_transactions(transaction_type: str, security_token: str, authentication_session: str):
    url = f'''https://www.avanza.se/_mobile/account/transactions/{transaction_type}?from=2000-01-01'''
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
        raise_error(response.json(object_hook=lambda x: ResponseError(**x)))


def get_account_overview(account_id: str, security_token: str, authentication_session: str) -> dict:
    url = f'https://www.avanza.se/_mobile/account/{account_id}/overview'
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
        raise_error(response.json(object_hook=lambda x: ResponseError(**x)))


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
        raise_error(response.json(object_hook=lambda x: ResponseError(**x)))


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
        raise_error(response.json(object_hook=lambda x: ResponseError(**x)))


def get_fund_list():
    url = 'https://www.avanza.se/_cqbe/fund/list'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-SecurityToken': '-'
    }
    data = {
        "startIndex": 0,
        "indexFund": False,
        "lowCo2": False,
        "regionFilter": [],
        "countryFilter": [],
        "alignmentFilter": [],
        "industryFilter": [],
        "fundTypeFilter": [],
        "interestTypeFilter": [],
        "sortField": "name",
        "sortDirection": "ASCENDING",
        "name": "",
        "recommendedHoldingPeriodFilter": [],
        "companyFilter": []
    }
    response = requests.get(url, headers=headers, data=json.dumps(data))
    if response.ok:
        number_of_funds = response.json()['totalNoFunds']
        funds = []
        for start_index in range(0, number_of_funds, 20):
            data['startIndex'] = start_index
            response = requests.get(url, headers=headers, data=json.dumps(data))
            if response.ok:
                funds.extend(response.json()['fundListViews'])
            else:
                raise_error(response.json(object_hook=lambda x: ResponseError(**x)))
        return funds
    else:
        raise_error(response.json(object_hook=lambda x: ResponseError(**x)))


def get_fund(orderbook_id: int):
    url = f'''https://www.avanza.se/_mobile/market/fund/{orderbook_id}'''
    headers = {'User-Agent': 'Avanza API client/1.3.0', 'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        raise_error(response.json(object_hook=lambda x: ResponseError(**x)))


def get_fund_chart(orderbook_id: int, from_date: str, to_date: str):
    '''max one year for day resolution, can return None values in dataSerie'''
    url = f'''https://www.avanza.se/_cqbe/fund/chart/{orderbook_id}/{from_date}/{to_date}'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        raise_error(response.json(object_hook=lambda x: ResponseError(**x)))
