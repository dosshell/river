import unittest
import totp


class TestTotp(unittest.TestCase):
    def test_totp(self):
        a: str = totp.totp('JBSWY3DPEHPK3PXP', 6, 30, 1553624198)
        self.assertEqual(a, '020400')
