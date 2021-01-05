import re
from datetime import datetime, time
import os
import pandas as pd
from pandas.tests.scalar import timestamp


def import_csv(relative_path, low_mem=False, typ=None):
    path = os.path.abspath(relative_path)
    if typ is not None:
        imp = pd.read_csv(path, sep=",", low_memory=low_mem, dtype=typ)
    else:
        imp = pd.read_csv(path, sep=",")

    return imp


def import_full_data():
    return import_csv("data/fullData.csv")


def import_statement_full_data():
    return import_csv("data/analysed_statement.csv")


def import_comments_full_data():
    typ = {'vote': str, 'reactions': str, 'timestamp': float}
    return import_csv("data/analysed_comments.csv", False, typ)


def import_prepared_data():
    path = "data//prepared_data.csv"
    pattern = re.compile("(EST|EDT)")
    custom_date_parser = lambda x: datetime.strptime(pattern.sub("", x), "%Y-%m-%d ")
    imp = pd.read_csv(path, sep=",", parse_dates=['published_date'], date_parser=custom_date_parser)
    return imp