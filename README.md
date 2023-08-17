# Web-Scraped-Auction-Database
Scrapes eBay auction data from JSON files and loads it into an SQLite database according to schema specified in an Entity-Relationship model.

In design.pdf, the Entity-Relationship model is illustrated.

The data within the JSON files is parsed in the my_parser.py file. The execution of this is conducted by running the runParser.sh Bash shell script where after the data is parsed, the tuples are sorted and duplicates are removed. The database is then created according to the table specifications in create.sql, and the data is loaded into the SQLite database by executing the commands in load.txt. Finally, I have included a set of seven SQL queries that can be run on the data in the database.
