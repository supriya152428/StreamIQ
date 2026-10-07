-- ============================================
-- StreamIQ: Netflix Content Analysis
-- PostgreSQL
-- ============================================


-- 1. Total number of titles
SELECT COUNT(*) AS total_titles
FROM netflix_titles;


-- 2. Movies vs TV Shows
SELECT
    type,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY type;


-- 3. Titles by release year
SELECT
    release_year,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY release_year
ORDER BY release_year DESC;


-- 4. Recent titles
SELECT
    title,
    release_year
FROM netflix_titles
WHERE release_year > 2020
ORDER BY release_year DESC;


-- 5. Years with more than 100 titles
SELECT
    release_year,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY release_year
HAVING COUNT(*) > 100
ORDER BY total_titles DESC;


-- 6. Recent vs Older Content
SELECT
    CASE
        WHEN release_year >= 2020 THEN 'Recent'
        ELSE 'Older'
    END AS content_age,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY content_age;


-- 7. Available Netflix Ratings
SELECT DISTINCT rating
FROM netflix_titles
ORDER BY rating;


-- 8. Latest 10 Releases
SELECT
    title,
    release_year
FROM netflix_titles
ORDER BY release_year DESC
LIMIT 10;


-- 9. Average Movie Duration
SELECT
    AVG(duration_value) AS avg_movie_duration
FROM netflix_titles
WHERE type = 'Movie'
  AND duration_unit = 'min';


-- 10. Content Added by Year
SELECT
    year_added,
    COUNT(*) AS titles_added
FROM netflix_titles
WHERE year_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added;


-- 11. Titles and Genres using JOIN
SELECT
    n.title,
    g.genre
FROM netflix_titles n
JOIN netflix_genres g
    ON n.show_id = g.show_id
LIMIT 20;


-- 12. Top 10 Genres
SELECT
    genre,
    COUNT(*) AS total_titles
FROM netflix_genres
GROUP BY genre
ORDER BY total_titles DESC
LIMIT 10;


-- 13. Netflix Titles Associated with India
SELECT
    n.title,
    n.type,
    n.release_year
FROM netflix_titles n
JOIN netflix_countries c
    ON n.show_id = c.show_id
WHERE c.country = 'India'
ORDER BY n.release_year DESC;


-- 14. Top 10 Content-Producing Countries
SELECT
    country,
    COUNT(*) AS total_titles
FROM netflix_countries
GROUP BY country
ORDER BY total_titles DESC
LIMIT 10;


-- 15. Country and Content Type Analysis
SELECT
    c.country,
    n.type,
    COUNT(DISTINCT n.show_id) AS total_titles
FROM netflix_titles n
JOIN netflix_countries c
    ON n.show_id = c.show_id
GROUP BY c.country, n.type
ORDER BY total_titles DESC
LIMIT 15;


-- 16. Titles Released After the Average Release Year
SELECT
    title,
    release_year
FROM netflix_titles
WHERE release_year >
      (
          SELECT AVG(release_year)
          FROM netflix_titles
      )
ORDER BY release_year DESC;


-- 17. Years with Above-Average Title Counts
WITH yearly_counts AS (
    SELECT
        release_year,
        COUNT(*) AS total_titles
    FROM netflix_titles
    GROUP BY release_year
)
SELECT *
FROM yearly_counts
WHERE total_titles >
      (
          SELECT AVG(total_titles)
          FROM yearly_counts
      )
ORDER BY total_titles DESC;


-- 18. Rank Years by Number of Titles
SELECT
    release_year,
    COUNT(*) AS total_titles,
    RANK() OVER (
        ORDER BY COUNT(*) DESC
    ) AS year_rank
FROM netflix_titles
GROUP BY release_year
ORDER BY year_rank;


-- 19. Assign Row Numbers to Years
SELECT
    release_year,
    COUNT(*) AS total_titles,
    ROW_NUMBER() OVER (
        ORDER BY COUNT(*) DESC
    ) AS row_num
FROM netflix_titles
GROUP BY release_year
ORDER BY row_num;


-- 20. Year-over-Year Content Additions
WITH yearly_additions AS (
    SELECT
        year_added,
        COUNT(*) AS titles_added
    FROM netflix_titles
    WHERE year_added IS NOT NULL
    GROUP BY year_added
)
SELECT
    year_added,
    titles_added,
    LAG(titles_added) OVER (
        ORDER BY year_added
    ) AS previous_year
FROM yearly_additions
ORDER BY year_added;