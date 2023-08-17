"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 02/22/2023 by Alvin Osterndorff (alvinosterndorff@gmail.com)

Skeleton parser with useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""
import json
import csv
import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

"""
Returns true if a file ends in .json
"""


def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'


"""
Converts month to a number, e.g. 'Dec' to '12'
"""


def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""


def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]


"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""


def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""


def parseJson(json_file):

    with open(json_file, 'r') as f:
        items = loads(f.read())['Items']  # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            # parse seller info
            seller_dict = json.dumps(item['Seller'])

            seller = json.loads(seller_dict)
            # write tuple to Seller filepython skeleton_parser.py ebay_data/items-0.json
            with open('SellersX.dat', 'a') as seller_file:
                seller_file.write(seller['UserID'] + '|')
                seller_file.write(seller['Rating'] + '|')
                seller_file.write(item['Country'] + '|')
                item['Location'] = item['Location'].replace('\"', '\"\"')
                seller_file.write('\"' +item['Location'] + '\"\n')
            # write tuple to Item file
            with open('ItemsX.dat', 'a') as item_file:
                item_file.write(item['ItemID'] + '|')
                item['Name'] = item['Name'].replace('\"', '\"\"')
                item_file.write('\"' + item['Name'] + '\"|')
                # Category table
                with open('CategoriesX.dat', 'a') as category_file:
                    size = len(item['Category'])
                    for i in range(size):
                        category_file.write(item['ItemID'] + '|')
                        category_file.write(item['Category'][i] + '\n')
                item_file.write(transformDollar(item['Currently']) + '|')
                # check for Buy_Price, add if exists
                if 'Buy_Price' in item:
                    item_file.write(transformDollar(item['Buy_Price']) + '|')
                else:
                    item_file.write('NULL' + '|')
                item_file.write(item['First_Bid'] + '|')
                item_file.write(item['Number_of_Bids'] + '|')
                item_file.write(transformDttm(item['Started']) + '|')
                item_file.write(transformDttm(item['Ends']) + '|')
                if item['Description'] != None:
                    item['Description'] = item['Description'].replace('\"', '\"\"')
                    item_file.write('\"' + item['Description'] + '\"|')
                else:
                    item_file.write('NULL' + '|')
                item_file.write(seller['UserID'] + '\n')
            if int(item['Number_of_Bids']) > 0:
                # parse set of bids into each bid
                bids_dict = json.dumps(item['Bids'])
                bids = json.loads(bids_dict)
                for bid in bids:
                    # parse each bid
                    single_bid_dict = json.dumps(bid['Bid'])
                    single_bid = json.loads(single_bid_dict)
                    # parse bidder info
                    bidder_dict = json.dumps(single_bid['Bidder'])
                    bidder = json.loads(bidder_dict)
                    with open('BiddersX.dat', 'a') as bidder_file:
                        bidder_file.write(bidder['UserID'] + '|')
                        bidder_file.write(bidder['Rating'] + '|')
                        if 'Country' in bidder:
                            bidder_file.write(bidder['Country'] + '|')
                        else:
                            bidder_file.write('NULL' + '|')
                        if 'Location' in bidder:
                            bidder['Location'] = bidder['Location'].replace('\"', '\"\"')
                            bidder_file.write('\"' + bidder['Location'] + '\"\n')
                        else:
                            bidder_file.write('NULL' + '\n')
                    with open('BidsX.dat', 'a') as bid_file:
                        bid_file.write(bidder['UserID'] + '|')
                        bid_file.write(item['ItemID'] + '|')
                        bid_file.write(single_bid['Time'] + '|')
                        bid_file.write(transformDollar(single_bid['Amount']) + '\n')


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""


def main(argv):

    if len(argv) < 2:
        print(sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>')
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)


if __name__ == '__main__':
    main(sys.argv)
