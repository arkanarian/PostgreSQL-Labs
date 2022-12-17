import psycopg2
from . import fill_tables

# connection = psycopg2.connect(host='localhost', port='30001', database='roddit_db_docker', user='roddit_user', password='trailking201')

# cursor = connection.cursor()

# how to connect to the psql inside containter:
# psql -U roddit_user -d roddit_db_docker


def recreate(cursor):
    cursor.execute("BEGIN;")

    # roles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            role_id     int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name        VARCHAR(30) UNIQUE NOT NULL,
            permission  VARCHAR(200) NOT NULL
        );
        """
    )

    # users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id         int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            username        VARCHAR(30) UNIQUE NOT NULL,
            password        VARCHAR(100) NOT NULL,
            email           VARCHAR(50) UNIQUE,
            telephone       CHAR(12) UNIQUE,
            role_id         int NOT NULL REFERENCES roles (role_id) ON DELETE SET NULL,
            unblock_date    DATE DEFAULT NULL
        );
        """
    )

    # logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            log_id      int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            user_id     int NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
            type        VARCHAR(20) NOT NULL,
            message     VARCHAR(300) NOT NULL
        );
        """
    )

    # pages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            page_id         int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            description     VARCHAR(300),
            owner_id        int UNIQUE NOT NULL REFERENCES users (user_id) ON DELETE CASCADE
        );    
    """)

    # tags table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            tag_id      int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            title       VARCHAR(30) UNIQUE NOT NULL
        );
    """)

    # categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id     int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            title           VARCHAR(30) UNIQUE NOT NULL
        );
    """)

    # communities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS communities (
            community_id    int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name            VARCHAR(30) UNIQUE NOT NULL,
            description     VARCHAR(200),
            category_id     int NOT NULL REFERENCES categories (category_id) ON DELETE RESTRICT,
            date_created    DATE NOT NULL DEFAULT CURRENT_DATE,
            unblock_date    DATE DEFAULT NULL
        );    
    """)

    # posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            post_id         int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            title           VARCHAR(100) NOT NULL,
            text            VARCHAR(5000) NOT NULL,
            image_url       VARCHAR(300),
            likes           int NOT NULL DEFAULT 0,
            reply_to_id     int DEFAULT NULL,
            date_created    DATE NOT NULL DEFAULT CURRENT_DATE,
            date_updated    DATE DEFAULT NULL
        );    
    """)
    cursor.execute("""
        ALTER TABLE posts
        ADD FOREIGN KEY (reply_to_id) REFERENCES posts (post_id) ON DELETE SET NULL;
    """)

    # documents table
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS documents (
    #         document_id     int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    #         url             VARCHAR(300) NOT NULL
    #     );    
    #     """
    # )

    # comments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            comment_id      int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            content          VARCHAR(300),
            owner_id        int NOT NULL REFERENCES users (user_id) ON DELETE SET NULL,
            post_id         int NOT NULL REFERENCES posts (post_id) ON DELETE CASCADE,
            reply_to_id     int DEFAULT NULL,
            date_created    DATE NOT NULL DEFAULT CURRENT_DATE,
            date_edited     DATE DEFAULT NULL
        );    
    """)
    cursor.execute("""
        ALTER TABLE comments
        ADD FOREIGN KEY (reply_to_id) REFERENCES comments (comment_id) ON DELETE SET NULL;
    """)

    # many-to-many relation tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS page_followers (
            page_id     int REFERENCES pages (page_id) ON DELETE CASCADE,
            user_id     int REFERENCES users (user_id) ON DELETE CASCADE,
            CONSTRAINT page_followers_pk PRIMARY KEY (page_id, user_id)
        );
    """)
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS page_follow_requests (
    #         page_id     int REFERENCES pages (page_id) ON DELETE CASCADE,
    #         user_id     int REFERENCES users (user_id) ON DELETE CASCADE,
    #         CONSTRAINT page_follow_requests_pk PRIMARY KEY (page_id, user_id)
    #     );
    #     """
    # )
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_posts (
            community_id    int REFERENCES communities (community_id) ON DELETE CASCADE,
            post_id         int REFERENCES posts (post_id) ON DELETE CASCADE,
            CONSTRAINT community_posts_pk PRIMARY KEY (community_id, post_id)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS page_posts (
            page_id     int REFERENCES pages (page_id) ON DELETE CASCADE,
            post_id     int REFERENCES posts (post_id) ON DELETE CASCADE,
            CONSTRAINT page_posts_pk PRIMARY KEY (page_id, post_id)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_admins (
            community_id    int REFERENCES communities (community_id) ON DELETE CASCADE,
            user_id         int REFERENCES users (user_id) ON DELETE CASCADE,
            CONSTRAINT community_admins_pk PRIMARY KEY (community_id, user_id)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_followers (
            community_id    int REFERENCES communities (community_id) ON DELETE CASCADE,
            user_id         int REFERENCES users (user_id) ON DELETE CASCADE,
            CONSTRAINT community_followers_pk PRIMARY KEY (community_id, user_id)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_likes (
            post_id     int REFERENCES posts (post_id) ON DELETE CASCADE,
            user_id     int REFERENCES users (user_id) ON DELETE CASCADE,
            CONSTRAINT post_likes_pk PRIMARY KEY (post_id, user_id)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_tags (
            post_id     int REFERENCES posts (post_id) ON DELETE CASCADE,
            tag_id      int REFERENCES tags (tag_id) ON DELETE CASCADE,
            CONSTRAINT post_tags_pk PRIMARY KEY (post_id, tag_id)
        );
    """)
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS post_saved (
    #         post_id     int REFERENCES posts (post_id) ON DELETE CASCADE,
    #         user_id     int REFERENCES users (user_id) ON DELETE CASCADE,
    #         CONSTRAINT post_saved_pk PRIMARY KEY (post_id, user_id)
    #     );
    #     """
    # )
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comment_likes (
            comment_id  int REFERENCES comments (comment_id) ON DELETE CASCADE,
            user_id     int REFERENCES users (user_id) ON DELETE CASCADE,
            CONSTRAINT comment_likes_pk PRIMARY KEY (comment_id, user_id)
        );
    """)
    # cursor.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS comment_dislikes (
    #         comment_id  int REFERENCES comments (comment_id) ON DELETE CASCADE,
    #         user_id     int REFERENCES users (user_id) ON DELETE CASCADE,
    #         CONSTRAINT comment_dislikes_pk PRIMARY KEY (comment_id, user_id)
    #     );
    #     """
    # )
    

    # real 1-to-1 relations
    # cursor.execute(
    #     """
    #     ALTER TABLE users
    #     ADD FOREIGN KEY (page_id) REFERENCES pages (page_id)
    #         DEFERRABLE INITIALLY DEFERRED;

    #     ALTER TABLE pages 
    #     ADD FOREIGN KEY (owner_id) REFERENCES users (user_id)
    #             DEFERRABLE INITIALLY DEFERRED;
    #     """
    # )
    cursor.execute("COMMIT;")
    print("All tables has been created")

def create_indexes(cursor):
    cursor.execute("BEGIN;")
    cursor.execute("""
        CREATE INDEX index_posts_date_created
        ON posts USING btree (date_created DESC)
        """
    )
    cursor.execute("""
        CREATE INDEX index_users_username
        ON users USING btree (username ASC)
        """
    )
    cursor.execute("""
        CREATE INDEX index_users_email
        ON users USING btree (email ASC)
        """
    )
    cursor.execute("""
        CREATE INDEX index_page_owner_id
        ON pages USING btree (owner_id ASC)
        """
    )
    cursor.execute("""
        CREATE INDEX index_community_category_id
        ON communities USING btree (category_id ASC)
        """
    )
    cursor.execute("""
        CREATE INDEX index_community_name
        ON communities USING btree (name ASC)
        """
    )
    cursor.execute(
        """
        CREATE INDEX index_post_reply_to_id
        ON posts USING btree (reply_to_id ASC)
        """
    )
    cursor.execute(
        """
        CREATE INDEX index_comment_owner_id
        ON comments USING btree (owner_id ASC)
        """
    )
    cursor.execute(
        """
        CREATE INDEX index_comment_post_id
        ON comments USING btree (post_id ASC)
        """
    )
    cursor.execute(
        """
        CREATE INDEX index_comment_reply_to_id
        ON comments USING btree (reply_to_id ASC)
        """
    )

    # i'm using additional index because pk is not triggering at searching based on post_id
    # https://stackoverflow.com/questions/571309/how-to-properly-index-a-linking-table-for-many-to-many-connection-in-mysql
    cursor.execute(
        """
        CREATE INDEX index_page_post
        ON page_posts USING btree (post_id)
        """
    )
    cursor.execute("COMMIT;")

def drop_indexes(cursor):
    cursor.execute("BEGIN;")
    cursor.execute("DROP INDEX index_posts_date_created")
    cursor.execute("DROP INDEX index_users_username")
    cursor.execute("DROP INDEX index_users_email")
    cursor.execute("DROP INDEX index_page_owner_id")
    cursor.execute("DROP INDEX index_community_category_id")
    cursor.execute("DROP INDEX index_community_name")
    cursor.execute("DROP INDEX index_post_community_id")
    cursor.execute("DROP INDEX index_post_reply_to_id")
    cursor.execute("DROP INDEX index_comment_owner_id")
    cursor.execute("DROP INDEX index_comment_post_id")
    cursor.execute("DROP INDEX index_comment_reply_to_id")
    cursor.execute("DROP INDEX index_page_post")
    cursor.execute("COMMIT;")
    
def drop_tables(cursor):
    cursor.execute("BEGIN;")

    # drop table
    cursor.execute(
        """
        DROP TABLE IF EXISTS page_followers;
        DROP TABLE IF EXISTS community_posts;
        DROP TABLE IF EXISTS page_posts;
        DROP TABLE IF EXISTS community_admins;
        DROP TABLE IF EXISTS community_followers;
        DROP TABLE IF EXISTS post_likes;
        DROP TABLE IF EXISTS post_tags;
        DROP TABLE IF EXISTS comment_likes;
        DROP TABLE IF EXISTS comments;
        DROP TABLE IF EXISTS pages;
        DROP TABLE IF EXISTS logs;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS roles;
        DROP TABLE IF EXISTS tags;
        DROP TABLE IF EXISTS communities;
        DROP TABLE IF EXISTS categories;
        DROP TABLE IF EXISTS posts;
        """
    )
    cursor.execute("COMMIT;")
    print("15 tables has been successfully dropped")

def create_triggers(connection):
    cursor.execute("BEGIN;")

    # TRIGGER new like
    # увеличивать количество лайков при добавлении нового лайка в mtom
    cursor.execute("""
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
    """)
    cursor.execute("""
        CREATE TRIGGER trigger_new_like
        AFTER INSERT
        ON post_likes
        FOR EACH ROW
        EXECUTE PROCEDURE add_like_post_func();
    """)

    # TRIGGER undo like
    # уменьшать количество лайков при удалении лайка из mtom
    cursor.execute("""
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
    """)
    cursor.execute("""
        CREATE TRIGGER trigger_undo_like
        AFTER DELETE
        ON post_likes
        FOR EACH ROW
        EXECUTE PROCEDURE undo_like_post_func();
    """)

    # TRIGGER logging new user
    cursor.execute("""
        CREATE OR REPLACE FUNCTION logs_new_user_func()
            RETURNS trigger
        AS $$
        begin
            INSERT INTO logs(type, message) 
            VALUES ('INFO', 'New user user_id(' || new.user_id || ') "' || new.username || '" was created.');
            RETURN NEW;
        end;
        $$ LANGUAGE plpgsql;
    """)
    cursor.execute("""
        CREATE OR REPLACE TRIGGER trigger_logs_new_user
        AFTER INSERT
        ON users
        FOR EACH ROW
        EXECUTE PROCEDURE logs_new_user_func();
    """)
    cursor.execute("COMMIT;")
    print("3 triggers has been created")

def create_functions(connection):
    cursor.execute("BEGIN;")
    # PROCEDURES
    # при создании community должен быть прикриплен хотябы один админ
    cursor.execute("""
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
    """)
    
    # FUNCTION
    # количетсов подписчиков у всех community
    cursor.execute("""
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
    """)
    
    # FUNCTION
    # количетсов подписчиков у одной community
    cursor.execute("""
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
    """)
    
    cursor.execute("COMMIT;")

def fill_all_tables(connection):
    fill_tables.fill(connection, ['roles', 'users', 'tags', 'categories', 'pages', 'communities', 'posts', 'comments'])

def fill_one_table(cursor, tablename, **kwargs):
    k = ', '.join(map(str,kwargs.keys()))
    v = '\', \''.join(map(str,kwargs.values()))
    cursor.execute(f"""INSERT INTO {tablename} ({k}) VALUES ('{v}');""")
    result = f"Table '{tablename}' has been filled"
    return result

def remove_row(cursor, tablename, **kwargs):
    k = list(kwargs.keys())
    v = list(kwargs.values())
    cursor.execute(f"""DELETE FROM {tablename} WHERE {k[0]} = {v[0]};""")
    result = f"Row ({k[0]}, {v[0]}) has been removed from '{tablename}'"
    return result

def update_row(cursor, tablename, **kwargs):
    k = list(kwargs.keys())
    v = list(kwargs.values())
    cursor.execute(f"""UPDATE {tablename} SET {k[1]} = '{v[1]}', {k[2]} = '{v[2]}',{k[3]} = '{v[3]}' WHERE {k[0]} = '{v[0]}';""")
    result = f"Row ({k[0]}, {v[0]}) has been updated in '{tablename}'"
    return result


def fill_one_table_proced(cursor, tablename, mtomtable="", **kwargs):
    v = '\', \''.join(map(str,kwargs.values()))
    if (mtomtable == 'community_posts'): 
        cursor.execute(f"call new_post_community('{v}');")
    result = f"Table '{tablename}' has been filled"
    return result


def _select_table(tablename):
    cursor.execute(f"select * from {tablename}")
    records = cursor.fetchall()
    for row in records:
        print(row)

def _add_mtom(input: str):
    arr_input = input.split(' ')
    tablename = arr_input[0]
    ind_1 = arr_input[1]
    ind_2 = arr_input[2]
    print(tablename)
    print(ind_1)
    print(ind_2)

def _fill_mtom_default():
    fill_tables.fill_mtom_default(connection)

def _fill_one_mtom():
    fill_tables.fill_one_mtom(connection)
    

def main(drop_all, create, create_indexes, drop_indexes, fill_all_tables, fill_one_table, select_table, add_mtom, fill_mtom_default, fill_one_mtom):
    if (drop_all): drop_tables()
    if (create): recreate()
    if (create_indexes): create_indexes()
    if (drop_indexes): drop_indexes()
    if (fill_all_tables): fill_all_tables()
    if (fill_one_table): fill_one_table(fill_one_table)
    if (select_table): _select_table(select_table)
    if (add_mtom): _add_mtom(add_mtom)
    if (fill_mtom_default): _fill_mtom_default()
    if (fill_one_mtom): _fill_one_mtom()

if __name__ == '__main__':
    # show all indexes (including pk)
    cursor.execute("""select * from pg_indexes where tablename not like 'pg%';""")
    # records = cursor.fetchall()
    # for row in records:
    #     print(row)
    import argparse

    parser = argparse.ArgumentParser(description='Executes standart queries on Postgres database')
    parser.add_argument('-d', '--drop_all', required=False,
                        help='drop all tables', action="store_true")
    parser.add_argument('-r', '--create', required=False,
                        help='create tables if not exists', action="store_true")
    parser.add_argument('-ci', '--create_indexes', required=False,
                        help='create indexes on tables', action="store_true")
    parser.add_argument('-di', '--drop_indexes', required=False,
                        help='drops indexes on tables', action="store_true")
    parser.add_argument('--fill_all_tables', required=False,
                        help='fill tables with dummy data', action="store_true")
    parser.add_argument('-f', '--fill_one_table', required=False,
                        help='fill one table with specified name')
    parser.add_argument('--select_table', required=False,
                        help='select from tablename')
    parser.add_argument('--add_mtom', required=False,
                        help='add many to many relation')
    parser.add_argument('--fill_mtom_default', required=False,
                        help='fill mtom default', action="store_true")
    parser.add_argument('--fill_one_mtom', required=False,
                        help='fill mtom default', action="store_true")
    args = parser.parse_args()
    main(
        drop_all=args.drop_all,
        create=args.create,
        create_indexes=args.create_indexes,
        drop_indexes=args.drop_indexes,
        fill_all_tables=args.fill_all_tables,
        fill_one_table=args.fill_one_table,
        select_table=args.select_table,
        add_mtom=args.add_mtom,
        fill_mtom_default=args.fill_mtom_default,
        fill_one_mtom=args.fill_one_mtom,
    )