import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import create_connection

st.set_page_config(
    page_title="Inventory Dashboard",
    layout="wide"
)

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