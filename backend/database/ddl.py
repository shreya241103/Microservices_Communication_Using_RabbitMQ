""" SQL DDL Functions
"""

def create_db_if_not_exists( connection, database):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {database};"
            cursor.execute(create_db_query)
            cursor.close()
            # connection.database = database
            # create_tables_if_not_exist( connection )
            # insert_products(connection)
            print("Database Initialized.")

    except Exception as e:
        print("Error:", e)

def create_tables_if_not_exist(connection):
    create_query = """
        -- CREATE TABLE Client
        CREATE TABLE IF NOT EXISTS Customer(
           Customer_ID VARCHAR(5),                -- Unique identifier for clients
           Name VARCHAR(20) NOT NULL,             -- Client's name (not null)
           Email TEXT NOT NULL,                   -- Client's email (not null)
           Password_client TEXT,                  -- Client's password
           PRIMARY KEY(Customer_ID)               -- Primary key is Client_ID
        );

        -- CREATE TABLE Orders
        CREATE TABLE IF NOT EXISTS Order(
           Client_ID VARCHAR(5),                                  -- Client associated with the order
           Product_ID VARCHAR(5),
           Total_Payment DECIMAL(10, 2),                          -- Total payment for the order
           Order_Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Order placement date with default value
           Status ENUM("In Progress", "Shipped", "Complete"),     -- Order status
           PRIMARY KEY(Client_ID, Order_Timestamp)                -- Primary key is Order_ID
        );

        -- CREATE TABLE Product
        CREATE TABLE IF NOT EXISTS Product(
           Product_ID VARCHAR(5),               -- Unique identifier for products
           Product_Name TEXT,                   -- Name of the product
           Product_Description TEXT,            -- Description of the product
           Price Decimal(10, 2),                -- Price of the product
           PRIMARY KEY (Product_ID)             -- Primary key is Product_ID
        );

        -- CREATE TABLE STORAGE
        CREATE TABLE IF NOT EXISTS STORAGE(
           Product_ID VARCHAR(5),                  -- Part stored in the storage
           Quantity INT,                        -- Quantity of parts in storage
           Threshold INT,                       -- Threshold quantity for restocking
           Restock_Time INT,
           PRIMARY KEY(Product_ID)                -- Primary key is Store_id
        );

        -- CREATE TABLE Admin
        CREATE TABLE IF NOT EXISTS Admin (
            Admin_ID VARCHAR(5) PRIMARY KEY,    -- Unique identifier for admins (primary key)
            password VARCHAR(100)               -- Admin's password
        );

        -- CREATE TABLE SUPPLIER_ORDERS
        CREATE TABLE IF NOT EXISTS RESTOCK_REQUESTS(
           Product_ID VARCHAR(5),
           Date_Time TIMESTAMP,                 -- Date and time of the order
           Status ENUM("In Progress","Shipped",
           "Complete", "Cancelled"),            -- Status of the order
           Quantity INT,                        -- Quantity of parts required from the supplier
           PRIMARY KEY (Product_ID, Date_Time) -- Composite primary key
        );

        -- ADDING CONSTRAINTS

        -- ALTER TABLE RESTOCK_REQUESTS
        ALTER TABLE RESTOCK_REQUESTS
        ADD CONSTRAINT IF NOT EXISTS fk_restock_prod FOREIGN KEY(Product_ID)
        REFERENCES Product(Product_ID) ON DELETE CASCADE ON UPDATE CASCADE;

        -- ALTER TABLE Order
        ALTER TABLE IF EXISTS Order
        ADD CONSTRAINT IF NOT EXISTS fk_order_cust
        FOREIGN KEY(Customer_ID) REFERENCES Customer(Customer_ID) ON DELETE CASCADE ON UPDATE CASCADE,
        ADD CONSTRAINT IF NOT EXISTS fk_order_product FOREIGN KEY(Product_ID) REFERENCES Product(Product_ID);

        -- ALTER TABLE Storage
        ALTER TABLE IF EXISTS Storage
        ADD CONSTRAINT IF NOT EXISTS fk_store_product FOREIGN KEY(Product_ID)
        REFERENCES Product(Product_ID) ON DELETE CASCADE ON UPDATE CASCADE;
    """

    try:
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(create_query, multi=True)
            connection.commit()
            cursor.close()
            print("Tables created successfully.")
    except Exception as e:
        print("Error:", e)


def insert_products( connection ):
    insert_query = """INSERT INTO Product (Product_ID, Product_Name, Product_Description, Price)
                        VALUES
                        ('P0001', 'Toyota Camry', 'The Toyota Camry, a renowned car model, is the perfect blend of style and performance. This car offers a comfortable and efficient driving experience for those seeking both luxury and reliability.', 1825000.00),
                        ('P0002', 'Ford F-150', 'The Ford F-150, is built to handle tough tasks with ease. Its robust build and powerful performance make it the ideal choice for work and adventure enthusiasts who require a dependable and rugged vehicle.', 2555000.00),
                        ('P0003', 'Honda Civic', 'The Honda Civic, a classic car model, is synonymous with reliability and efficiency.Known for its fuel economy and sleek design, this car is a top pick for those who value practicality and style on the road.', 1460000.00),
                        ('P0004', 'Chevrolet Silverado', 'The Chevrolet Silverado, a versatile truck model, is designed to tackle heavy-duty jobs with finesse.With its strong performance and spacious interior, this truck is perfect for individuals who demand power and comfort.', 2190000.00),
                        ('P0005', 'BMW S1000RR', 'The BMW S1000RR is a high-performance sportbike that combines cutting-edge technology with thrilling speed. With its aerodynamic design and powerful engine, its the ultimate choice for motorcycle enthusiasts.', 1500000.00),
                        ('P0006', 'Tesla Model 3', 'The Tesla Model 3 is an electric car that redefines sustainability and style. With its sleek design and advanced autopilot features, it offers a futuristic driving experience for eco-conscious individuals.', 4500000.00),
                        ('P0007', 'Yamaha YZF R6', 'The Yamaha YZF R6 is a sporty and agile motorcycle designed for adrenaline junkies. Its compact size and powerful engine make it perfect for both city commuting and track racing.', 900000.00),
                        ('P0008', 'Honda Accord', 'The Honda Accord is a reliable and stylish sedan known for its fuel efficiency and comfortable ride. With advanced safety features and modern design, its a top choice for those seeking a dependable daily driver.', 2600000.00),
                        ('P0009', 'Ducati Multistrada V4', 'The Ducati Multistrada V4 is an adventure motorcycle built for versatility and performance. With its powerful engine and rugged design, its the perfect option for riders who enjoy both on and off-road journeys.', 2200000.00),
                        ('P0010', 'Toyota Prius', 'The Toyota Prius is a hybrid car that sets the standard for fuel efficiency. With its eco-friendly features and practical design, its a great choice for environmentally conscious drivers.', 2500000.00);
                    """
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Product")
            count = cursor.fetchone()[0]
            if count == 0:  # If Product table is empty, insert data
                cursor.execute(insert_query)
                connection.commit()
                print("Products inserted successfully.")
            cursor.close()
    except Exception as e:
        print("Error:", e)