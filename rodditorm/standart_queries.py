import psycopg2
import fill_tables

connection = psycopg2.connect(host='localhost', port='30001', database='roddit_db_docker', user='roddit_user', password='trailking201')

cursor = connection.cursor()

# how to connect to the psql inside containter:
# psql -U roddit_user -d roddit_db_docker


def _recreate():
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
            telephone       CHAR(13) UNIQUE,
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

def _create_indexes():
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

def _drop_indexes():
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
    
def _drop_tables():
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

def _fill_all_tables():
    fill_tables.fill(connection, ['roles', 'users', 'tags', 'categories', 'pages', 'communities', 'posts', 'comments'])

def _fill_one_table(tablename):
    fill_tables.fill(connection, [tablename,])
    

def main(drop_all, create, create_indexes, drop_indexes, fill_all_tables, fill_one_table):
    if (drop_all): _drop_tables()
    if (create): _recreate()
    if (create_indexes): _create_indexes()
    if (drop_indexes): _drop_indexes()
    if (fill_all_tables): _fill_all_tables()
    if (fill_one_table): _fill_one_table(fill_one_table)

if __name__ == '__main__':
    # show all indexes (including pk)
    cursor.execute("""select * from pg_indexes where tablename not like 'pg%';""")
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
    args = parser.parse_args()
    main(
        drop_all=args.drop_all,
        create=args.create,
        create_indexes=args.create_indexes,
        drop_indexes=args.drop_indexes,
        fill_all_tables=args.fill_all_tables,
        fill_one_table=args.fill_one_table,
    )