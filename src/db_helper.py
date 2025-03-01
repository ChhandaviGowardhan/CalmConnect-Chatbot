import mysql.connector
from fastapi import HTTPException
import logging

# Database configuration (update these details based on your setup)
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Hennessy@3",  # Your password here
    "database": "calmconnect"  # Your database name here
}

# Test the database connection
def test_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            logging.info("Connected to the database successfully.")
        conn.close()
    except mysql.connector.Error as err:
        logging.error(f"Database connection failed: {err}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {err}")

def insert_user(username: str, password: str):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        logging.info("Database connected, attempting to insert data.")
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        logging.info("Data inserted successfully.")
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
