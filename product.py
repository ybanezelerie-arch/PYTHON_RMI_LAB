"""Product data model for the Pyro5 distributed-system lab."""

from dataclasses import asdict, dataclass
from typing import Dict, Any


@dataclass
class Product:
    """Represents a product stored by the remote service."""

    product_id: int
    name: str
    price: float
    stock: int

    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dictionary that Pyro5 can serialize easily."""
        return asdict(self)


# Sample data shared by the server implementation.
DEFAULT_PRODUCTS = [
    Product(1, "Keyboard", 750.00, 12),
    Product(2, "Mouse", 350.00, 20),
    Product(3, "USB Flash Drive", 280.00, 15),
]
