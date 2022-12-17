-- SELECT
SELECT *
FROM communities
WHERE 



-- ALTER TABLE
ALTER TABLE communities ALTER COLUMN date_created DATE NOT NULL DEFAULT DATE(CURRENT_DATE);
ALTER TABLE communities DROP COLUMN date_created;
ALTER TABLE communities ALTER COLUMN date_created SET NOT NULL;
ALTER TABLE posts ADD COLUMN likes int NOT NULL DEFAULT 0;
ALTER FUNCTION RENAME trigger_function TO add_likes_post_func;

SELECT
	count(*) > 0 IF 'above' : 'down zero' AS some_col

-- INSERT
-- добавление поста в mtom таблицу, с условием что этот пост 
-- не добавлен в mtom таблицу для page_posts
do $$
begin
IF (
	SELECT count(*)
	FROM page_posts
	WHERE post_id = 3
) > 0
THEN
	RAISE notice'Post is realted to a page';
ELSE 
	INSERT INTO community_posts(community_id, post_id)
	VALUES (1,3);
END IF;
end $$;

-- UPDATE
UPDATE communities
SET 
	name = 'Cats and Gods',
	description = 'This community is writing about cats and gods'
WHERE community_id = 1
RETURNING *;

-- телефон начинается на 375
SELECT *
FROM users
WHERE telephone LIKE '375%';


-- простой update
UPDATE users 
SET username = 'vasya_pupkin'
WHERE username = 'tina_leach'
RETURNING *;


-- DELETE
DELETE FROM comments WHERE comment_id > 30;

-- DISTINCT
-- убирает повторяющиеся строки по определенному столбцу
SELECT DISTINCT name FROM communities;


-- SUBQUIERIES
INSERT INTO page_posts(page_id, post_id)
VALUES
(
	(SELECT page_id FROM pages WHERE owner_id = 3),
	(SELECT post_id FROM posts WHERE title = 'Product through professional.')
)

