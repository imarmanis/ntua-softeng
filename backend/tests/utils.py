from collections import Counter
from datetime import datetime


def url_for(path):
    return '/observatory/api' + path


def auth_header(token):
    return {
        'X-OBSERVATORY-AUTH': token
    }


def valid_response(real_data, json):
    for attr in real_data.keys():
        if isinstance(real_data[attr], list):
            assert Counter(real_data[attr]) == Counter(json[attr])
        else:
            assert real_data[attr] == json[attr]


def str_to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()
