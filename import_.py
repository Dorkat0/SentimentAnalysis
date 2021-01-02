import os
import pandas as pd


def import_csv(relative_path, typ=None):
    path = os.path.abspath(relative_path)
    if typ is not None:
        imp = pd.read_csv(path, sep=",", low_memory=False,  dtype=typ)
    else:
        imp = pd.read_csv(path, sep=",")

    return imp


def import_full_data():
    return import_csv("data/fullData.csv")


def import_statement_full_data():
    return import_csv("data/analysed_statement.csv")


def import_comments_full_data():
    typ = {'vote': str, 'reactions': str}
    return import_csv("data/analysed_comments.csv", typ)
