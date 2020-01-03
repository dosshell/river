import argparse
import requests
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/data'


def create_fund_list_data(fund_filter):
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

    with open(dir_path + '/fund_list.json', 'w') as f:
        json.dump(data, f)


def create_fund_data(orderbook_id):
    '''Only support full years for now'''
    url = f'''https://www.avanza.se/_mobile/market/fund/{orderbook_id}'''
    headers = {'User-Agent': 'Avanza API client/1.3.0', 'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.get(url, headers=headers)
    if not response.ok:
        raise ValueError("Connection problems?")

    with open(dir_path + f"""/fund_{orderbook_id}.json""", 'w') as f:
        json.dump(response.json(), f)


def create_fund_chart_data(orderbook_id, start_date, stop_date):
    url = f'''https://www.avanza.se/_cqbe/fund/chart/{orderbook_id}/{start_date}/{stop_date}'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        raise ValueError("Connection problems?")

    with open(dir_path + f"""/fund_chart_{orderbook_id}_{start_date}_{stop_date}.json""", 'w') as f:
        json.dump(response.json(), f)


def main(args):
    funds = [377804, 944976]

    create_fund_list_data(funds)

    for n in funds:
        create_fund_data(n)

    # test_fetch_instrument_chart
    create_fund_chart_data(377804, "1900-01-01", "2019-12-28")
    create_fund_chart_data(377804, "2012-04-04", "2013-03-30")
    create_fund_chart_data(377804, "2012-10-10", "2012-10-10")
    create_fund_chart_data(377804, "2012-10-11", "2013-10-06")
    create_fund_chart_data(377804, "2013-10-07", "2014-10-02")
    create_fund_chart_data(377804, "2014-10-03", "2015-09-28")
    create_fund_chart_data(377804, "2015-09-29", "2016-09-23")
    create_fund_chart_data(377804, "2016-09-24", "2017-09-19")
    create_fund_chart_data(377804, "2017-09-20", "2018-09-15")
    create_fund_chart_data(377804, "2018-09-16", "2019-09-11")
    create_fund_chart_data(377804, "2019-09-12", "2019-12-28")

    create_fund_chart_data(944976, "1900-01-01", "2019-12-28")
    create_fund_chart_data(944976, "2018-09-02", "2019-08-28")
    create_fund_chart_data(944976, "2019-03-26", "2019-03-26")
    create_fund_chart_data(944976, "2019-03-27", "2019-12-28")

    # test_fetch_instrument_chart: partial append test
    create_fund_chart_data(377804, "2018-09-16", "2018-09-24")
    create_fund_chart_data(377804, "2018-09-25", "2019-09-20")
    create_fund_chart_data(377804, "2019-09-21", "2019-12-28")

    # test_fetch_instrument: empty append
    create_fund_chart_data(377804, "2019-12-28", "2019-12-29")

    # test_aquire_start_date
    create_fund_chart_data(32, "1900-01-01", "2019-12-28")
    create_fund_chart_data(32, "1998-06-04", "1999-05-30")
    create_fund_chart_data(35, "1900-01-01", "2019-12-28")
    create_fund_chart_data(35, "1993-07-05", "1994-06-30")
    create_fund_chart_data(38, "1900-01-01", "2019-12-28")
    create_fund_chart_data(38, "1997-10-03", "1998-09-28")
    create_fund_chart_data(351, "1900-01-01", "2019-12-28")
    create_fund_chart_data(351, "2015-06-04", "2016-05-29")

    # test append_fund_chart
    create_fund_chart_data(377804, "2012-10-20", "2013-10-15")
    create_fund_chart_data(377804, "2013-10-16", "2014-10-11")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create test data")
    args = parser.parse_args()
    main(args)
