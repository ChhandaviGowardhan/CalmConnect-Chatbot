#retrival
import mysql.connector
from mysql.connector import Error

# Function to create a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hennessy@3",
            database="calmconnect"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to fetch the diagnosis for a specific username using a join
def get_diagnosis(username: str):
    connection = create_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        # Perform a join to retrieve diagnosis corresponding to the username based on user_id
        query = """
            SELECT d.diagnosis 
            FROM users u
            JOIN diagnosis d ON u.user_id = d.user_id
            WHERE u.username = %s
        """
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result is not None:
            return result[0]  # Return the diagnosis
        else:
            return None  # No result found
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        connection.close()  # Always close the connection