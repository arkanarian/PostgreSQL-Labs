-- ORDER BY
SELECT name, description, date_created FROM communities ORDER BY name DESC;
SELECT title, text, image_url, date_created, date_updated FROM posts ORDER BY date_created DESC;

SELECT name, description, date_created FROM communities WHERE category_id = 1;


-- GROUP BY
-- топ 3 количество групп в каждой категории
-- OFFSET - начинать с какого
SELECT
	cat.title,
	COUNT(com.category_id) communities_amount
FROM communities AS com
INNER JOIN categories AS cat USING (category_id)
GROUP BY cat.title
ORDER BY communities_amount DESC
LIMIT 3 OFFSET 2;

-- подсчитать сколько постов на каждой странице
SELECT com.community_id, com.name, cp.posts_amount
FROM communities AS com
INNER JOIN (
	SELECT
		community_id,
		COUNT(post_id) posts_amount
	FROM community_posts
	GROUP BY community_id
) AS cp USING (community_id);


-- вывести communities с количеством постов > 2
-- HAVING
SELECT com.community_id, com.name, cp.posts_amount
FROM communities AS com
INNER JOIN (
	SELECT
		community_id,
		COUNT(post_id) posts_amount
	FROM community_posts
	GROUP BY community_id
	HAVING COUNT(post_id) > 2
) AS cp USING (community_id);


-- EXISTS
-- вывести посты у которых количество лайков > 2
SELECT post_id, title
FROM posts p
WHERE EXISTS(
	SELECT 1
	FROM post_likes pl
	WHERE pl.post_id = p.post_id
		AND likes > 2
)
ORDER BY post_id;


-- количество подписчиков у community
-- parameter: community_id
SELECT com.community_id, com.name, cf.followers
FROM communities AS com
INNER JOIN followers_community_amount(2) AS cf USING (community_id);

-- вывести топ 3 community по количеству подписчиков
SELECT com.community_id, com.name, cf.followers
FROM communities AS com
INNER JOIN followers_community_amount() AS cf USING (community_id)
ORDER BY cf.followers DESC
LIMIT 3;

-- вывести communities у которых колво подписчиков между 1 и 2 (включая) BETWEEN
SELECT com.community_id, com.name, cf.followers
FROM communities AS com
INNER JOIN followers_community_amount() AS cf USING (community_id)
WHERE cf.followers BETWEEN 1 AND 2
ORDER BY cf.followers DESC;


-- JOIN
-- community + название ее категории
SELECT 
	com.name,
	com.description,
	com.date_created,
	cat.title as category_name
FROM communities AS com
INNER JOIN categories AS cat USING (category_id)

-- WHERE IN
-- выбирает communities у которых название категории одно из нескольких значений
SELECT * 
FROM (
	SELECT com.name, cat.title AS cat_name
	FROM communities AS com
	INNER JOIN categories AS cat USING (category_id)
) AS com_cat
WHERE cat_name IN ('bicycle', 'music');

-- AGGREGATE FUNCTIONS

-- AVG
-- находит среднее количество подписчиков у communities
SELECT AVG(followers) avg_followers
FROM followers_community_amount() cf;


-- SUM
-- находит сколько всего лайков поставлено на всех постах communities
-- argument: community_id
SELECT SUM(p.likes)
FROM (
	SELECT com.community_id, cp.post_id
	FROM communities com
	INNER JOIN community_posts cp USING (community_id)
	WHERE community_id = 1
) cp
INNER JOIN posts p USING (post_id);

-- UNION
-- выводит информацию о всех pages и communities
SELECT community_id AS id, type, name, description, followers
FROM (
	SELECT com.community_id, com.name, com.description, cf.followers, 'community' AS type
	FROM communities com
	INNER JOIN followers_community_amount() cf USING (community_id)
) AS c
UNION ALL
SELECT page_id, type, name, description, followers
FROM (
	SELECT p.page_id, u.username AS name, p.description, pf.followers, 'page' AS type
	FROM pages p
	INNER JOIN followers_page_amount() pf USING (page_id)
	INNER JOIN users u ON p.owner_id = u.user_id
) AS p;


-- CASE
SELECT 
	cat.category_id,
	cat.title,
	pop.com_amount,
	CASE
		WHEN pop.com_amount >= 0 and pop.com_amount < 2 THEN 'At the bottom of interest'
		WHEN pop.com_amount >= 2 and pop.com_amount < 3 THEN 'Some people interested in'
		WHEN pop.com_amount >= 3 THEN 'The hottest category'
	END popularity
FROM categories cat
INNER JOIN (
	SELECT 
		cat.category_id,
		COUNT(cat.category_id) as com_amount
	FROM categories cat
	INNER JOIN communities com USING (category_id)
	GROUP BY cat.category_id
) pop USING (category_id)
ORDER BY pop.com_amount DESC;


