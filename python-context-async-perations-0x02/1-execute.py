import mysql.connector

class ExecuteQuery:
    def __init__(self, query, params=None, host="localhost", user="root", password="your_password", database="ALX_prodev"):
        self.query = query
        self.params = params or ()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute(self.query, self.params)

        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[ERROR] {exc_type}: {exc_val}")
            self.conn.rollback()
        else:
            self.conn.commit()

        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        return False 
