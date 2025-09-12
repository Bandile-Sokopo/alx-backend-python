import mysql.connector

config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'ALX_prodev'
}


def paginate_users(page_size, offset):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s;",
            (page_size, offset)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
