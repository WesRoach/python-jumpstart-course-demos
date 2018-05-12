# Topics Covered:
# list comprehensions
# generator expressions
# str magic method
# repr magic method
# string parsing
# CSV file format
# Coding for Python 2 AND 3
# data pipelines with generators
import csv
import os

try:
    import statistics
except:
    import statistics_standin_for_py2 as statistics

from you_try.data_types import Purchase


def main():
    print_header()
    filename = get_data_file()
    data = load_file(filename)
    query_data(data)


def print_header():
    print("----------------------------------------")
    print("     REAL ESTATE DATA MINING APP")
    print("----------------------------------------")
    print()


def get_data_file():
    base_folder = os.path.dirname(__file__)
    return os.path.join(base_folder, 'data',
                        'SacramentoRealEstateTransactions2008.csv')


def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as fin:
        reader = csv.DictReader(fin)
        purchases = []
        for row in reader:
            p = Purchase.create_from_dict(row)
            purchases.append(p)

        return purchases


# Load File basic
# def load_file(filename):
#     with open(filename, 'r', encoding='utf-8') as fin:
#         header = fin.readline().strip()
#         print("Found header: " + header)
#
#         lines = []
#         for line in fin:
#             line_data = line.strip().split(',')
#             bed_count = line_data[4]
#             lines.append(line_data)
#
#         print(lines[:5])


def query_data(data):
    # if data was sorted by price:
    data.sort(key=lambda p: p.price)

    # most expensive house?
    high_purchase = data[-1]
    print("The most expensive house is ${:,}, with {} beds and {} "
          "baths.".format(
        high_purchase.price, high_purchase.beds, high_purchase.baths))

    # least expensive house?
    low_purchase = data[0]
    print("The least expensive house is ${:,}, with {} beds and {} "
          "baths.".format(
        low_purchase.price, low_purchase.beds, low_purchase.baths))

    # average price house?
    prices = (
        p.price  # projection or items
        for p in data  # the set to process
    )

    avg_price = statistics.mean(prices)
    print("The average home price is: ${:,}".format(int(avg_price)))

    # average price of 2 bedroom houses
    two_bed_homes = (
        p  # projection or items
        for p in data  # the set to process
        if announce(p, '2-bedrooms, found {}'.format(p.beds))
           and p.beds == 2  # test / condition
    )

    homes = []
    for h in two_bed_homes:
        if len(homes) > 5:
            break
        homes.append(h)

    avg_price = statistics.mean((announce(p.price, 'price') for p in homes))
    avg_baths = statistics.mean((p.baths for p in homes))
    avg_sqft = statistics.mean((p.sq__ft for p in homes))
    print("Average 2-bedroom home is: ${:,}, baths={}, sq ft={:,}"
          .format(int(avg_price), round(avg_baths, 1), round(avg_sqft, 1)))


def announce(item, msg):
    print("Pulling item {} for {}".format(item, msg))
    return item


if __name__ == '__main__':
    main()
