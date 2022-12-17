import psycopg2
from fastapi import HTTPException, status
from utils import initializing
# import fill_tables

connection = psycopg2.connect(host='localhost', port='30001', database='roddit_db_docker', user='roddit_user', password='trailking201')

def printing(result, curs_description):
    sresult = ""
    widths = []
    columns = []
    tavnit = '|'
    separator = '+' 
    for i, cd in enumerate(curs_description):
        column = [ str(result[j][i]) for j in range(0, result.__len__()) ]
        max_col_len = len(max(column, key=len))
        widths.append(max(max_col_len, len(cd[0])))
        columns.append(cd[0])

    for w in widths:
        tavnit += " %-"+"%ss |" % (w,)
        separator += '-'*w + '--+'

    sresult += separator + '\n'
    sresult += tavnit % tuple(columns) + '\n'
    sresult += separator + '\n'
    for row in result:
        sresult += tavnit % row + '\n'
    sresult += separator + '\n'
    print(sresult)
    return result

def execute(query: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            print(cursor.description)
            result = printing(cursor.fetchall(), cursor.description)
    print(query)
    return result, status.HTTP_200_OK


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            initializing.recreate(cursor)
            result = 'All tables has been created'
    return result, status.HTTP_200_OK


def create_indexes():
    with connection:
        with connection.cursor() as cursor:
            initializing.create_indexes(cursor)
            result = 'All indexes has been created'
    return result, status.HTTP_200_OK


def drop_tables():
    with connection:
        with connection.cursor() as cursor:
            initializing.drop_tables(cursor)
            result = 'All tables has been dropped'
    return result, status.HTTP_200_OK


def drop_indexes():
    with connection:
        with connection.cursor() as cursor:
            initializing.drop_indexes(cursor)
            result = 'All indexes has been dropped'
    return result, status.HTTP_200_OK


def create_triggers():
    with connection:
        with connection.cursor() as cursor:
            initializing.create_triggers(cursor)
            result = 'All triggers has been created'
    return result, status.HTTP_200_OK


def create_functions():
    with connection:
        with connection.cursor() as cursor:
            initializing.create_functions(cursor)
            result = 'All functions has been created'
    return result, status.HTTP_200_OK

def fill_one_table(tablename, mtomtable="", **kwargs):
    result = 'Error'
    with connection:
        with connection.cursor() as cursor:
            if (mtomtable): result = initializing.fill_one_table_proced(cursor, tablename, mtomtable, **kwargs)
            else: result = initializing.fill_one_table(cursor, tablename, **kwargs)
    return result, status.HTTP_200_OK

def remove_row(tablename, **kwargs):
    result = 'Error'
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("BEGIN;")
            result = initializing.remove_row(cursor, tablename, **kwargs)
            cursor.execute("COMMIT;")
    return result, status.HTTP_200_OK

def update_row(tablename, **kwargs):
    result = 'Error'
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("BEGIN;")
            result = initializing.update_row(cursor, tablename, **kwargs)
            cursor.execute("COMMIT;")
    return result, status.HTTP_200_OK


# def fill_all_tables():
#     with connection.cursor() as cursor:
#         fill_tables.fill(cursor, ['roles', 'users', 'tags', 'categories', 'pages', 'communities', 'posts', 'comments'])
#         result = 'All tables has been filled'
#     return result, status.HTTP_200_OK


# def fill_one_table(tablename):
#     with connection.cursor() as cursor:
#         fill_tables.fill(cursor, [tablename,])
#         result = 'Table has been filled'
#     return result, status.HTTP_200_OK