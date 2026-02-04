import mysql.connector
from mysql.connector import Error
import os

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'ecommerce_db'),
            autocommit=True
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """Execute a query and optionally fetch results"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        else:
            last_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return last_id
    except Error as e:
        print(f"Database error: {e}")
        if connection:
            connection.close()
        return None

def execute_one(query, params=None):
    """Execute a query and fetch one result"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    except Error as e:
        print(f"Database error: {e}")
        if connection:
            connection.close()
        return None
