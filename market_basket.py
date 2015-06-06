#!/usr/bin/env python3
# Market basket python program

import csv



print("Hello world")

def read_CSV(file_name):

    result = list()
    with open(file_name, 'r') as csv_file:
        file_reader = csv.reader(csv_file)
        for row in file_reader:
            order_set = set(row)-set(['0'])
            result.append(order_set)
    # print(result)
    return result


def support_count(orders, item_set):
    count = 0

    for order in orders[1:]:

        if item_set.issubset(order):
            print("Found {} in {}".format(item_set, order))
            count += 1
        else:
            print("Didn't find {} in {}".format(item_set, order))


    return count

# def support_frequency(sums_of_items, total_items):
#     #support_frequency_list = list()
#     #for x in sums_of_items
#     pass

def main():
    data = read_CSV('market_basket.csv')
    item_set = set(['Eggs','Bread','Bananas'])
    print(support_count(data, item_set))


if __name__ == '__main__':
    main()
