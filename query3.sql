 WITH NumCats AS (
  SELECT ItemID
  FROM Category
  GROUP BY ItemID
  HAVING COUNT(Category_Name) = 4)
SELECT COUNT(*) FROM NumCats;
