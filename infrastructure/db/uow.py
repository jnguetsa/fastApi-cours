from application.unit_of_work import UnitOfWork
from infrastructure.repositories.order_repository import SqlAlchemyOrderRepository
from infrastructure.repositories.user_repository import SqlAlchemyUserRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = SqlAlchemyUserRepository(self.session)
        self.products = SqlAlchemyProductRepository(self.session)
        self.orders = SqlAlchemyOrderRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await super().__aexit__(exc_type, exc, tb)
        await self.session.close()

    async def commit(self):   await self.session.commit()
    async def rollback(self): await self.session.rollback()