import statistics
import os
import pandas as pd

import import_ as imp

NEEDED_COMMENTS = 10                    # statements with less comments will be dropped
COMMENT_RANGE_TO_CONSIDER = 0.90        # in percent


def get_prepared_data(datetime_evaluation: bool = False):
    print("preparing data...")

    # import csv statements
    statements = imp.import_statement_full_data()

    # select only the data needed for the statistic
    statements_statistic = statements[
        ["article_id", "sentimentResult_neg", "sentimentResult_pos", "published_date"]].copy()

    # calculates sum of negative and positive sentiment
    statements_statistic['overall_sentiment'] = statements_statistic["sentimentResult_pos"] + statements_statistic[
        "sentimentResult_neg"]

    # calculate percentage of agreement out of the sentiment
    statements_statistic['statement_opinion_percent'] = (statements_statistic['overall_sentiment'] + 5) / 10

    # import csv comments
    comments = imp.import_comments_full_data()

    # if selected: choose datetime as well
    if datetime_evaluation:
        comments_statistic = comments[
            ["article_id", "comment_id", "sentimentResult_neg", "sentimentResult_pos", "timestamp"]].copy()

        # converting to datetime
        comments_statistic['datetime'] = pd.to_datetime(comments_statistic['timestamp'], unit='ms')

    else:
        comments_statistic = comments[["article_id", 'comment_id', "sentimentResult_neg", "sentimentResult_pos"]].copy()

    # calculates sum of negative and positive sentiment
    comments_statistic['overall_sentiment'] = comments_statistic['sentimentResult_pos'] + comments_statistic[
        'sentimentResult_neg']

    # preparation for combining data
    combined = statements_statistic.copy()
    combined['comments_sentiment'] = 0.0    # init
    combined['comments_agreement'] = 0.0    # init
    combined['SD'] = 0.0                    # standard deviation
    combined['number_of_comments'] = NEEDED_COMMENTS
    combined['duration_of_comments'] = None

    empty_statements = []  # statements with no comments

    for e, row in combined.iterrows():
        # gets current article id
        article_id = row['article_id']

        # selects only comments that belongs to the statement
        comments_for_statement = comments_statistic[comments_statistic['article_id'] == article_id]

        # sorts out empty statements (with out less than the needed comments below a statement)
        if len(comments_for_statement) <= NEEDED_COMMENTS:
            empty_statements.append(e)
            continue
        else:

            # if enabled: evaluates datetime and duration of comments per statement
            if datetime_evaluation:
                min_val = comments_for_statement['datetime'].min()  # get first comment

                # sort dataframe by datetime
                sort = comments_for_statement.sort_values('datetime')

                # get number of valid datetime
                max_val_index = sort['datetime'].count()

                # gets the value at COMMENT_RANGE_TO_CONSIDER as the "max" date value.
                # we did not choose df.max because we wanted to exclude random comments years later.
                almost_max_val = sort.iloc[int(max_val_index * COMMENT_RANGE_TO_CONSIDER)]['datetime']
                # max_val = comments_for_statement['datetime'].max()        # Alternative to Comment range. (like 100%)

                # calculates duration
                #dur = (almost_max_val - min_val).days
                dur_days = (almost_max_val - min_val).days

                #  allow only valid calculations
                if isinstance(dur_days, int):
                    combined.at[e, 'duration_of_comments'] = dur_days

            # gets number of comments for the selected statement
            number_of_comments = comments_for_statement['overall_sentiment'].count()
            combined.at[e, 'number_of_comments'] = number_of_comments

            # sums up all sentiment data of the comments
            comment_sum = comments_for_statement['overall_sentiment'].sum()

            # calculates average sentiment of all comments for the statement and stores it
            intersection = comment_sum / number_of_comments
            combined.at[e, 'comments_sentiment'] = intersection

            # calculate SD for the comments
            combined.at[e, 'SD'] = statistics.stdev(comments_for_statement['overall_sentiment'])

            # calculates percentage of agreement based on comment sentiment and stores it
            combined.at[e, 'comments_agreement'] = (intersection + 5) / 10  # convert possible range: -5..5 to percentage

    # leave the "empty comment rows in to see if there are any relation from the comments to the statement
    combined.drop(empty_statements, inplace=True)

    print("data prepared")
    return combined, empty_statements


def date_import_for_manual_evaluation():
    # import csv statements
    statements = imp.import_statement_full_data()
    return statements


if __name__ == '__main__':
    data, _ = get_prepared_data(datetime_evaluation=True)
    data.to_csv(os.path.abspath("data//prepared_data.csv"))
    print("data saved in csv file")
