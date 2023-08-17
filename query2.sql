SELECT COUNT(DISTINCT UserID) AS NumNY
FROM (
  SELECT UserID FROM Seller WHERE Location = 'New York'
  UNION
  SELECT UserID FROM Bidder WHERE Location = 'New York'
) AS TotalUsersNY;
