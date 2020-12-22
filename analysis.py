import import_ as imp

data = imp.importCSV("data/fullData.csv")

for e, row in data.iterrows():
    print(row['comments'])