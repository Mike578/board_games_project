USE bgg_project;


SELECT *
FROM bgg_project.df_games_before_cleaning
LIMIT 50;


-- BG general info
SELECT
g.bgg_id
, g.name
, g.year_published
, ROUND(g.avg_rating,2) AS average_rating
, ROUND(g.game_weight,1) AS game_difficulty
, rd.total_ratings
FROM bgg_project.df_games_before_cleaning AS g 
LEFT JOIN bgg_project.mechanics_improved AS mi USING (bgg_id)
LEFT JOIN bgg_project.artists_improved AS ai USING (bgg_id)
LEFT JOIN bgg_project.publishers_improved AS pi USING (bgg_id)
LEFT JOIN bgg_project.themes_improved AS ti USING (bgg_id)
LEFT JOIN bgg_project.ratings_distribution AS rd USING (bgg_id) 
LIMIT 50;

DESCRIBE bgg_project.df_games_before_cleaning;

-- BG details
SELECT
g.bgg_id 
, g.name
, g.mfg_age_rec AS manufacturer_age_reco
, ROUND(g.com_age_rec,0) AS community_age_reco
, g.mfg_playtime AS manufacturer_playtime_reco
, g.com_min_playtime AS community_min_playtime
, g.com_max_playtime AS community_max_playtime
, ti.theme
, mi.mechanic
, ai.artists
, pi.publisher
, g.kickstarted
, g.description
, g.image_path
FROM bgg_project.df_games_before_cleaning AS g 
LEFT JOIN bgg_project.mechanics_improved AS mi USING (bgg_id)
LEFT JOIN bgg_project.artists_improved AS ai USING (bgg_id)
LEFT JOIN bgg_project.publishers_improved AS pi USING (bgg_id)
LEFT JOIN bgg_project.themes_improved AS ti USING (bgg_id)
LEFT JOIN bgg_project.ratings_distribution AS rd USING (bgg_id) 
LIMIT 50;


-- Top 10 best games in the 90's
SELECT
	g.bgg_id,
    g.name,
    rd.average_rating,
    rd.total_ratings,
    t.theme
FROM bgg_project.games AS g
LEFT JOIN bgg_project.ratings_distribution AS rd USING (bgg_id) 
LEFT JOIN bgg_project.themes_improved AS t USING (bgg_id)
WHERE rd.total_ratings > 200
AND g.year_published >= 1990 AND g.year_published < 2001
ORDER BY rating desc
LIMIT 20;

-- Top 10 best games in the 2000's
SELECT
	g.bgg_id,
    g.name,
    rd.average_rating,
    rd.total_ratings,
    t.theme
FROM bgg_project.games AS g
LEFT JOIN bgg_project.ratings_distribution AS rd USING (bgg_id) 
LEFT JOIN bgg_project.themes_improved AS t USING (bgg_id)
WHERE rd.total_ratings > 200
AND g.year_published >= 2000 AND g.year_published < 2010
ORDER BY rating desc
LIMIT 20;



-- Evolution of the  number of BG published over years
SELECT
	year_published,
    COUNT(*) AS total_games
FROM bgg_project.games AS g
WHERE year_published IS NOT NULL
GROUP BY year_published
ORDER BY year_published DESC;


-- What are the most popular themes
SELECT
    t.theme,
    COUNT(g.bgg_id) AS total_games
FROM bgg_project.games g
LEFT JOIN bgg_project.themes_improved t ON g.bgg_id = t.bgg_id
WHERE t.theme IS NOT NULL
GROUP BY t.theme
ORDER BY total_games DESC
LIMIT 10;


-- Top 10 publishers
SELECT 
    p.publisher,
    COUNT(g.bgg_id) AS total_games
FROM bgg_project.games g
LEFT JOIN bgg_project.publishers_improved p ON g.bgg_id = p.bgg_id
WHERE p.publisher IS NOT NULL
GROUP BY p.publisher
ORDER BY total_games DESC
LIMIT 10;


-- How game difficulty influences the average rating
SELECT
	ROUND(game_weight, 1) AS difficulty_level,
    COUNT(*) AS total_games,
    ROUND(AVG(avg_rating), 2) AS avg_rating
FROM bgg_project.df_games_before_cleaning
GROUP BY difficulty_level
ORDER BY difficulty_level ASC;


-- Average time duration per game category
SELECT
    c.category,
    ROUND(AVG(g.com_min_playtime), 2) AS avg_min_playtime,
    ROUND(AVG(g.com_max_playtime), 2) AS avg_max_playtime
FROM bgg_project.games g
LEFT JOIN bgg_project.categories_improved c USING(bgg_id)
WHERE g.com_max_playtime IS NOT NULL
GROUP BY c.category
ORDER BY avg_max_playtime DESC
LIMIT 10;