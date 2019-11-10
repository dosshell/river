import argparse
import requests
import json
import os
import datetime
import apsw


def get_test_data_fund_list(pages):
    url = 'https://www.avanza.se/_cqbe/fund/list'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-SecurityToken': '-'
    }
    data = {
        "startIndex": 0,
        "indexFund": False,
        "lowCo2": False,
        "regionFilter": [],
        "countryFilter": [],
        "alignmentFilter": [],
        "industryFilter": [],
        "fundTypeFilter": [],
        "interestTypeFilter": [],
        "sortField": "name",
        "sortDirection": "ASCENDING",
        "name": "",
        "recommendedHoldingPeriodFilter": [],
        "companyFilter": []
    }
    response = requests.get(url, headers=headers, data=json.dumps(data))
    if not response.ok:
        return None
    funds_per_page = 20
    number_of_funds = pages * funds_per_page
    funds = {}
    for start_index in range(0, number_of_funds, funds_per_page):
        data['startIndex'] = start_index
        response = requests.get(url, headers=headers, data=json.dumps(data))
        if not response.ok:
            raise ValueError("Connection problems?")
        funds[start_index] = response.json()
        funds[start_index]['totalNoFunds'] = number_of_funds
    return funds


def get_test_data_fund(orderbook_id):
    '''Only support full years for now'''
    url = f'''https://www.avanza.se/_mobile/market/fund/{orderbook_id}'''
    headers = {'User-Agent': 'Avanza API client/1.3.0', 'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.get(url, headers=headers)
    if not response.ok:
        raise ValueError("Connection problems?")
    return response.json()


def get_test_data_fund_chart(orderbook_id, year):
    from_date = datetime.date(year, 1, 1).isoformat()
    to_date = datetime.date(year + 1, 1, 1).isoformat()
    url = f'''https://www.avanza.se/_cqbe/fund/chart/{orderbook_id}/{from_date}/{to_date}'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        raise ValueError("Connection problems?")
    return response.json()


def create_test_db(conn, pages):
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE fund_list(
                orderbook_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                start_date TEXT NOT NULL
            )''')
    data = get_test_data_fund_list(pages)
    a = [item for sublist in data.values() for item in sublist['fundListViews']]
    values = [(x['orderbookId'], x['name'], x['startDate']) for x in a]
    cursor.executemany('insert into fund_list values (?,?,?)', values)


def main(args):
    pages = 4
    funds = [1949]
    years = [2009, 2010, 2011, 2012]

    dir_path = os.path.dirname(os.path.realpath(__file__) + '/data')

    # create/overrite fund_list.json
    fund_list_data = get_test_data_fund_list(pages)
    with open(dir_path + '/fund_list.json', 'w') as f:
        json.dump(fund_list_data, f)

    for orderbook_id in funds:
        fund_data = get_test_data_fund(orderbook_id)
        with open(dir_path + f'''/fund_{orderbook_id}.json''', 'w') as f:
            json.dump(fund_data, f)

    for orderbook_id in funds:
        for year in years:
            chart_data = get_test_data_fund_chart(orderbook_id, year)
            with open(dir_path + f'''/fund_chart_{orderbook_id}_{year}.json''', 'w') as f:
                json.dump(chart_data, f)

    db_path = dir_path + '/test.db'
    if os.path.isfile(db_path):
        os.remove(db_path)
    conn = apsw.Connection(db_path)
    create_test_db(conn, pages)
    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create test data")
    args = parser.parse_args()
    main(args)
