import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import create_connection

# ================= LOGIN STATE =================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login(username, password):

    connection = create_connection()

    cursor = connection.cursor()

    query = """
    SELECT *
    FROM users
    WHERE username = %s
    AND password = %s
    """

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    connection.close()

    return user

st.set_page_config(
    page_title="Inventory Dashboard",
    layout="wide"
)
# ================= LOGIN PAGE =================

if not st.session_state.logged_in:

    st.title("🔐 Inventory System Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login(username, password)

        if user:

            st.session_state.logged_in = True

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error("Invalid Username or Password")

# ================= MAIN DASHBOARD =================
else:
     st.title("📦 Smart Inventory Management System")

    # Sidebar
     st.sidebar.title("Navigation")

     page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Products", "Analytics"]
    )

     connection = create_connection()

    # ================= DASHBOARD =================
     if page == "Dashboard":

        st.header("📊 Dashboard Overview")

        cursor = connection.cursor()

        # Revenue
        cursor.execute(
            "SELECT SUM(total_amount) FROM orders"
        )

        revenue = cursor.fetchone()[0]

        # Product count
        cursor.execute(
            "SELECT COUNT(*) FROM products"
        )

        total_products = cursor.fetchone()[0]

        # Orders count
        cursor.execute(
            "SELECT COUNT(*) FROM orders"
        )

        total_orders = cursor.fetchone()[0]

        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Revenue", f"₹{revenue}")
        col2.metric("📦 Products", total_products)
        col3.metric("🛒 Orders", total_orders)

    # ================= PRODUCTS =================
     elif page == "Products":

        st.header("📦 Product Inventory")

        # ================= ADD PRODUCT =================
        st.subheader("➕ Add New Product")

        with st.form("product_form"):

            name = st.text_input("Product Name")
            category = st.text_input("Category")
            price = st.number_input(
                "Price",
                min_value=0.0
            )

            stock = st.number_input(
                "Stock Quantity",
                min_value=0
            )

            # Fetch suppliers
            cursor = connection.cursor()

            cursor.execute(
                "SELECT supplier_id, supplier_name FROM suppliers"
        )

            suppliers = cursor.fetchall()

            supplier_dict = {
                supplier[1]: supplier[0]
                for supplier in suppliers
        }

            selected_supplier = st.selectbox(
                "Select Supplier",
                list(supplier_dict.keys())
        )

            supplier_id = supplier_dict[selected_supplier]

            submit = st.form_submit_button(
                "Add Product"
            )

            if submit:

                cursor = connection.cursor()

                query = """
                INSERT INTO products
                (name, category, price, stock_quantity, supplier_id)
                VALUES (%s, %s, %s, %s, %s)
                """

                values = (
                    name,
                    category,
                    price,
                    stock,
                    supplier_id
                )

                cursor.execute(query, values)

                connection.commit()

                st.success("✅ Product Added Successfully!")

        # ================= VIEW PRODUCTS =================
        st.subheader("📋 Available Products")

        query = "SELECT * FROM products"

        df = pd.read_sql(query, connection)

        st.dataframe(df)

    # ================= ANALYTICS =================
     elif page == "Analytics":

        st.header("📈 Sales Analytics")

        # Top selling products
        query = """
        SELECT products.name,
            SUM(order_items.quantity) AS total_sold
        FROM order_items
        JOIN products
        ON order_items.product_id = products.product_id
        GROUP BY products.name
        ORDER BY total_sold DESC
        """

        sales_df = pd.read_sql(query, connection)

        st.subheader("Top Selling Products")

        st.dataframe(sales_df)

        # Chart
        fig, ax = plt.subplots()

        ax.bar(
            sales_df["name"],
            sales_df["total_sold"]
        )

        ax.set_xlabel("Products")
        ax.set_ylabel("Units Sold")
        ax.set_title("Top Selling Products")

        st.pyplot(fig)

        # Low stock alerts
        low_stock_query = """
        SELECT name, stock_quantity
        FROM products
        WHERE stock_quantity < 10
        """

        low_stock_df = pd.read_sql(
            low_stock_query,
            connection
        )

        st.subheader("⚠️ Low Stock Alerts")

        st.dataframe(low_stock_df)

     connection.close()