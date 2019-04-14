import sqlite3
import avanza


def update(avanza_client: avanza.Avanza):
    if (not avanza_client.is_authed):
        print('No avanza connection')
        return None

    overview = avanza_client.get_overview()
    accounts = [(x['accountId'], x['accountType'], str(x['depositable'])) for x in overview['accounts']]
    balance = [(x['accountId'], x['ownCapital']) for x in overview['accounts']]

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Create structure
    c.execute('''CREATE TABLE IF NOT EXISTS
                 account (
                   account_id NOT NULL PRIMARY KEY,
                   account_type,
                   depositable
                 )
          ''')

    c.execute('''CREATE TABLE IF NOT EXISTS
                 balance (
                   account_id,
                   total_balance,
                   datetime,
                   FOREIGN KEY(account_id) REFERENCES account(account_id)
                 )
          ''')

    # Store data
    c.executemany('''INSERT OR IGNORE INTO account VALUES (?, ?, ?)''', accounts)
    c.executemany('''INSERT INTO balance VALUES (?, ?, datetime('now'))''', balance)

    conn.commit()

    conn.close()

    return True
