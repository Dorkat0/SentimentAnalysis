import os

import import_ as imp
from sentistrength import PySentiStr
import pandas as pd

se = PySentiStr()
path = os.path.abspath("SentiStrength.jar")
se.setSentiStrengthPath(path)
se.setSentiStrengthLanguageFolderPath(os.path.abspath("SentStrength_Data_Sept2011"))

statement = imp.importCSV("data/SOCC/raw/gnm_articles.csv")
statement['sentimentResult_pos'] = 0
statement['sentimentResult_neg'] = 0

number_of_statements = statement.count()

# statement = statement.head(20)          # TODO comment for howl dataset

print("stated...")
print(number_of_statements + " statements")

iteration = 0
for e, row in statement.iterrows():
    test = row['article_text']
    val = se.getSentiment(test, score='dual')
    # comment_sum = sum(list(val))
    if len(val) > 1:
        print("TBE: add sum")


    statement.at[e, 'sentimentResult_pos'], statement.at[e, 'sentimentResult_neg'] = val[0]
    # e[1]['sentimentResult'] = comment_sum

    iteration = iteration + 1
    if iteration > 10000:
        print("next 10.000")
        iteration = 0

print("statement done")

comment = imp.importCSV("data/SOCC/raw/gnm_comments.csv")
comment['sentimentResult_pos'] = 0
comment['sentimentResult_neg'] = 0

# comment = comment.head(20)          # TODO comment for howl dataset

number_of_comments = comment.count()
print(number_of_comments + " statements")

iteration = 0
for e, row in comment.iterrows():
    test = row['comment_text']
    val = se.getSentiment(test, score='dual')
    # comment_sum = sum(list(val))
    if len(val) > 1:
        print("TBE: edit sum")

    comment.at[e, 'sentimentResult_pos'], comment.at[e, 'sentimentResult_neg'] = val[0]
    # e[1]['sentimentResult'] = comment_sum

    iteration = iteration + 1
    if iteration > 10000:
        print("next 10.000")
        iteration = 0
    # print('added comment')

print("comments done")

print("create combination")
iteration = 0
statement['comments'] = None
for e, row in statement.iterrows():
    article_id = row['article_id']  # TODO remove comment
    # article_id = 10012655              # TODO comment
    statement.at[e, 'comments'] = comment[comment['article_id'] == article_id]
    # print(statement.at[e, 'comments'])
    iteration = iteration + 1
    if iteration > 10000:
        print("next 10.000")
        iteration = 0

print("Combined")

statement.to_csv(os.path.abspath("data//fullData.csv"))
print("Done")
