import time
import mysql.connector
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="ALX_prodev"
        )
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            print("[LOG] MySQL connection closed.")
    return wrapper

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except mysql.connector.Error as e:
                    attempt += 1
                    print(f"[ERROR] Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"[LOG] Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("[FATAL] All retry attempts failed.")
                        raise
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    return cursor.fetchall()

