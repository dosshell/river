import json
import requests
from typing import List, Dict
import datetime


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
    if not response.ok:
        return None
    number_of_funds = response.json()['totalNoFunds']
    funds = []
    for start_index in range(0, number_of_funds, 20):
        data['startIndex'] = start_index
        response = requests.get(url, headers=headers, data=json.dumps(data))
        if not response.ok:
            return None
        funds.extend(response.json()['fundListViews'])
    return funds


def get_fund(orderbook_id: int):
    url = f'''https://www.avanza.se/_mobile/market/fund/{orderbook_id}'''
    headers = {'User-Agent': 'Avanza API client/1.3.0', 'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        return response.json(object_hook=lambda x: ResponseError(**x))


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
        return response.json(object_hook=lambda x: ResponseError(**x))


def get_fund_chart_helper(orderbook_id: int, from_date: datetime.date, to_date: datetime.date, start_date=None):
    '''Handles more than one year with day resolution and does not return None values'''
    '''Returns the none named super procent like factor'''

    if start_date is None:
        meta = get_fund(orderbook_id)
        meta_from = datetime.datetime.strptime(meta['startDate'], '%Y-%m-%d').date()
    else:
        meta_from = start_date

    today = datetime.date.today()

    trimmed_from = max(meta_from, from_date)
    trimmed_to = min(today, to_date)

    nose_end = min(from_date.replace(year=trimmed_from.year + 1, month=1, day=1), trimmed_to)
    tail_start = max(to_date.replace(month=1, day=1), trimmed_to)

    merged = {
        'id': str(orderbook_id),
        'dataSerie': [],
        'fromDate': from_date.isoformat(),
        'toDate': to_date.isoformat()
    }

    nose = get_fund_chart(orderbook_id, trimmed_from.isoformat(), nose_end.isoformat())
    nose['dataSerie'] = [x for x in nose['dataSerie'] if x['y'] is not None]
    for n in nose['dataSerie']:
        n['y'] = n['y'] / 100 + 1
    merged['dataSerie'].extend(nose['dataSerie'])

    proc_fix = 1.0
    if len(merged['dataSerie']) >= 1:
        proc_fix = merged['dataSerie'][-1]['y']

    for year in range(nose_end.year, tail_start.year):
        mid = get_fund_chart(orderbook_id,
                             datetime.date(year, 1, 1).isoformat(),
                             datetime.date(year + 1, 1, 1).isoformat())
        mid['dataSerie'] = [x for x in mid['dataSerie'] if x['y'] is not None]
        for n in mid['dataSerie']:
            n['y'] = proc_fix * (n['y'] / 100 + 1)
        merged['dataSerie'].extend(mid['dataSerie'])
        if len(merged['dataSerie']) >= 1:
            proc_fix = merged['dataSerie'][-1]['y']

    if tail_start < trimmed_to:
        tail = get_fund_chart(orderbook_id, tail_start.isoformat(), trimmed_to.isoformat())
        tail['dataSerie'] = [x for x in tail['dataSerie'] if x['y'] is not None]
        for n in tail['dataSerie']:
            n['y'] = proc_fix * (n['y'] / 100 + 1)
        merged['dataSerie'].extend(tail['dataSerie'])

    return merged
