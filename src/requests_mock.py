class MockResponse:
    def __init__(self, data="", status_code=200, headers={}):
        self.content = data
        self.status_code = status_code
        self.ok = (status_code == 200)
        self.headers = headers
        self.headers['Content-Type'] = 'application/json;charset=utf-8'


def request_post(url, data=None, headers=None) -> MockResponse:
    if url == 'https://www.avanza.se/_api/authentication/sessions/usercredentials':
        content = """{"twoFactorLogin":{"transactionId":"6d772726-eaef-4f6b-9f8f-54cd445cc7c2","method":"TOTP"}}"""
        r = MockResponse(content, 200)
        return r
    elif url == 'https://www.avanza.se/_api/authentication/sessions/totp':
        content = """{
                        "authenticationSession": "e88ff939-3eef-4b27-881e-ecbd2349d642",
                        "customerId": "304594",
                        "pushSubscriptionId": "19a1facdf9f1917d3398a994b4a0f5dc9f0e7283",
                        "registrationComplete": true
                     }"""
        return MockResponse(content,
                            200,
                            headers={
                                'X-SecurityToken':
                                '40b33e79-a0d6-4432-955e-6d395b6ca0c8'
                            })
    else:
        return MockResponse(None, 404)
