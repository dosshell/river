import base64
import math
import hmac
import time
import hashlib
import logger


def totp(priv_key: bytes,
         digits: int = 6,
         period: int = 30,
         unixtime: int = None) -> int:

    if unixtime is None:
        unixtime = int(time.time())

    logger.log("Generating totp code with unixtime: " + str(unixtime))
    raw_key: bytes = base64.b32decode(priv_key)
    tc: int = math.floor(unixtime / period)
    a: int = hotp(raw_key, tc)
    return str(a).zfill(6)


def hotp(key: bytes, msg: int, digits: int = 6) -> int:
    raw_msg = bytearray(8)
    for n in range(0, 8):
        raw_msg[7 - n] = (msg >> n * 8) & 0xff
    h: bytes = hmac.new(key, raw_msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0f
    ubin = (h[offset] << 24) | (h[offset + 1] << 16) | (h[offset + 2] << 8) | (
        h[offset + 3])
    sbin = ubin & 0x7fffffff
    return sbin % pow(10, digits)
