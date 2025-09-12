import mysql.connector

config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'ALX_prodev'
}


def stream_user_ages():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT age FROM user_data;")
        for (age,) in cursor:
            yield float(age)
    finally:
        cursor.close()
        connection.close()


def calculate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        return 0
    return total_age / count
