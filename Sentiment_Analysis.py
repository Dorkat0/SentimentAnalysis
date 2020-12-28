import concurrent.futures
import threading
from datetime import datetime
import os

import import_ as imp
from sentistrength import PySentiStr
import pandas as pd


def get_sentiment_statement(data: pd.DataFrame, fr, to):
    for e, row in data[fr:to].iterrows():
        text = row['article_text']
        val = se.getSentiment(text, score='dual')
        # comment_sum = sum(list(val))
        #if len(val) > 1:


        data.at[e, 'sentimentResult_pos'], data.at[e, 'sentimentResult_neg'] = val[0]
    print("TBE: add sum" + str(fr) + ":" +str(to))


se = PySentiStr()
path = os.path.abspath("SentiStrength.jar")
se.setSentiStrengthPath(path)
se.setSentiStrengthLanguageFolderPath(os.path.abspath("SentStrength_Data_Sept2011"))



#threadNumber = 20
#number_per_thread = round(number_of_statements / threadNumber)
#nr = 0

#with concurrent.futures.ThreadPoolExecutor(max_workers=threadNumber) as executor:
#    executor.map(get_sentiment_statement, statement)
#threads = []

#for i in range(threadNumber):
#    thread = threading.Thread(target=get_sentiment_statement, args=(statement, nr, number_per_thread))
#    nr += number_per_thread
#    thread.start()
#    threads.append(thread)

#for i in threads:
#    i.join()



#print("finished thread statements")



# statement = statement.head(20)          # TODO comment for howl dataset


statement = imp.importCSV("data/SOCC/raw/gnm_articles.csv")
statement['sentimentResult_pos'] = 0
statement['sentimentResult_neg'] = 0

statement = statement.head(50)          # TODO comment for howl dataset


number_of_statements = statement['article_id'].count()

print("stated...")
print(str(number_of_statements) + " statements")
start_time = datetime.now()
print("stated at: " + str(start_time))

iteration = 0
for e, row in statement.iterrows():
    text = row['article_text']
    val = se.getSentiment(text, score='dual')
    # comment_sum = sum(list(val))
    if len(val) > 1:
        print("TBE: add sum")


    statement.at[e, 'sentimentResult_pos'], statement.at[e, 'sentimentResult_neg'] = val[0]
    # e[1]['sentimentResult'] = comment_sum

    iteration = iteration + 1
    if iteration > 5000:
        print("next 5.000")
        iteration = 0

print("statement done")

statement.to_csv(os.path.abspath("data//analysed_statement.csv"))
end_time = datetime.now()
print("ended at: " + str(end_time))
print("duration: " + str((end_time - start_time)))




comment = imp.importCSV("data/SOCC/raw/gnm_comments.csv")
comment['sentimentResult_pos'] = 0
comment['sentimentResult_neg'] = 0

comment = comment.head(20)          # TODO comment for howl dataset

number_of_comments = comment['comment_id'].count()
print(str(number_of_comments) + " comments")
start_time = datetime.now()
print("stated at: " + str(start_time))

iteration = 0
for e, row in comment.iterrows():
    text = row['comment_text']
    val = se.getSentiment(text, score='dual')
    # comment_sum = sum(list(val))
    if len(val) > 1:
        print("TBE: edit sum")

    comment.at[e, 'sentimentResult_pos'], comment.at[e, 'sentimentResult_neg'] = val[0]
    # e[1]['sentimentResult'] = comment_sum

    iteration = iteration + 1
    if iteration > 5000:
        print("next 5.000")
        iteration = 0
    # print('added comment')

print("comments done")
comment.to_csv(os.path.abspath("data//analysed_comments.csv"))
end_time = datetime.now()
print("ended at: " + str(end_time))
print("duration: " + str(end_time - end_time))


print("create combination")
start_time = datetime.now()
print("stated at: " + str(start_time))

iteration = 0
statement['comments'] = None
for e, row in statement.iterrows():
    article_id = row['article_id']  # TODO remove comment
    # article_id = 10012655              # TODO comment
    statement.at[e, 'comments'] = comment[comment['article_id'] == article_id]
    # print(statement.at[e, 'comments'])
    iteration = iteration + 1
    if iteration > 5000:
        print("next 5.000")
        iteration = 0

print("Combined")
end_time = datetime.now()
print("ended at: " + str(end_time))
print("duration: " + str(end_time - end_time))

statement.to_csv(os.path.abspath("data//fullData.csv"))
print("Done")
