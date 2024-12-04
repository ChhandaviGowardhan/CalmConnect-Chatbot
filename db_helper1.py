#feeling updation
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
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to insert the feeling into the diagnosis table
def insert_diagnosis(feeling: str):
    connection = create_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        # Insert the feeling into the diagnosis table
        query = "INSERT INTO diagnosis (diagnosis) VALUES (%s)"
        cursor.execute(query, (feeling,))
        connection.commit()  # Commit the changes
        return cursor.rowcount > 0  # Return True if at least one row was inserted
    except Error as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        cursor.close()
        connection.close()  # Always close the connection