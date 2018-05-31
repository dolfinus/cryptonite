from transliterate import slugify
from datetime import date, datetime
try:
    from urllib.parse import urlencode, unquote
except ImportError:
    from urllib import urlencode, unquote

def get_id(name):
    return slugify(unquote(name)) or unquote(name).lower().replace(' ','-')

def encode_datetime(dict):
    for field, value in dict.items():
        if isinstance(value, (date, datetime)):
            dict[field] = dict[field].isoformat()
    return dict

def divide_dict(dict_, names):
    eq     = {}
    non_eq = {}
    for key, value in dict_.items():
        if isinstance(names, str):
            if key == names:
                eq = value
            else:
                non_eq[key] = value
        else:
            if key in names:
                eq[key] = value
            else:
                non_eq[key] = value

    return eq, non_eq

def strip_spaces(str):
    return str.replace('\n','').replace('\r', '').strip()

def unmask(str):
    return str.replace('[x]','[ ]').replace('[X]','[ ]').replace('[*]','[ ]').replace('(*)','( )')

def current_second():
    return datetime.utcnow().replace(microsecond=0)

class Format:
    RAW  = 1
    DICT = 2
    JSON = 4