#!/bin/bash
rm *.dat
python my_parser.py ebay_data/items-*.json
sort SellersX.dat > SellersY.dat
uniq SellersY.dat > Sellers.dat
sort ItemsX.dat > ItemsY.dat
uniq ItemsY.dat > Items.dat
sort CategoriesX.dat > CategoriesY.dat
uniq CategoriesY.dat > Categories.dat
sort BidsX.dat > BidsY.dat
uniq BidsY.dat > Bids.dat
sort BiddersX.dat > BiddersY.dat
uniq BiddersY.dat > Bidders.dat