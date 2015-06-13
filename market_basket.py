#!/usr/bin/env python3
# Market basket python program

import csv

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
    count = 1

    for order in orders[1:]:
        if item_set.issubset(order):
            #print("Found {} in {}".format(item_set, order))
            count += 1
        else:
            #print("Didn't find {} in {}".format(item_set, order))
            pass
    return count

def support_frequency(orders, item_set):
    N = len(orders)
    return support_count(orders, item_set)/float(N)

def confidence(orders, left, right):
    left_count = support_count(orders, left)
    right = right.union(left)
    right_count = support_count(orders, right)
    result = right_count/left_count
    return result

def apriori(orders, support_threshold):
    #frequency_list1 = list()
    N = len(orders[1:])

    inventory_list = orders[0]  #inventory_list is the header of the csv file
    print('Inventory List: \n' + str(inventory_list) + '\n')

    test_set = orders
    transaction = test_set.pop()

    candidate_set = set()

    while (inventory_list): # count support for each item in inventory list
        unique_item = inventory_list.pop()

        candidate_set.add(unique_item)

        temp_set = set()
        temp_set.add(unique_item)

        s = support_frequency(orders, temp_set)

        if (s < support_threshold):
            print(unique_item + ' ' + str(s) + " does not meet threshold ")
            candidate_set.remove(unique_item)
        else:
            print(unique_item + ' ' + str(s) + " meets threshold ")
    pass

    print ('\nCandidate Set: \n' + str(candidate_set))




def main():
    data = read_CSV('market_basket.csv')
   # item_set = set(['Eggs','Bread'])
   # item_set2 = set(['Spinach'])
   # print(support_frequency(data, item_set))
   # print(confidence(data, item_set, item_set2))



    apriori(data, .3)


if __name__ == '__main__':
    main()
