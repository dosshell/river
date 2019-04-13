import unittest
import db


class TestDb(unittest.TestCase):
    def test_update(self):
        db.update()
