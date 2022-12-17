from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, HTMLResponse
import psycopg2

import service

app = FastAPI()
connection = psycopg2.connect(host='localhost', port='30001', database='roddit_db_docker', user='roddit_user', password='trailking201')


@app.get('/base/select_table')
def fill_one_table(tablename: str):
    """
    Select any table
    """
    query = f"""
        SELECT *
        FROM {tablename};
    """
    result, status = service.execute(query)
    return result


@app.get('/base/insert/rate_categories')
def advanced_union_pages_communities():
    """
    Base\n
    INSERT\n
    добавление поста в mtom таблицу, с условием что этот пост\n
    не добавлен в mtom таблицу для page_posts
    """
    query = """
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
        """
    result, status = service.execute(query)
    return result


@app.get('/base/update/community_name')
def advanced_union_pages_communities(community_id: int):
    """
    Base\n
    UPDATE\n
    просто
    """
    query = f"""
        UPDATE communities
        SET 
            name = 'Cats and Gods',
            description = 'This community is writing about cats and gods'
        WHERE community_id = {community_id}
        RETURNING *;
        """
    result, status = service.execute(query)
    return result


@app.get('/base/like/like_telephone')
def advanced_union_pages_communities(string: str):
    """
    Base\n
    LIKE\n
    телефон начинается на 375
    """
    query = """
        SELECT *
        FROM users
        WHERE telephone LIKE '%(string)s%';
        """, {'string': string}
    result, status = service.execute(query)
    return result


@app.get('/base/update/update_username')
def advanced_union_pages_communities():
    """
    Base\n
    UPDATE\n
    простой update
    """
    query = """
        UPDATE users 
        SET username = 'vasya_pupkin'
        WHERE username = 'tina_leach'
        RETURNING *;
        """
    result, status = service.execute(query)
    return result


@app.get('/base/delete/remove_comments')
def advanced_union_pages_communities():
    """
    Base\n
    DELETE\n
    удалить комменты
    """
    query = """
        DELETE FROM comments WHERE comment_id > 90;
        """
    result, status = service.execute(query)
    return result


@app.get('/base/distinct/com')
def advanced_union_pages_communities():
    """
    Base\n
    DISTINCT\n
    com
    """
    query = """
        SELECT DISTINCT name FROM communities;
        """
    result, status = service.execute(query)
    return result


@app.get('/base/subqueries/page_posts')
def advanced_union_pages_communities():
    """
    Base\n
    SUBQUIERIES\n
    вставка значений
    """
    query = """
        INSERT INTO page_posts(page_id, post_id)
        VALUES
        (
            (SELECT page_id FROM pages WHERE owner_id = 3),
            (SELECT post_id FROM posts WHERE title = 'Product through professional.')
        );
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/union/pages_communities')
def advanced_union_pages_communities():
    """
    Advanced\n
    UNION\n
    выводит информацию о всех pages и communities
    """
    query = """
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
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/group_by/top_3_communities')
def advanced_union_pages_communities():
    """
    Advanced\n
    GROUP BY\n
    топ 3 category по количеству групп в каждой категории + offset 2
    """
    query = """
        SELECT
            cat.title,
            COUNT(com.category_id) communities_amount
        FROM communities AS com
        INNER JOIN categories AS cat USING (category_id)
        GROUP BY cat.title
        ORDER BY communities_amount DESC
        LIMIT 3 OFFSET 2;
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/group_by/amount_posts')
def advanced_group_by_amount_posts():
    """
    Advanced\n
    GROUP BY\n
    подсчитать сколько постов на каждой странице
    """
    query = """
        SELECT com.community_id, com.name, cp.posts_amount
        FROM communities AS com
        INNER JOIN (
            SELECT
                community_id,
                COUNT(post_id) posts_amount
            FROM community_posts
            GROUP BY community_id
        ) AS cp USING (community_id);
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/having/amount_posts_gt_2')
def advanced_union_pages_communities():
    """
    Advanced\n
    HAVING\n
    вывести communities с количеством постов > 2
    """
    query = """
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
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/exists/posts_amount_likes_gt_2')
def advanced_union_pages_communities():
    """
    Advanced\n
    EXISTS\n
    вывести посты у которых количество лайков > 2
    """
    query = """
        SELECT post_id, title
        FROM posts p
        WHERE EXISTS(
            SELECT 1
            FROM post_likes pl
            WHERE pl.post_id = p.post_id
                AND likes > 2
        )
        ORDER BY post_id;
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/join/amount_followers_com')
def advanced_union_pages_communities(community_id: int):
    """
    Advanced\n
    INNER JOIN\n
    количество подписчиков у community
    """
    print(community_id)
    query = f"""
        SELECT com.community_id, com.name, cf.followers
        FROM communities AS com
        INNER JOIN followers_community_amount(%s) AS cf USING (community_id);
        """, (community_id)
    print(query)
    result, status = service.execute(query)
    return result


