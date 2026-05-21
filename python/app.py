from inventory import view_products, add_product, place_order ,sales_analytics

while True:
    print("\n=================================")
    print(" Inventory Management System ")
    print("=================================")

    print("1. View Products")
    print("2. Add Product")
    print("3. Place Order")
    print("4. sales analytics")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        view_products()

    elif choice == "2":
        add_product()

    elif choice == "3":
        place_order()

    elif choice == "4":
        sales_analytics()
    
    elif choice == "5":
        print("Exiting the system. Goodbye!")
        break
    
    else:
        print("Invalid choice!")