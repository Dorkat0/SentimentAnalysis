import statistics
import datetime

import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats import spearmanr
import data_preparation
import import_ as imp


def overall_information(data):
    plt.boxplot(data['overall_sentiment'])
    plt.title("statement opinion positive")
    plt.ylabel("positive neutral and negative report")
    plt.xticks([])
    plt.figtext(.8, .8, "5 = positive\n0 = neutral\n-5 = negative")
    plt.ylim([-5, +5])
    plt.show()
    plt.boxplot(data['comments_agreement'] * 100)
    plt.title("comment agreement")
    plt.ylabel("agreement (in %)")
    plt.xticks([])
    plt.show()
    print("plotted")


def single_values(data):
    com_med_agree = statistics.median(data['comments_agreement'] * 100)
    print("Median of the comment agreement: {:.2f}".format(com_med_agree))

    SD_mean = statistics.mean(data['SD'])
    print("Median of the comment agreement: {:.2f}".format(SD_mean))

    average_discussion_days = data['duration_of_comments'].sum() / data['duration_of_comments'].count()
    print("The average discussion time was {:.0f} days".format(average_discussion_days))

    average_received_comments = statistics.mean(data['number_of_comments'])
    print("In average a statement receives {:.0f} comments".format(average_received_comments))


def correlation_statement_and_comment(data):
    pers = pearsonr(data['statement_opinion_percent'], data['comments_agreement'])
    print("The pearson correlation coefficient is {:.3f} and the p-value is {:.3f}".format(pers[0], pers[1]))
    if pers[1] > 0.05:
        print("the p-value is higher than 0.05, therefore there is no statistically significant correlation")
    else:
        print("The p-value is lower than 0.05, therefore there is an statistically significant correlation")

    sp = spearmanr(data['statement_opinion_percent'], data['comments_agreement'])
    print("The Spearmans correlation coefficient is {:.3f} and the p-value is {:.10f}".format(sp[0], sp[1]))
    if sp[1] > 0.05:
        print("the p-value is higher than 0.05, therefore there is no statistically significant correlation")
    else:
        print("The p-value is lower than 0.05, therefore there is an statistically significant correlation")


def plot_correlation(data):
    data1 = data[['overall_sentiment', 'comments_agreement']].sort_values(by='overall_sentiment')
    data1.plot(x='overall_sentiment', y='comments_agreement', kind='scatter')
    plt.xlabel("statement sentiment")
    plt.ylabel("agreement by comments")
    plt.show()
    print("plotted")


def plot_SD_and_comments_agreement(data):
    data.plot(x='published_date', y='SD')
    plt.xlim([datetime.datetime(2013, 1, 1), datetime.datetime(2016, 12, 31)])
    plt.show()


def plot_number_of_comments(data):
    data.sort_values(by='published_date', ascending=False)
    data.plot(x='published_date', y='number_of_comments')
    plt.xlim([datetime.datetime(2013, 1, 1), datetime.datetime(2016, 12, 31)])
    plt.xlabel("publish date")
    plt.ylabel("number of comments")
    plt.show()


def plot_time_in_between(data):
    data.plot(y='duration_of_comments', x='published_date')
    plt.xlim([datetime.datetime(2013, 1, 1), datetime.datetime(2016, 12, 31)])
    plt.ylim([0, 700])
    plt.xlabel("date of publications")
    plt.ylabel("days of discussion")
    plt.show()


def manual(data):
    full_data = data_preparation.date_import_for_manual_evaluation()

    # max_val = data.at[data['number_of_comments'].argmax(), 'article_id']
    # print("wanted article id: {:.0f}".format(max_val))

    max_val = data.at[data['duration_of_comments'].argmax(), 'article_id']
    print("wanted article id: {:.0f}".format(max_val))
    statement = full_data.loc[full_data['article_id'] == max_val]
    print(statement)


if __name__ == '__main__':
    data = imp.import_prepared_data()

    data.sort_values(by='published_date')

    #single_values(data)
    #overall_information(data)
    #plot_SD_and_comments_agreement(data)
    #correlation_statement_and_comment(data)
    #plot_correlation(data)
    #plot_number_of_comments(data)
    #plot_time_in_between(data)
    #manual(data)