@app.get('/advanced/join/top_3_com_followers')
def advanced_union_pages_communities():
    """
    Advanced\n
    INNER JOIN\n
    вывести топ 3 community по количеству подписчиков
    """
    query = """
        SELECT com.community_id, com.name, cf.followers
        FROM communities AS com
        INNER JOIN followers_community_amount() AS cf USING (community_id)
        ORDER BY cf.followers DESC
        LIMIT 3;
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/between/com_amount_followers_between_1_2')
def advanced_union_pages_communities():
    """
    Advanced\n
    INNER JOIN, BETWEEN\n
    вывести communities у которых колво подписчиков между 1 и 2
    """
    query = """
        SELECT com.community_id, com.name, cf.followers
        FROM communities AS com
        INNER JOIN followers_community_amount() AS cf USING (community_id)
        WHERE cf.followers BETWEEN 1 AND 2
        ORDER BY cf.followers DESC;
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/join/community_category_name')
def advanced_union_pages_communities():
    """
    Advanced\n
    INNER JOIN\n
    community + название ее категории
    """
    query = """
        SELECT 
            com.name,
            com.description,
            com.date_created,
            cat.title as category_name
        FROM communities AS com
        INNER JOIN categories AS cat USING (category_id);
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/where_in/com_name_one_of')
def advanced_union_pages_communities():
    """
    Advanced\n
    WHERE IN\n
    выбирает communities у которых название категории одно из нескольких значений
    """
    query = """
        SELECT * 
        FROM (
            SELECT com.name, cat.title AS cat_name
            FROM communities AS com
            INNER JOIN categories AS cat USING (category_id)
        ) AS com_cat
        WHERE cat_name IN ('bicycle', 'music');
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/aggreg_avg/avg_followers_com')
def advanced_union_pages_communities():
    """
    Advanced\n
    AGGREGATE: AVG\n
    находит среднее количество подписчиков у communities
    """
    query = """
        SELECT AVG(followers) avg_followers
        FROM followers_community_amount() cf;
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/aggreg_sum/sim_likes_all_posts_all_com')
def advanced_union_pages_communities():
    """
    Advanced\n
    AGGREGATE: SUM\n
    находит сколько всего лайков поставлено на всех постах communities
    """
    query = """
        SELECT SUM(p.likes)
        FROM (
            SELECT com.community_id, cp.post_id
            FROM communities com
            INNER JOIN community_posts cp USING (community_id)
            WHERE community_id = 1
        ) cp
        INNER JOIN posts p USING (post_id);
        """
    result, status = service.execute(query)
    return result


@app.get('/advanced/case/rate_categories')
def advanced_union_pages_communities():
    """
    Advanced\n
    CASE\n
    выписывает какие самый популярные категории, какие средние, какие неинтересные
    """
    query = """
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
        """
    result, status = service.execute(query)
    return result


@app.get('/init/create_tables')
def create_tables():
    """
    Create all tables
    """
    result, status = service.create_tables()
    return result


@app.get('/init/drop_tables')
def drop_tables():
    """
    Drop all tables
    """
    result, status = service.drop_tables()
    return result


@app.get('/init/create_indexes')
def create_indexes():
    """
    Create all indexes
    """
    result, status = service.create_indexes()
    return result


@app.get('/init/drop_indexes')
def drop_indexes():
    """
    Drop all indexes
    """
    result, status = service.drop_indexes()
    return result


@app.get('/init/create_triggers')
def create_triggers():
    """
    Create all triggers
    """
    result, status = service.create_triggers()
    return result


@app.get('/init/create_functions')
def create_functions():
    """
    Create all functions and procedures
    """
    result, status = service.create_functions()
    return result


@app.get('/init/fill_all_tables')
def fill_all_tables():
    """
    Fill all tables
    """
    result, status = service.fill_all_tables()
    return result


@app.get('/init/fill_one_table')
def fill_one_table(tablename: str):
    """
    Fill table
    """
    result, status = service.fill_one_table(tablename)
    return result


@app.get('/fill/register_user')
def fill_one_table(
        username: str,
        password: str,
        email: str,
        telephone: str,
        role_id: int
    ):
    """
    Fill users
    """
    result, status = service.fill_one_table('users', username=username, password=password, email=email, telephone=telephone, role_id=role_id)
    return result


@app.get('/fill/register_page')
def fill_one_table(
        owner_id: int,
        description: str,
    ):
    """
    Fill pages
    """
    result, status = service.fill_one_table('pages', owner_id=owner_id, description=description)
    return result


@app.get('/fill/create_tag')
def fill_one_table(
        title: str
    ):
    """
    Fill tags
    """
    result, status = service.fill_one_table('tags', title=title)
    return result


@app.get('/fill/create_category')
def fill_one_table(
        title: str
    ):
    """
    Fill tags
    """
    result, status = service.fill_one_table('categories', title=title)
    return result


@app.get('/fill/register_community')
def fill_one_table(
        name: str,
        description: str
    ):
    """
    Fill tags
    """
    result, status = service.fill_one_table('communities', name=name, description=description)
    return result


@app.get('/fill/create_post_community')
def fill_one_table(
        title: str,
        text: str,
        community_id: str
    ):
    """
    при создании post должен быть создан в каокйто community (fill community_posts)
    """
    result, status = service.fill_one_table('posts', 'community_posts', title=title, text=text, community_id=community_id)
    return result


@app.get('/fill/create_comment')
def fill_one_table(
        title: str,
        text: str
    ):
    """
    Fill tags
    """
    dict_values = {
        'title': title,
        'text': text
    }
    result, status = service.fill_one_table('comments', **dict_values)
    return result


@app.get('/delete/user')
def remove_user(
        username: str
    ):
    """
    Delete user
    """
    result, status = service.remove_row('users', username=username)
    return result


@app.get('/update/user')
def update_user(
        user_id: int,
        username: str,
        password: str,
        email: str,
    ):
    """
    Update user
    """
    result, status = service.update_row('users', user_id=user_id, username=username, password=password, email=email)
    return result