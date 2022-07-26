SELECT title FROM movies JOIN ratings ON movies.id = ratings.movie_id
WHERE id IN (SELECT stars.movie_id FROM stars WHERE person_id IN(SELECT id FROM people
WHERE name = "Chadwick Boseman")) ORDER BY ratings.rating DESC LIMIT 5;