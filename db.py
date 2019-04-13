import sqlite3
import avanza


def update(avanza_client: avanza.Avanza):
    if (not avanza_client.is_authed):
        print('No avanza connection')
        return None

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
        id NOT NULL PRIMARY KEY,
        account_type TEXT,
        depositable)
        ''')

    overview = avanza_client.get_overview()

    v = [(x['accountId'], x['accountType'], str(x['depositable'])) for x in overview['accounts']]
    print(v)
    c.executemany('''INSERT OR IGNORE INTO accounts VALUES (?, ?, ?)''', v)

    conn.commit()
    conn.close()

    return True
