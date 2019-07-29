import sqlite3


class Database:
    '''A simple database interface'''

    def __init__(self):
        self._conn = None

    def open(self, db_file: str, non_persistent: bool = False):
        if not non_persistent:
            self._conn = sqlite3.connect(db_file)
        else:
            source = sqlite3.connect(db_file)
            self._conn = sqlite3.connect(':memory:')
            source.backup(self._conn)
            source.close()

    def close(self):
        self._conn.close()

    def backup(self, backup_file: str) -> bool:
        if self._conn is None:
            return False

        bck = sqlite3.connect(backup_file)
        self._conn.backup(bck)
        bck.close()
        return True

    def insert_account_sample(self, account_sample):
        pass

    def update_instrument_list(self, list_of_instruments):
        pass

    def update_instrument(self, instrument_log):
        pass
