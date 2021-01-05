import statistics

import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats import spearmanr

import data_preparation
import import_ as imp
import pandas as pd


def overall_information(data):
    plt.boxplot(data['overall_sentiment'])
    plt.title("statement opinion positive")
    plt.ylabel("positive neutral and negative report")
    plt.xticks([])
    plt.figtext(.8, .8, "5 = positive\n0 = neutral\n-5 = negative")
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
    data1 = data[['statement_opinion_percent', 'comments_agreement']].sort_values(by='statement_opinion_percent')
    # data2.plot(x='comments_agreement', y='statement_opinion_percent')
    data1.plot(x='statement_opinion_percent', y='comments_agreement', kind='scatter')
    plt.show()
    print("plotted")


def plot_SD_and_comments_agreement(data):
    plt.plot(data['SD'])
    plt.show()

def plot_number_of_comments(data):
    data.sort_values(by='published_date', ascending=False)
    data.plot(x='published_date', y='number_of_comments')
    plt.show()


def plot_time_in_between(data):  # TODO not working jet

    data['time_in_between'] = None
    for e, row in data.iterrows():
        start = row['comments']['datetime'].min()
        end = row['comments']['datetime'].max()
        data = end - start
        row['time_in_between'] = data


if __name__ == '__main__':
    # Options:
    # 0 ... csv import
    # 1 ... data with time

    option = 0
    statement_with_no_comment = False

    if option == 0:
        data = imp.import_prepared_data()
        empty_statements = []
    elif option == 1:
        data, empty_statements = data_preparation.get_prepared_data(full_comments=True)
    else:
        raise Exception('not a valid option')

    if statement_with_no_comment:
        if option == 0:
            print("not possible to drop statement with no comment, by csv import")
        data.drop(empty_statements, inplace=True)

    #data.sort_values(by='published_date')
    #overall_information(data)
    #correlation_statement_and_comment(data)
    #plot_correlation(data)
    #plot_SD_and_comments_agreement(data)
    #plot_number_of_comments(data)
    single_values(data)
    # plot_time_in_between(data)
