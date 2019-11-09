import argparse
import requests
import json
import os


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


def main(args):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # create/overrite fund_list.json
    fund_list_data = get_test_data_fund_list(4)
    with open(dir_path + '/fund_list.json', 'w') as f:
        json.dump(fund_list_data, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create test data")
    args = parser.parse_args()
    main(args)
