#!/usr/bin/env python3
# Market basket python program

import csv



print("Hello world")

def read_CSV(file_name):

    result = list()
    with open(file_name, 'rb') as csv_file:
        file_reader = csv.reader(csv_file)
        for row in file_reader:
            result.append(row)
    return result


def support_count(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    sum_list = list()
    transpose = [[row[i] for row in matrix] for i in range(cols)]
    for row in transpose:
        sum_list.append(sum(list(map(int, row[1:]))))

    #print(transpose)
    #print(sum_list)
    return sum_list

def support_frequency():


def main():
    data = read_CSV('market_basket.csv')
    support_count(data)


if __name__ == '__main__':
    main()
