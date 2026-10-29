"""Pyro5 server exposing a remote ProductService object."""

from threading import Lock

import Pyro5.api

from product import DEFAULT_PRODUCTS


@Pyro5.api.expose
class ProductService:
    """Remote methods that clients can invoke over the network."""

    def __init__(self):
        self._products = {p.product_id: p for p in DEFAULT_PRODUCTS}
        self._lock = Lock()

    def list_products(self):
        """Return all products as dictionaries."""
        with self._lock:
            return [p.to_dict() for p in self._products.values()]

    def get_product(self, product_id):
        """Return one product, or None when its ID does not exist."""
        with self._lock:
            product = self._products.get(int(product_id))
            return product.to_dict() if product else None

    def add_product(self, product_id, name, price, stock):
        """Add a product; return a status message."""
        product_id = int(product_id)
        with self._lock:
            if product_id in self._products:
                return {"success": False, "message": "Product ID already exists."}
            if not str(name).strip():
                return {"success": False, "message": "Product name cannot be empty."}
            if float(price) < 0 or int(stock) < 0:
                return {"success": False, "message": "Price and stock cannot be negative."}
            from product import Product
            product = Product(product_id, str(name).strip(), float(price), int(stock))
            self._products[product_id] = product
            return {"success": True, "message": "Product added successfully.", "product": product.to_dict()}

    def update_stock(self, product_id, quantity):
        """Set a product's stock quantity."""
        product_id, quantity = int(product_id), int(quantity)
        with self._lock:
            product = self._products.get(product_id)
            if product is None:
                return {"success": False, "message": "Product not found."}
            if quantity < 0:
                return {"success": False, "message": "Stock cannot be negative."}
            product.stock = quantity
            return {"success": True, "message": "Stock updated.", "product": product.to_dict()}


def main():
    host = "0.0.0.0"  # Listen on all network interfaces; use localhost for same-computer testing.
    port = 9090
    object_id = "product.service"

    daemon = Pyro5.api.Daemon(host=host, port=port)
    uri = daemon.register(ProductService(), objectId=object_id)

    print("=" * 56)
    print("PYTHON RMI LAB - PRODUCT SERVER")
    print("Server is running. Keep this terminal open.")
    print(f"Object URI: {uri}")
    print("Client URI for same computer: PYRO:product.service@localhost:9090")
    print("=" * 56)
    try:
        daemon.requestLoop()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        daemon.close()


if __name__ == "__main__":
    main()
