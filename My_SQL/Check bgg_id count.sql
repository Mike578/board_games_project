USE bgg;

-- artists check bgg_id 
SELECT bgg_id, COUNT(*) AS count
FROM artists
GROUP BY bgg_id
HAVING  count > 1;
    
    
-- categories check bgg_id
SELECT bgg_id, COUNT(*) AS count
FROM categories
GROUP BY bgg_id
HAVING count > 1;

-- designers check bgg_id
SELECT bgg_id, COUNT(*) AS count
FROM designers
GROUP BY bgg_id
HAVING count > 1;


-- games check bgg_id
SELECT bgg_id, COUNT(*) AS count
FROM games
GROUP BY bgg_id
HAVING count > 1;

-- mechanics check bgg_id
SELECT bgg_id, COUNT(*) AS count
FROM mechanics
GROUP BY bgg_id
HAVING count > 1;


-- publishers check bgg_id
SELECT bgg_id, COUNT(*) AS count
FROM publishers
GROUP BY bgg_id
HAVING count > 1;
    
    
    
-- rankings check bgg_id
SELECT bgg_id, COUNT(*) AS count
FROM rankings
GROUP BY bgg_id
HAVING count > 1;
    

-- ratings_distribution check bgg_id
SELECT bgg_id, COUNT(*) AS count
FROM ratings_distribution
GROUP BY bgg_id
HAVING count > 1;

-- subcategories check bgg_id
SELECT bgg_id, COUNT(*) AS count
FROM subcategories
GROUP BY bgg_id
HAVING count > 1;


-- themes check bgg_id
SELECT bgg_id, COUNT(*) AS count
FROM themes
GROUP BY bgg_id
HAVING count > 1;
    
    

-- user_ratings check bgg_id
SELECT bgg_id, COUNT(*) AS count
FROM themes
GROUP BY bgg_id
HAVING count > 1;