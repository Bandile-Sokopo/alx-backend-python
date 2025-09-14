import mysql.connector

class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="password", database="ALX_prodev"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        print("[LOG] Database connection opened.")
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[ERROR] {exc_type} - {exc_val}")
            self.conn.rollback()
        else:
            self.conn.commit()

        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("[LOG] Database connection closed.")
        return False  
