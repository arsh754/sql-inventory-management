from db import create_connection
from db import create_connection

def view_products():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM products"
    cursor.execute(query)

    products = cursor.fetchall()

    print("\nAvailable Products:")
    print("---------------------")

    for product in products:
        print(product)

    connection.close()


def add_product():
    connection = create_connection()
    cursor = connection.cursor()

    name = input("Enter product name: ")
    category = input("Enter category: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock quantity: "))
    supplier_id = int(input("Enter supplier ID: "))

    query = """
    INSERT INTO products
    (name, category, price, stock_quantity, supplier_id)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (name, category, price, stock, supplier_id)

    cursor.execute(query, values)
    connection.commit()

    print("\nProduct added successfully!")

    connection.close()

def place_order():
    connection = create_connection()
    cursor = connection.cursor()

    customer_id = int(input("Enter customer ID: "))
    product_id = int(input("Enter product ID: "))
    quantity = int(input("Enter quantity: "))

    # Get product price and stock
    cursor.execute(
        "SELECT price, stock_quantity FROM products WHERE product_id = %s",
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:
        print("Product not found!")
        return

    price, stock = product

    if quantity > stock:
        print("Not enough stock available!")
        return

    subtotal = price * quantity

    # Create order
    cursor.execute(
        """
        INSERT INTO orders (customer_id, order_date, total_amount)
        VALUES (%s, CURDATE(), %s)
        """,
        (customer_id, subtotal)
    )

    order_id = cursor.lastrowid

    # Add order item
    cursor.execute(
        """
        INSERT INTO order_items
        (order_id, product_id, quantity, subtotal)
        VALUES (%s, %s, %s, %s)
        """,
        (order_id, product_id, quantity, subtotal)
    )

    # Reduce stock
    cursor.execute(
        """
        UPDATE products
        SET stock_quantity = stock_quantity - %s
        WHERE product_id = %s
        """,
        (quantity, product_id)
    )

    connection.commit()

    print("\nOrder placed successfully!")
    print(f"Total Amount: ₹{subtotal}")

    connection.close()

def sales_analytics():
    connection = create_connection()
    cursor = connection.cursor()

    print("\n===== SALES ANALYTICS =====")

    # Total revenue
    cursor.execute(
        "SELECT SUM(total_amount) FROM orders"
    )

    revenue = cursor.fetchone()[0]

    print(f"\nTotal Revenue: ₹{revenue}")

    # Top selling products
    cursor.execute(
        """
        SELECT products.name,
               SUM(order_items.quantity) AS total_sold
        FROM order_items
        JOIN products
        ON order_items.product_id = products.product_id
        GROUP BY products.name
        ORDER BY total_sold DESC
        """
    )

    results = cursor.fetchall()

    print("\nTop Selling Products:")
    print("----------------------")

    for row in results:
        print(f"{row[0]} → {row[1]} sold")

    # Low stock products
    cursor.execute(
        """
        SELECT name, stock_quantity
        FROM products
        WHERE stock_quantity < 10
        """
    )

    low_stock = cursor.fetchall()

    print("\nLow Stock Alerts:")
    print("------------------")

    if low_stock:
        for item in low_stock:
            print(f"{item[0]} → Only {item[1]} left")
    else:
        print("No low stock items.")

    connection.close()