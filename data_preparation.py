import math
import statistics
from datetime import datetime
import os
import pandas as pd

import import_ as imp


def get_prepared_data(full_comments: bool = False):
    print("preparing data...")

    # import csv statements
    statements = imp.import_statement_full_data()

    # select only the data needed for the statistic
    statements_statistic = statements[["article_id", "sentimentResult_neg", "sentimentResult_pos", "published_date"]].copy()

    # calculates sum of negative and positive sentiment
    statements_statistic['overall_sentiment'] = statements_statistic["sentimentResult_pos"] + statements_statistic[
        "sentimentResult_neg"]

    statements_statistic['statement_opinion_percent'] = (statements_statistic['overall_sentiment'] + 5) / 10

    # import csv comments
    comments = imp.import_comments_full_data()

    # select only the data needed for the statistic
    if full_comments:
        comments_statistic = comments[
            ["article_id", "comment_id", "sentimentResult_neg", "sentimentResult_pos", "timestamp"]].copy()
        comments_statistic['datetime'] = datetime
        cur_oldest_comment = datetime()
        cur_newes_comment = datetime()
        for e, row in comments_statistic.iterrows():
            date_f = row['timestamp'] / 1000  # other format
            if not math.isnan(date_f):
                test = pd.to_datetime(datetime.fromtimestamp(date_f).isoformat())
                row['datetime'] = test
            else:
                row['datetime'] = None
        min = comments_statistic['datetime'].min
        max= comments_statistic['datetime'].max()
        dur = min - max
        comments_statistic['duration_of_comments'] = dur

    else:
        comments_statistic = comments[["article_id", 'comment_id', "sentimentResult_neg", "sentimentResult_pos"]].copy()

    # calculates sum of negative and positive sentiment
    comments_statistic['overall_sentiment'] = comments_statistic['sentimentResult_pos'] + comments_statistic[
        'sentimentResult_neg']

    # preparation for combining data
    combined = statements_statistic.copy()
    combined['comments_sentiment'] = 0.0
    combined['comments_agreement'] = 0.0
    combined['SD'] = 0.0  # standard deviation
    combined['number_of_comments'] = 10
    if full_comments:
        combined['comments'] = None

    empty_statements = []  # statements with no comments

    for e, row in combined.iterrows():
        # gets current article id
        article_id = row['article_id']

        # selects only comments that belongs to the statement
        comments_for_statement = comments_statistic[comments_statistic['article_id'] == article_id]

        # sorts out empty statements (with out any comment under the statement)
        if len(comments_for_statement) <= 10:
            empty_statements.append(e)
            continue
        else:
            combined.at[e, 'SD'] = statistics.stdev(comments_for_statement['overall_sentiment'])  # calculate SD

        if full_comments:
            combined.at[e, 'comments'] = comments_for_statement

        # gets number of comments for the selected statement
        number_of_comments = comments_for_statement['overall_sentiment'].count()
        combined.at[e, 'number_of_comments'] = number_of_comments

        # sums up all sentiment data of the comments
        comment_sum = comments_for_statement['overall_sentiment'].sum()

        # calculates average sentiment of all comments for the statement and stores it
        intersection = comment_sum / number_of_comments
        combined.at[e, 'comments_sentiment'] = intersection

        # calculates percentage of agreement based on comment sentiment and stores it
        combined.at[e, 'comments_agreement'] = (intersection + 5) / 10  # convert possible range: -5..5 to percentage

    # leave the "empty comment rows in to see if there are any relation from the comments to the statement
    combined.drop(empty_statements, inplace=True)

    print("data prepared")
    return combined, empty_statements


if __name__ == '__main__':
    data, _ = get_prepared_data()
    data.to_csv(os.path.abspath("data//prepared_data.csv"))
    print("data saved in csv file")
