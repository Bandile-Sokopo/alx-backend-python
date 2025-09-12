import mysql.connector

config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'ALX_prodev'
}


def stream_users():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:   
            yield row
    finally:
        cursor.close()
        connection.close()
