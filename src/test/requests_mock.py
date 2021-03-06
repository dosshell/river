import json as libjson
import urllib.parse


def get_file_content(filename) -> str:
    with open('test/data/' + filename, "r") as f:
        return f.read()


class MockResponse:
    def __init__(self, data="", status_code=200, headers={}):
        self.content = data
        self.status_code = status_code
        self.ok = (status_code == 200)
        self.headers = headers
        self.headers['Content-Type'] = 'application/json;charset=utf-8'

    def json(self, object_hook=None):
        return libjson.loads(self.content, object_hook=object_hook)


def request_post(url, data=None, headers=None) -> MockResponse:
    if url == 'https://www.avanza.se/_api/authentication/sessions/usercredentials':
        content = """{"twoFactorLogin":{"transactionId":"6d772726-eaef-4f6b-9f8f-54cd445cc7c2","method":"TOTP"}}"""
        r = MockResponse(content)
        return r
    elif url == 'https://www.avanza.se/_api/authentication/sessions/totp':
        content = """{
                        "authenticationSession": "e88ff939-3eef-4b27-881e-ecbd2349d642",
                        "customerId": "304594",
                        "pushSubscriptionId": "19a1facdf9f1917d3398a994b4a0f5dc9f0e7283",
                        "registrationComplete": true
                     }"""
        return MockResponse(content, headers={'X-SecurityToken': '40b33e79-a0d6-4432-955e-6d395b6ca0c8'})
    else:
        return MockResponse(None, 404)


def request_get(url, headers=None, data=None) -> MockResponse:
    o = urllib.parse.urlparse(url)
    if o.path == '/_cqbe/fund/list':
        content = get_file_content('fund_list.json')
        return MockResponse(content)
    elif o.path.startswith('/_mobile/market/fund/'):
        id = o.path.split('/')[4]
        content = get_file_content(f'''fund_{id}.json''')
        return MockResponse(content)
    elif o.path.startswith('/_cqbe/fund/chart/'):
        orderbook_id = o.path.split('/')[4]
        from_date = o.path.split('/')[5]
        to_date = o.path.split('/')[6]
        content = get_file_content(f'''fund_chart_{orderbook_id}_{from_date}_{to_date}.json''')
        return MockResponse(content)
    else:
        raise ValueError("Unknown url")
