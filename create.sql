drop table if exists Seller;
drop table if exists Item;
drop table if exists Bid;
drop table if exists Bidder;
CREATE TABLE Seller (
  UserID TEXT,
  Rating INTEGER,
  Country TEXT,
  Location TEXT,
  PRIMARY KEY (UserID)
);
CREATE TABLE Item (
  ItemID INTEGER,
  Name TEXT,
  Currently REAL,
  Buy_Price REAL,
  First_Bid REAL,
  Number_of_Bids INTEGER,
  Started TEXT,
  Ends TEXT,
  Description TEXT,
  SellerID INTEGER,
  PRIMARY KEY (ItemID),
  FOREIGN KEY (SellerID) REFERENCES Seller(UserID)
);
CREATE TABLE Category (
  ItemID INTEGER,
  Category_Name,
  PRIMARY KEY (ItemID, Category_Name),
  FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);
CREATE TABLE Bid (
  BidderID TEXT,
  ItemID INTEGER,
  Time TEXT,
  Amount REAL,
  PRIMARY KEY (BidderID, ItemID, Time),
  FOREIGN KEY (BidderID) REFERENCES Bidder(UserID),
  FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);
CREATE TABLE Bidder (
  UserID TEXT,
  Rating INTEGER,
  Country TEXT,
  Location TEXT,
  PRIMARY KEY (UserID)
);