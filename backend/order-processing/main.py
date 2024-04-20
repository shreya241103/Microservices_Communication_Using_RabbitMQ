import os
import crud
import pika
import json
import mysql.connector

port = 3406
password = "password"
print("Order Processing Microservice Running")

def get_connection():
    try:
        # Connect to MySQL database using host machine's IP address
        connection = mysql.connector.connect(
            host = "host.docker.internal",
            port = port,
            user = "root",
            password = password,
            database = "Inventory_DB"
        )
        if connection.is_connected():
            return connection

    except mysql.connector.Error as error:
        print("Failed to connect to MySQL database:", error)

def listen_for_requests():
    print("Database Read Service Listening for Requests..")

    amqp_url = os.environ['AMQP_URL']
    url_params = pika.URLParameters(amqp_url)

    rabbitmq_connection = pika.BlockingConnection(url_params)
    channel = rabbitmq_connection.channel()

    channel.queue_declare(queue='New_Order')
    channel.queue_declare(queue='CheckStock')

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print("Received message:", message)

        order = { "order_id": "", "customer_id": ""}

        connection = get_connection()
        if connection:
            # Insert Order to DB
            print("Sending order info to stock management")

            crud.insert_order(connection, order)
            # Data give to stock
            data_to_publish = ""

            # Publish message to CheckStock Queue
            channel.basic_publish(
                exchange='',
                routing_key='CheckStock',
                body=data_to_publish
            )

    channel.basic_consume(queue='New_Order', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages...')
    channel.start_consuming()

if __name__ == "__main__":
    listen_for_requests()
