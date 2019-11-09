import json as libjson
import urllib.parse


def get_file_content(filename) -> str:
    with open('test/' + filename, "r") as f:
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
        start_index = libjson.loads(data)['startIndex']
        all_content = get_file_content('fund_list.json')
        content = libjson.dumps(libjson.loads(all_content)[str(start_index)])
        return MockResponse(content)
    elif o.path == '/_mobile/market/fund/1949':
        content = get_file_content('fund_1949.json')
        return MockResponse(content)
    elif o.path.startswith('/_cqbe/fund/chart/'):
        orderbook_id = o.path.split('/')[4].split('-')[0]
        year = o.path.split('/')[5].split('-')[0]
        content = get_file_content(f'''fund_chart_{orderbook_id}_{year}.json''')
        return MockResponse(content)
    else:
        return None
