import ddl
import crud
import pika
import mysql.connector

def database_init():
    try:
        # Connect to MySQL database using host machine's IP address
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root"
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
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="Inventory_DB"
        )
        if connection.is_connected():
            return connection

    except mysql.connector.Error as error:
        print("Failed to connect to MySQL database:", error)

def listen_for_requests():
    print("Listening for requests")

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='requests')
    channel.queue_declare(queue='responses')

    def callback(ch, method, properties, body):
        request = body.decode()
        print("Received message:", request)

        if request == "read_products":
            connection = get_connection()
            if connection:
                products_json = crud.read_products(connection)
                if products_json:
                    print("Sending products to the client")

                    channel.basic_publish(
                        exchange='',
                        routing_key='responses',
                        body=products_json
                    )

    channel.basic_consume(queue='requests', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == "__main__":
    database_init()
    listen_for_requests()
