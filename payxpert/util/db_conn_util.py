import mysql.connector
from exception.database_connection_exception import DatabaseConnectionException

def get_connection():
    try:
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="payrole"
        )
    except mysql.connector.Error as e:
        raise DatabaseConnectionException(f"Error connecting to the database: {e}")