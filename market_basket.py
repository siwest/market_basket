#!/usr/bin/env python3
"""Market basket python program."""

import sys, getopt

def read_data(file_name):
    """Read a csv file that lists possible transactions"""
    result = list()
    with open(file_name, 'r') as file_reader:
        for line in file_reader:
            order_set = set(line.strip().split(','))
            result.append(order_set)
    return result


def support_count(orders, item_set):
    """Calculate support count of item set from orders 2D list"""
    count = 0

    for order in orders:
        if item_set.issubset(order):
            # print("Found {} in {}".format(item_set, order))
            count += 1
        else:
            # print("Didn't find {} in {}".format(item_set, order))
            pass
    return count


def support_frequency(orders, item_set):
    """Calculate support frequency of item set from orders 2D list"""
    N = len(orders)
    return support_count(orders, item_set)/float(N)


def confidence(orders, left, right):
    """Calculate confidence of item set from orders 2D list"""
    left_count = support_count(orders, left)
    right = right.union(left)
    right_count = support_count(orders, right)
    result = right_count/left_count
    return result


def apriori(orders, support_threshold, confidence_threshold):
    """Accepts a list of item sets (i.e. orders) and returns a list of
    association rules matching support and confidence thresholds. """
    candidate_items = set()

    for items in orders:
        candidate_items = candidate_items.union(items)

    # print("Candidate items are {}".format(candidate_items))

    def apriori_next(item_set=set()):
        """Accepts a single item set and returns list of all association rules
        containing item_set that match support and confidence thresholds.
        """
        result = []

        # print("Calling APN with {}".format(item_set))
        # print("Candidates are {}".format(candidate_items))

        if len(item_set) == len(candidate_items):
            # Recursion base case.
            # print("{} == {}".format(item_set, candidate_items))
            return result

        elif not item_set:
            # Initialize with every item meeting support threshold.
            # print("Initializing APN.\n")
            for item in candidate_items:
                item_set = {item}
                if support_frequency(orders, item_set) >= support_threshold:
                    # print("Item '{}' crosses support threshold".format(item))
                    result.extend(apriori_next(item_set))
                else:
                    pass

        else:
            # Given an item set, find all candidate items meeting thresholds
            for item in candidate_items.difference(item_set):
                # print("Testing {}".format(item_set.union({item})))
                if confidence(orders, item_set, {item}) >=\
                        confidence_threshold:
                    # print("\n\n{} => {} crosses confidence threshold at {}".format(item_set, item, confidence(orders, item_set, {item})))
                    if support_frequency(orders, item_set.union({item})) >=\
                            support_threshold:
                       #print("\nItem set {} crosses support threshold at {}".format(item_set.union({item}), support_frequency(orders, item_set.union({item}))))
                        result.append((item_set, item))
                        result.extend(apriori_next(item_set.union({item})))
                    else:
                        pass
                else:
                    pass

        return [rule for rule in result if rule]

    return apriori_next()


def main(argv):
    """Add command line arguments file name, support threshold, and confidence threshold"""
    try:
      opts, args = getopt.getopt(argv,"hf:s:c:",["support_threshold=","confidence_threshold="])
    except getopt.GetoptError:
      print ('file.csv -s <support_threshold> -c <confidence_threshold>')
      sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('file.csv -s <support> -c <confidence>')
            sys.exit()
        elif opt in ("-f", "--file"):
            infile = arg
        elif opt in ("-s", "--support"):
            support_threshold = float(arg)
        elif opt in ("-c", "--confidence"):
            confidence_threshold = float(arg)

    data = read_data(infile)

    final_results = ["{} => {}  s = {:0.2f}, c = {:0.2f}".format(
        item_set, item, support_frequency(data[1:], item_set.union({item})),
        confidence(data[1:], item_set, {item})) for item_set, item in apriori(
        data[1:], support_threshold, confidence_threshold)]
    for result in final_results:
        print(result)

if __name__ == '__main__':
    main(sys.argv[1:])
