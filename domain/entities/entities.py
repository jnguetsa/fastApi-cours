from dataclasses import dataclass, field
from decimal import Decimal
from domain.exception.exception import InvalidQuantity

@dataclass
class User:
    email: str
    full_name: str
    id: int | None = None

@dataclass
class Product:
    name: str
    price: Decimal
    id: int | None = None

@dataclass
class OrderItem:
    product_id: int
    quantity: int
    unit_price: Decimal

@dataclass
class Order:
    user_id: int
    items: list[OrderItem] = field(default_factory=list)
    status: str = "PENDING"
    id: int | None = None

    def add_item(self, product_id: int, quantity: int, unit_price: Decimal) -> None:
        if quantity <= 0:
            raise InvalidQuantity("La quantité doit être positive")
        self.items.append(OrderItem(product_id, quantity, unit_price))   # la règle métier vit ici

    @property
    def total(self) -> Decimal:
        return sum((i.unit_price * i.quantity for i in self.items), Decimal("0"))