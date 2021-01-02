import io

import pandas as pd

import import_ as imp


def get_prepared_data():
    # import csv statements
    statements = imp.import_statement_full_data()

    # select only the data needed for the statistic
    statements_statistic = statements[["article_id", "sentimentResult_neg", "sentimentResult_pos"]].copy()

    # calculates sum of negative and positive sentiment
    statements_statistic['overall_sentiment'] = statements_statistic["sentimentResult_pos"] + statements_statistic[
        "sentimentResult_neg"]

    # import csv comments
    comments = imp.import_comments_full_data()

    # select only the data needed for the statistic
    comments_statistic = comments[["article_id", 'comment_id', "sentimentResult_neg", "sentimentResult_pos"]].copy()

    # calculates sum of negative and positive sentiment
    comments_statistic['overall_sentiment'] = comments_statistic['sentimentResult_pos'] + comments_statistic[
        'sentimentResult_neg']

    # preparation for combining data
    combined = statements_statistic.copy()
    combined['comments_sentiment'] = 0.0
    combined['comments_agreement'] = 0.0
    # combined['comments'] = None

    empty_statements = []  # statements with no comments

    for e, row in combined.iterrows():
        # gets current article id
        article_id = row['article_id']

        # selects only comments that belongs to the statement
        comments_for_statement = comments_statistic[comments_statistic['article_id'] == article_id]

        # sorts out empty statements (with out any comment under the statement)
        if len(comments_for_statement) == 0:
            empty_statements.append(e)
            continue

        # combined.at[e, 'comments'] = comments_for_statement       # TODO: if needed for further evaluation

        # gets number of comments for the selected statement
        number_of_comments = comments_for_statement['overall_sentiment'].count()

        # sums up all sentiment data of the comments
        comment_sum = comments_for_statement['overall_sentiment'].sum()

        # calculates average sentiment of all comments for the statement and stores it
        sentiment_sum = comment_sum / number_of_comments
        combined.at[e, 'comments_sentiment'] = sentiment_sum

        # calculates percentage of agreement based on comment sentiment and stores it
        combined.at[e, 'comments_agreement'] = (sentiment_sum + 5) / 10  # possible range: -5..5

    # leave the "empty comment rows in to see if there are any relation from the comments to the statement
    # combined.drop(combined.index[], inplace=True)

    return combined, empty_statements
