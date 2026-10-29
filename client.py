"""Command-line client for the remote Pyro5 ProductService."""

import Pyro5.api

DEFAULT_URI = "PYRO:product.service@localhost:9090"


def show_products(service):
    products = service.list_products()
    print("\nPRODUCT CATALOG")
    print("-" * 62)
    print(f"{'ID':<6}{'NAME':<24}{'PRICE':>12}{'STOCK':>10}")
    print("-" * 62)
    for p in products:
        print(f"{p['product_id']:<6}{p['name']:<24}{p['price']:>12.2f}{p['stock']:>10}")
    print("-" * 62)


def main():
    uri = input(f"Enter server URI [{DEFAULT_URI}]: ").strip() or DEFAULT_URI
    try:
        with Pyro5.api.Proxy(uri) as service:
            print("\nConnected to remote ProductService.")
            while True:
                print("\n===== PRODUCT CLIENT MENU =====")
                print("1. List all products")
                print("2. Find product by ID")
                print("3. Add product")
                print("4. Update product stock")
                print("0. Exit")
                choice = input("Choose an option: ").strip()

                if choice == "1":
                    show_products(service)
                elif choice == "2":
                    product_id = input("Product ID: ").strip()
                    product = service.get_product(product_id)
                    if product:
                        print("Product found:", product)
                    else:
                        print("Product not found.")
                elif choice == "3":
                    try:
                        product_id = int(input("New product ID: "))
                        name = input("Product name: ")
                        price = float(input("Price: "))
                        stock = int(input("Stock quantity: "))
                        result = service.add_product(product_id, name, price, stock)
                        print(result["message"])
                        if result.get("product"):
                            print("Added:", result["product"])
                    except ValueError:
                        print("Invalid input. ID and stock must be whole numbers; price must be numeric.")
                elif choice == "4":
                    try:
                        product_id = int(input("Product ID: "))
                        stock = int(input("New stock quantity: "))
                        result = service.update_stock(product_id, stock)
                        print(result["message"])
                        if result.get("product"):
                            print("Updated:", result["product"])
                    except ValueError:
                        print("Enter a valid whole number for product ID and stock.")
                elif choice == "0":
                    print("Client disconnected. Goodbye!")
                    break
                else:
                    print("Invalid option. Please choose 0, 1, 2, 3, or 4.")
    except Exception as exc:
        print("Could not connect to the server.")
        print("Check that server.py is running and that the URI and port are correct.")
        print(f"Details: {exc}")


if __name__ == "__main__":
    main()
