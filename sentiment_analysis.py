from datetime import datetime
import os

import import_ as imp
from sentistrength import PySentiStr

"""Note: multithreading did not work"""

# initialize SentiStrengh
se = PySentiStr()
path = os.path.abspath("SentiStrength.jar")
se.setSentiStrengthPath(path)
se.setSentiStrengthLanguageFolderPath(os.path.abspath("SentStrength_Data_Sept2011"))

# imports raw data of statement
statement = imp.import_csv("data/SOCC/raw/gnm_articles.csv")

statement = statement.head(50)          # TODO comment for howl dataset

# number of statements
number_of_statements = statement['article_id'].count()

# information for terminal
print("stated...")
print(str(number_of_statements) + " statements")
start_time = datetime.now()
print("stated at: " + str(start_time))

# preparation
statement['sentimentResult_pos'] = 0
statement['sentimentResult_neg'] = 0
iteration = 0
for e, row in statement.iterrows():
    # statement text for analysing
    text = row['article_text']
    #text = "I love you but hate the current political climate."

    # run SentiStrengh
    result = se.getSentiment(text, score='dual')

    # adds sentiment result to dataframe
    statement.at[e, 'sentimentResult_pos'], statement.at[e, 'sentimentResult_neg'] = result[0]

    # information for terminal
    iteration = iteration + 1
    if iteration > 5000:
        print("next 5.000")
        iteration = 0

print("statement done")

# store result in csv file
statement.to_csv(os.path.abspath("data//analysed_statement.csv"))
end_time = datetime.now()
print("ended at: " + str(end_time))
print("duration: " + str((end_time - start_time)))



# imports raw data of comments
comment = imp.import_csv("data/SOCC/raw/gnm_comments.csv")

comment = comment.head(20)          # TODO comment for howl dataset

# number of statements
number_of_comments = comment['comment_id'].count()

# information for terminal
print(str(number_of_comments) + " comments")
start_time = datetime.now()
print("stated at: " + str(start_time))

# preparation
comment['sentimentResult_pos'] = 0
comment['sentimentResult_neg'] = 0
iteration = 0
for e, row in comment.iterrows():
    # comment text for analysing
    text = row['comment_text']

    # run SentiStrengh
    result = se.getSentiment(text, score='dual')

    # adds sentiment result to dataframe
    comment.at[e, 'sentimentResult_pos'], comment.at[e, 'sentimentResult_neg'] = result[0]

    # information for terminal
    iteration = iteration + 1
    if iteration > 5000:
        print("next 5.000")
        iteration = 0

print("comments done")
comment.to_csv(os.path.abspath("data//analysed_comments.csv"))
end_time = datetime.now()
print("ended at: " + str(end_time))
print("duration: " + str(end_time - end_time))


# combines statement and comment

# terminal information
print("create combination")
start_time = datetime.now()
print("stated at: " + str(start_time))

# preparation
iteration = 0
statement['comments'] = None
for e, row in statement.iterrows():
    # get statement_id
    article_id = row['article_id']

    # saves only comments underneath the specific statement
    statement.at[e, 'comments'] = comment[comment['article_id'] == article_id]

    # terminal information
    iteration = iteration + 1
    if iteration > 5000:
        print("next 5.000")
        iteration = 0

print("Combined")
end_time = datetime.now()
print("ended at: " + str(end_time))
print("duration: " + str(end_time - end_time))

# save result       #Fixme did not work as needed.
statement.to_csv(os.path.abspath("data//fullData.csv"))
print("Done")
