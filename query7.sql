WITH NameCount as (
  SELECT Category.Category_Name, Bid.Amount
  FROM Category, Bid
  WHERE Category.ItemID = Bid.ItemID
  AND Bid.Amount > 100)
SELECT COUNT(DISTINCT Category_Name)
FROM NameCount;
