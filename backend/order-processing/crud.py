import json

def insert_order(connection, order):
    try:
        if connection.is_connected():
            # Insert Order to Database here
            query = f"INSERT INTO Orders VALUES ('{order["order_id"]}')"
            cursor = connection.cursor()
            cursor.execute(query)
            pass

    except Exception as e:
        print("Error Inserting Order:", e)