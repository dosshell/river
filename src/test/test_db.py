import unittest
import db
from avanza import Avanza
import settings
import totp


class TestDb(unittest.TestCase):
    def test_update(self):
        if not settings.is_template:
            avanza_client = Avanza()
            avanza_client.login(settings.config['AvanzaUsername'],
                                settings.config['AvanzaPassword'],
                                totp.totp(settings.config['AvanzaPrivateKey']))
            self.assertTrue(db.update(avanza_client))
