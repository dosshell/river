import argparse
import requests
import json
import os
import datetime
import apsw
from db_utils_link import db_utils


def get_test_data_fund_list(fund_filter):
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
        raise ValueError("Connection problems?")
    data = response.json()
    number_of_funds = data['totalNoFunds']

    data['totalNoFunds'] = len(fund_filter)
    data['fundListViews'] = []

    for start_index in range(0, number_of_funds, 20):
        data['startIndex'] = start_index
        response = requests.get(url, headers=headers, data=json.dumps(data))
        if not response.ok:
            raise ValueError("Connection problems?")
        r = response.json()
        new_funds = [x for x in r['fundListViews'] if x['orderbookId'] in fund_filter]
        data['fundListViews'].extend(new_funds)
    return data


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


def create_test_db(conn, fund_list_data, chart_datas):
    with conn:
        cursor = conn.cursor()
        db_utils.create_tables(cursor)

        # Populate with real data from created json files
        values = [(x['orderbookId'], x['name'], x['startDate']) for x in fund_list_data['fundListViews']]
        cursor.executemany('insert into fund_list values (?,?,?)', values)
        for fund, data in chart_datas.items():
            pfix = 1.0
            for d in data:
                rows = [(fund, datetime.datetime.utcfromtimestamp(x['x'] / 1000).isoformat(), (x['y'] / 100 + 1) * pfix)
                        for x in d['dataSerie'] if x['y'] is not None]
                pfix = rows[-1][2]
                cursor.executemany('insert into fund_chart values(?,?,?)', rows)


def main(args):
    funds = [944976, 377804]

    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/data'

    # create/overrite fund_list.json
    fund_list_data = get_test_data_fund_list(funds)
    with open(dir_path + '/fund_list.json', 'w') as f:
        json.dump(fund_list_data, f)

    fund_chart_datas = {}
    for orderbook_id in funds:
        fund_data = get_test_data_fund(orderbook_id)
        with open(dir_path + f'''/fund_{orderbook_id}.json''', 'w') as f:
            json.dump(fund_data, f)

        from_year = int(fund_data['startDate'].split('-')[0])
        to_year = datetime.date.today().year + 1
        fund_chart_datas[orderbook_id] = []
        for year in range(from_year, to_year):
            chart_data = get_test_data_fund_chart(orderbook_id, year)
            fund_chart_datas[orderbook_id].append(chart_data)
            with open(dir_path + f'''/fund_chart_{orderbook_id}_{year}.json''', 'w') as f:
                json.dump(chart_data, f)

    # populate with test data
    db_path = dir_path + '/test.db'
    if os.path.isfile(db_path):
        os.remove(db_path)
    conn = apsw.Connection(db_path)
    create_test_db(conn, fund_list_data, fund_chart_datas)
    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create test data")
    args = parser.parse_args()
    main(args)
