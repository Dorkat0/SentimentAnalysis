import io

import pandas as pd

import import_ as imp


def only_statistics(data: pd.DataFrame):
    statistic_data = data[["article_id", "sentimentResult_neg", "sentimentResult_pos", "comments"]]
    #statistic_data["comments"] = statistic_data["comments"][["article_id", "comment_id", "sentimentResult_neg", "sentimentResult_pos"]]

    for e, row in statistic_data.iterrows():
        co = row['comments']
        com = io.StringIO(co)
        comm = pd.read_csv(com, error_bad_lines=False)

        row['comments'] = comm


    return statistic_data


data = imp.importFullData()
statistic_data_test = only_statistics(data)
print(statistic_data_test)
