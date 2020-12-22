import os

import pandas as pd

def importCSV(relativPath):
    path = os.path.abspath(relativPath)
    imp = pd.read_csv(path, sep=",")

    return imp

