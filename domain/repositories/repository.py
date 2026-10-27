# contrats, pas d'implémentation
from abc import ABC, abstractmethod
from domain.entities.entities import User, Product, Order

class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> User:
        pass
    @abstractmethod
    async def get(self, user_id: int) -> User | None:
        pass
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass
class ProductRepository(ABC):
    @abstractmethod
    async def get(self, product_id: int) -> Product | None:
        pass

class OrderRepository(ABC):
    @abstractmethod
    async def add(self, order: Order) -> Order:
        pass
    @abstractmethod
    async def get(self, order_id: int) -> Order | None:
        pass