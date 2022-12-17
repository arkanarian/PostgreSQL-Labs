-- STANDART QUERIES
DROP TRIGGER trigger_name ON table_name;
DROP FUNCTION function_name;

-- TRIGGER new like
-- увеличивать количество лайков при добавлении нового лайка в mtom
CREATE OR REPLACE FUNCTION add_like_post_func()
	RETURNS trigger
AS $$
begin
	UPDATE posts
	likes = likes + 1
	WHERE post_id = new.post_id;
	RETURN NEW;
end;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_new_like
AFTER INSERT
ON post_likes
FOR EACH ROW
EXECUTE PROCEDURE add_like_post_func();
-- RUN
INSERT INTO post_likes (post_id, user_id) VALUES (3,2);

-- TRIGGER undo like
-- уменьшать количество лайков при удалении лайка из mtom
CREATE OR REPLACE FUNCTION undo_like_post_func()
	RETURNS trigger
AS $$
begin
	UPDATE posts
	likes = likes - 1
	WHERE post_id = old.post_id;
	RETURN NEW;
end;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_undo_like
AFTER DELETE
ON post_likes
FOR EACH ROW
EXECUTE PROCEDURE undo_like_post_func();
-- RUN
DELETE FROM post_likes WHERE post_id = 3 AND user_id = 2;

-- TRIGGER logging new user
CREATE OR REPLACE FUNCTION logs_new_user_func()
	RETURNS trigger
AS $$
begin
	INSERT INTO logs(type, message) 
	VALUES ('INFO', 'New user user_id(' || new.user_id || ') "' || new.username || '" was created.');
	RETURN NEW;
end;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_logs_new_user
AFTER INSERT
ON users
FOR EACH ROW
EXECUTE PROCEDURE logs_new_user_func();
-- RUN
-- python3 main.py -f users


-- PROCEDURES
-- при создании community должен быть прикриплен хотябы один админ
CREATE OR REPLACE PROCEDURE new_community(
	_name VARCHAR(30),
	_description VARCHAR(200),
	_category_id int,
	_admin_id int
)    
as $$
declare
	_community_id int := -1;
begin
	with rows as (
		insert into communities(name, description, category_id)
		values (_name, _description, _category_id)
		returning *
	)
	SELECT community_id
	INTO _community_id
	FROM rows;
	-- add admin of community
	insert into community_admins(community_id, user_id)
	values (_community_id, _admin_id);

    commit;
end;
$$ language plpgsql;


-- PROCEDURES
-- при создании post должен быть создан в каокйто community (fill community_posts)
CREATE OR REPLACE PROCEDURE new_post_community(
	_title VARCHAR(100),
	_text VARCHAR(5000),
	_community_id int
)    
as $$
declare
	_post_id int := -1;
begin
	with rows as (
		insert into posts(title, text)
		values (_title, _text)
		returning post_id
	)
	select post_id
	into _post_id
	from rows;
	insert into community_posts(community_id, post_id)
	values (_community_id, _post_id);
end;
$$ language plpgsql;

-- количетсов подписчиков у всех community
CREATE OR REPLACE FUNCTION followers_community_amount()
	RETURNS TABLE ( community_id int,
					followers bigint)
	LANGUAGE plpgsql AS
$func$
BEGIN
   	RETURN QUERY
	SELECT c.community_id,
		COUNT(cf.user_id) AS followers
	FROM communities AS c
	INNER JOIN community_followers AS cf USING (community_id)
	GROUP BY c.community_id;
END
$func$;

-- количетсов подписчиков у одной community
CREATE OR REPLACE FUNCTION followers_community_amount(_community_id int)
	RETURNS TABLE ( community_id int,
					followers bigint)
	LANGUAGE plpgsql AS
$func$
BEGIN
   	RETURN QUERY
	SELECT c.community_id,
		COUNT(cf.user_id) AS followers
	FROM communities AS c
	INNER JOIN community_followers AS cf USING (community_id)
	WHERE cf.community_id = _community_id
	GROUP BY c.community_id;
END
$func$;

-- количетсов подписчиков у всех page
CREATE OR REPLACE FUNCTION followers_page_amount()
	RETURNS TABLE ( page_id int,
					followers bigint)
	LANGUAGE plpgsql AS
$func$
BEGIN
   	RETURN QUERY
	SELECT p.page_id,
		COUNT(pf.user_id) AS followers
	FROM pages AS p
	INNER JOIN page_followers AS pf USING (page_id)
	GROUP BY p.page_id;
END
$func$;

-- количетсов подписчиков у одной page
CREATE OR REPLACE FUNCTION followers_page_amount(_page_id int)
	RETURNS TABLE ( page_id int,
					followers bigint)
	LANGUAGE plpgsql AS
$func$
BEGIN
   	RETURN QUERY
	SELECT p.page_id,
		COUNT(pf.user_id) AS followers
	FROM pages AS p
	INNER JOIN page_followers AS pf USING (page_id)
	WHERE pf.page_id = _page_id
	GROUP BY p.page_id;
END
$func$;