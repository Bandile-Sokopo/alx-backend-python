import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error,errorcode
import csv
import uuid

config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
}

def connect_db():
    try:
        with connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: ")
        ) as connection:
            print(connection)
    except Error as e:
        print(e)

def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
    finally:
        cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(database="ALX_prodev", **config)


def create_table(connection):
    cursor = connection.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age DECIMAL(3,0) NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        print("Table user_data created or already exists.")
    finally:
        cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s", (data['email'],))
        if cursor.fetchone()[0] == 0:
            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                str(uuid.uuid4()),
                data['name'],
                data['email'],
                data['age']
            ))
            connection.commit()
            print(f"Inserted: {data['name']} ({data['email']})")
        else:
            print(f"Skipped duplicate: {data['email']}")
    finally:
        cursor.close()