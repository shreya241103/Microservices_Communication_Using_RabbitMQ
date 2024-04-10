import ddl
import crud
import mysql.connector

def database_init():
    try:
        # Connect to MySQL database using host machine's IP address
        connection = mysql.connector.connect(
            host="host.docker.internal",
            port=3406,
            user="root",
            password="password"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            ddl.create_db_if_not_exists( connection, "Inventory_DB")

    except mysql.connector.Error as error:
        print("Failed to connect to MySQL Server:", error)

def get_connection():
    try:
        # Connect to MySQL database using host machine's IP address
        connection = mysql.connector.connect(
            host="host.docker.internal",
            port=3406,
            user="root",
            password="password",
            database="Inventory_DB"
        )
        if connection.is_connected():
            return connection

    except mysql.connector.Error as error:
        print("Failed to connect to MySQL database:", error)

def listen_for_requests():
    print("Listening for requests")

if __name__ == "__main__":
    database_init()
    conn = get_connection()
    listen_for_requests()
