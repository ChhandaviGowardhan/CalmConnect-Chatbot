# Feeling Updation
import mysql.connector
from mysql.connector import Error

# Function to create a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hennessy@3",  # Replace with your actual password
            database="calmconnect"  # Ensure this is the correct database
        )
        if connection.is_connected():
            print("Connection established successfully.")  # Debug log
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to insert the feeling into the diagnosis table
def insert_diagnosis(feeling: str):
    if not feeling:  # Ensure the feeling is not empty or None
        print("Invalid input: feeling is empty or None.")
        return False

    connection = create_connection()
    if connection is None:
        print("Database connection failed.")
        return False

    try:
        cursor = connection.cursor()
        # Insert the feeling into the diagnosis table
        query = "INSERT INTO diagnosis (diagnosis) VALUES (%s)"
        print(f"Executing query: {query} with value: {feeling}")  # Debug log
        cursor.execute(query, (feeling,))
        connection.commit()  # Commit the changes
        print(f"Rows affected: {cursor.rowcount}")  # Confirm rows affected
        return cursor.rowcount > 0  # Return True if at least one row was inserted
    except Error as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()  # Always close the connection
