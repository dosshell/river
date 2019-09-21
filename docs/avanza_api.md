```cmd
socat openssl:www.avanza.se:443,verify=0,crnl -
```

# Authentication

Client:
```
POST /_api/authentication/sessions/username HTTP/1.1
Accept: */*
Content-Type: application/json
User-Agent: Avanza API client/1.3.0
Content-Length: 71
Host: www.avanza.se
Connection: close

{"maxInactiveMinutes":1440,"password":"PASSWORD","username":"USERNAME"}
```

Server:
```
HTTP/1.1 200 OK
Date: Wed, 02 May 2018 16:17:01 GMT
Server: Apache
X-SecurityToken: 3dc9db8e-d5ef-4d0e-b890-ae9fe62ef761
Cache-Control: no-cache, no-store, must-revalidate, private
Pragma: no-cache
Content-Type: application/json;charset=utf-8
Set-Cookie: csid=e34cd2eb-6260-44b4-bfa9-c04a024a5d58;Path=/;Secure;HttpOnly
Connection: close
Transfer-Encoding: chunked
Strict-Transport-Security: max-age=31536000

b2
{"authenticationSession":"e34cd2eb-6260-44b4-bfa9-c04a024a5d58","pushSubscriptionId":"5ec8b9809a899f4ceaa4c877c72c596c82723265","customerId":"304594","registrationComplete":true}
0
```

# getInstrument

Client:
```
GET /_mobile/market/stock/12345 HTTP/1.1
Accept: */*
Content-Type: application/json
User-Agent: Avanza API client/1.3.0
Content-Length: 2
X-AuthenticationSession: e34cd2eb-6260-44b4-bfa9-c04a024a5d58
X-SecurityToken: 3dc9db8e-d5ef-4d0e-b890-ae9fe62ef761
Host: 127.0.0.1:1224
Connection: close

{}
```

# getChartdata

Client:
```
GET /_mobile/chart/orderbook/12345?timePeriod=one_year HTTP/1.1
Accept: */*
Content-Type: application/json
User-Agent: Avanza API client/1.3.0
Content-Length: 2
X-AuthenticationSession: e34cd2eb-6260-44b4-bfa9-c04a024a5d58
X-SecurityToken: 3dc9db8e-d5ef-4d0e-b890-ae9fe62ef761
Host: 127.0.0.1:1224
Connection: close

{}
```


# Nya PI:t
```
POST https://www.avanza.se/_api/authentication/sessions/usercredentials
Content-Type:	application/json; charset=UTF-8
Content-Length:	69
Host:	www.avanza.se
Connection:	Keep-Alive
Accept-Encoding: gzip
User-Agent Avanza/se.avanzabank.androidapplikation (3.21.2 (585); Android 6.0)
{
    "maxInactiveMinutes": 240,
    "password": "password",
    "username": "username"
}
```
Response:
```
Set-Cookie: AZAMFATRANSACTION=fc2a3fa7-5e61-4f31-a75c-802835d596ee;Path=/;Expires=Tue, 29 May 2018 17:29:25 GMT;Secure;HttpOnly
Keep-Alive:	timeout=70, max=100
Strict-Transport-Security:	max-age=31536000
{
    "twoFactorLogin": {
        "method": "TOTP",
        "transactionId": "fc2a3fa7-5e61-4f31-a75c-802835d596ee"
    }
}
```


```
POST https://www.avanza.se/_api/authentication/sessions/totp
VND.se.avanza.security-Totp-Transaction-Id:	fc2a3fa7-5e61-4f31-a75c-802835d596ee
User-Agent:	Avanza/se.avanzabank.androidapplikation (3.21.2 (585); Android 6.0)
{
    "maxInactiveMinutes": 240,
    "method": "TOTP",
    "totpCode": "634253"
}
```
Response:
```
X-SecurityToken: 40b33e79-a0d6-4432-955e-6d395b6ca0c8
Set-Cookie:	csid=e88ff939-3eef-4b27-881e-ecbd2349d642;Path=/;Secure;HttpOnly
{
    "authenticationSession": "e88ff939-3eef-4b27-881e-ecbd2349d642",
    "customerId": "304594",
    "pushSubscriptionId": "19a1facdf9f1917d3398a994b4a0f5dc9f0e7283",
    "registrationComplete": true
}
```
