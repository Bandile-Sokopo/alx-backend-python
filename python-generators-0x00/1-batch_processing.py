import mysql.connector

config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'ALX_prodev'
}


def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM user_data;")
        while True: 
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if int(user["age"]) > 25]
        yield filtered 

