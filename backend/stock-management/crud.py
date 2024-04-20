def order_status(connection, order):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            product_id = order.get("Product_ID", "")
            quantity = order.get("Quantity", 0)  # Assuming default quantity is 0

            # SQL query to check if the given quantity is greater than the quantity in storage
            storage_query = "SELECT Quantity FROM Storage WHERE Product_ID = %s"
            cursor.execute(storage_query, (product_id,))
            storage_quantity = cursor.fetchone()[0]

            # Check if the given quantity is greater than the quantity in storage
            if quantity < storage_quantity:
                result = 'True'
            else:
                result = 'False'
            
            # Commit the transaction
            connection.commit()
            if result == 'True':
                reduce_quantity(connection,product_id,quantity)
            # Return the result
            return result

    except Exception as e:
        print("Error Inserting Order:", e)
        return None
    
def reduce_quantity(connection, product_id, quantity):
    try:
        if connection.is_connected():
            # Define the SQL query to update the quantity in the Storage table
            query = '''
                UPDATE Storage
                SET Quantity = Quantity - %s
                WHERE Product_ID = %s;
            '''
            cursor = connection.cursor()

            # Execute the SQL query with parameters
            cursor.execute(query, (quantity, product_id))

            # Commit the transaction
            connection.commit()
            print("Quantity reduced successfully")

    except Exception as e:
        print("Error reducing quantity:", e)

