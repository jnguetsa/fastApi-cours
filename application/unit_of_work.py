from abc import ABC, abstractmethod
from domain.repositories.repository import UserRepository, ProductRepository, OrderRepository

class UnitOfWork(ABC):
    users: UserRepository
    products: ProductRepository
    orders: OrderRepository

    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.rollback()

    @abstractmethod
    async def commit(self):
        pass


    @abstractmethod
    async def rollback(self):
        pass