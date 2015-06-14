#!/usr/bin/env python3
"""Market basket python program."""

import csv
import itertools


def read_CSV(file_name):
    """TODO: Insert docstring here."""
    result = list()
    with open(file_name, 'r') as csv_file:
        file_reader = csv.reader(csv_file)
        for row in file_reader:
            order_set = set(row)-set(['0'])
            result.append(order_set)
    # print(result)
    return result


def support_count(orders, item_set):
    """TODO: Insert docstring here."""
    count = 1

    for order in orders[1:]:
        if item_set.issubset(order):
            # print("Found {} in {}".format(item_set, order))
            count += 1
        else:
            # print("Didn't find {} in {}".format(item_set, order))
            pass
    return count


def support_frequency(orders, item_set):
    """TODO: Insert docstring here."""
    N = len(orders)
    return support_count(orders, item_set)/float(N)


def confidence(orders, left, right):
    """TODO: Insert docstring here."""
    left_count = support_count(orders, left)
    right = right.union(left)
    right_count = support_count(orders, right)
    result = right_count/left_count
    return result


def generate_candidate_set(orders, inventory_list, support_threshold):
    """TODO: Insert docstring here."""
    candidate_set = set()
    while (inventory_list):
        # find frequent item sets, save in candidate_set
        unique_item = inventory_list.pop()

        candidate_set.add(unique_item)

        temp_set = set()
        temp_set.add(unique_item)

        s = support_frequency(orders, temp_set)

        if (s < support_threshold):
            print(
                str(unique_item) + ' ' + str(s) + " does not meet threshold ")
            candidate_set.remove(unique_item)
        else:
            print(str(unique_item) + ' ' + str(s) + " meets threshold ")
    pass

    # print ('\nCandidate Set: \n' + str(candidate_set))
    return candidate_set


def apriori(orders, support_threshold, confidence_threshold):
    """Accepts a list of item sets (i.e. orders) and returns a list of
    association rules matching support and confidence thresholds. """
    candidate_items = set()
    for items in orders:
        candidate_items = candidate_items.union(items)

    print("Candidate items are {}".format(candidate_items))

    def apriori_next(item_set=set()):
        """Accepts a single item set and returns list of all association rules
        containing item_set that match support and confidence thresholds.
        """
        result = []

        # print("Calling APN with {}".format(item_set))
        # print("Candidates are {}".format(candidate_items))

        if len(item_set) == len(candidate_items):
            # Recursion base case.
            print("{} == {}".format(item_set, candidate_items))
            return result

        elif not item_set:
            # Initialize with every item meeting support threshold.
            print("Initializing APN.\n")
            for item in candidate_items:
                item_set = {item}
                if support_frequency(orders, item_set) > support_threshold:
                    #print("Item '{}' crosses support threshold".format(item))
                    result.extend(apriori_next(item_set))
                else:
                    pass

        else:
            # Given an item set, find all candidate items meeting thresholds
            for item in candidate_items.difference(item_set):
                #print("Testing {}".format(item_set.union({item})))
                if support_frequency(orders, item_set.union({item})) >\
                        support_threshold:
                    print("\n\nItem set {} crosses support threshold".format(
                        item_set.union({item})))
                    if confidence(orders, item_set, {item}) >\
                            confidence_threshold:
                        print("\n\n{} => {} crosses confidence threshold".format(
                            item_set, item))
                        result.append((item_set, item))
                        result.extend(apriori_next(item_set.union({item})))
                    else:
                        pass
                else:
                    pass

        return [rule for rule in result if rule]

    return apriori_next()


def main():
    """TODO: Insert docstring here."""
    data = read_CSV('market_basket.csv')
    # item_set = set(['Eggs','Bread'])
    # item_set2 = set(['Spinach'])
    # print(support_frequency(data, item_set))
    # print(confidence(data, item_set, item_set2))

    print(["{} => {}".format(item_set, item) for item_set, item in apriori(
        data, 0.1, 0.1)])


if __name__ == '__main__':
    main()
