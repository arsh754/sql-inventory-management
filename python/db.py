import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Arsh@1234",
        database="inventory_system"
    )

    return connection