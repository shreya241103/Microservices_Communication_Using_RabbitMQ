import json

def read_products(connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            select_query = f"SELECT * FROM Product;"
            cursor.execute(select_query)
            products = cursor.fetchall()
            cursor.close()

            products_dict = []
            for product in products:
                product_dict = {
                    "Product_ID": product[0],
                    "Product_Name": product[1],
                    "Product_Description": product[2],
                    "Price": product[3]
                }
                products_dict.append(product_dict)

            # Convert list of dictionaries to JSON
            products_json = json.dumps(products_dict, indent=4)

            print("Products Fetched:")
            print(products_json)

            return products_json

    except Exception as e:
        print("Error Fetching Products:", e)
