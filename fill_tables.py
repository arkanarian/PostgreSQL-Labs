import datetime
from typing import Any, Dict, Iterator
from urllib import request
import pandas as pd
from faker import Faker
from collections import defaultdict
from sqlalchemy import create_engine
import random

fake = Faker()

def fill(connection, tablename=[]):
    fake_data = defaultdict(list)
    if ("roles" in tablename): fill_roles(connection)
    if ("users" in tablename): fill_users(connection)
    if ("categories" in tablename): fill_categories(connection)
    if ("tags" in tablename): fill_tags(connection)
    if ("pages" in tablename): fill_pages(connection)
    if ("communities" in tablename): fill_communities(connection)
    if ("posts" in tablename): fill_posts(connection)
    if ("comments" in tablename): fill_comments(connection)


def fill_comments(connection):
    with connection.cursor() as cursor:
        cursor.execute("BEGIN;")
        for _ in range(30):
            cursor.execute("""
                INSERT INTO comments (content, owner_id, post_id, date_created) VALUES (
                    %(content)s,
                    %(owner_id)s,
                    %(post_id)s,
                    %(date_created)s
                );
            """, {
                'content': fake.paragraph(nb_sentences=2),
                'owner_id': random.randint(1,5),
                'post_id': random.randint(1,10),
                # 'date_created': fake.date_between(start_date=datetime.date(2022, 1, 1))
                'date_created': str(fake.date_between(start_date=datetime.date(2022, 1, 1)))
            })
        cursor.execute("COMMIT;")
    print("Table 'comments' has been filled")


def fill_posts(connection):
    with connection.cursor() as cursor:
        cursor.execute("BEGIN;")
        for _ in range(10):
            cursor.execute("""
                INSERT INTO posts (title, text, image_url) VALUES (
                    %(title)s,
                    %(text)s,
                    %(image_url)s
                );
            """, {
                'title': fake.sentence(nb_words=random.randint(3,7), variable_nb_words=False),
                'text': fake.paragraph(nb_sentences=5),
                'image_url': fake.image_url()
            })
        cursor.execute("COMMIT;")
    print("Table 'posts' has been filled")


def fill_tags(connection):
    tags_titles = ['sport', 'music', 'playing', 'adventure', 'computer', 'it', 'programming', 'plants,' 'yoga', 'hygge', 'bicycle']
    with connection.cursor() as cursor:
        cursor.execute("BEGIN;")
        for _ in range(10):
            cursor.execute("""
                INSERT INTO tags (title) VALUES (
                    %(title)s
                );
            """, {
                'title': tags_titles[_]
            })
        cursor.execute("COMMIT;")
    print("Table 'tags' has been filled")


def fill_categories(connection):
    cat_titles = ['sport', 'music', 'playing', 'adventure', 'bicycle']
    with connection.cursor() as cursor:
        cursor.execute("BEGIN;")
        for _ in range(5):
            cursor.execute("""
                INSERT INTO categories (title) VALUES (
                    %(title)s
                );
            """, {
                'title': cat_titles[_]
            })
        cursor.execute("COMMIT;")
    print("Table 'categories' has been filled")


def fill_communities(connection):
    with connection.cursor() as cursor:
        cursor.execute("BEGIN;")
        for _ in range(10):
            cursor.execute("""
                INSERT INTO communities (name, description, category_id, date_created) VALUES (
                    %(name)s,
                    %(description)s,
                    %(category_id)s,
                    %(date_created)s
                );
            """, {
                'name': fake.company(),
                'description': fake.catch_phrase(),
                'category_id': random.randint(1,5),
                'date_created': fake.date_between(start_date=datetime.date(2022, 1, 1))
            })
        cursor.execute("COMMIT;")
    print("Table 'communities' has been filled")


def fill_pages(connection):
    with connection.cursor() as cursor:
        cursor.execute("BEGIN;")
        for _ in range(5):
            cursor.execute("""
                INSERT INTO pages (description, owner_id) VALUES (
                    %(description)s,
                    %(owner_id)s
                );
            """, {
                # 'description': fake.job() + ' is my occupation. And i\' living in ' + fake.country(),
                'description': fake.paragraph(nb_sentences=2, variable_nb_sentences=False)+ ' I\'m working ' + fake.job() + '.',
                'owner_id': str(_+1)
            })
        cursor.execute("COMMIT;")
    print("Table 'pages' has been filled")


def fill_users(connection):
    with connection.cursor() as cursor:
        cursor.execute("BEGIN;")
        for _ in range(5):
            fname = fake.first_name()
            lname = fake.last_name()
            cursor.execute("""
                INSERT INTO users (username, password, email, telephone, role_id) VALUES (
                    %(username)s,
                    %(password)s,
                    %(email)s,
                    %(telephone)s,
                    %(role_id)s
                );
            """, {
                'username': fname.lower() + '_' + lname.lower(),
                'password': fake.sentence(nb_words=1, variable_nb_words=False) + str(random.randint(0,1000)) + fake.sentence(nb_words=1, variable_nb_words=False),
                'email': fake.ascii_free_email(),
                'telephone': "375" + str(random.randint(10,44)) + str(random.randint(1000000,9999999)),
                'role_id': 1,
            })
        cursor.execute("COMMIT;")
    print("Table 'users' has been filled")


def fill_roles(connection):
    with connection.cursor() as cursor:
        cursor.execute("BEGIN;")
        cursor.execute("""
            INSERT INTO roles (name, permission) VALUES 
                ('user', 'creating page, like posts, write comments, follow pages and communities'),
                ('moderator', 'blocking pages and communities, removing posts and comments, writing comments'),
                ('admin', 'blocking pages and communities, removing posts and comments, writing comments, removing users, pages and communities')
            ;
        """)
        cursor.execute("COMMIT;")
    print("Table 'roles' has been filled")