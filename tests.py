import unittest
import totp


class TestTotpMethods(unittest.TestCase):
    def test_totp(self):
        a: int = totp.totp('JBSWY3DPEHPK3PXP', 6, 30, 1553624198)
        b: str = str(a).zfill(6)
        self.assertEqual(b, '020400')


if __name__ == '__main__':
    unittest.main()
