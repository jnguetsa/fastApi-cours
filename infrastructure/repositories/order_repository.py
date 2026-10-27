from sqlalchemy import select
from sqlalchemy.orm import selectinload
from domain.entities.entities import Order, OrderItem
from domain.repositories.repository import OrderRepository
from infrastructure.db.models import OrderModel, OrderItemModel

def _to_entity(m: OrderModel) -> Order:
    return Order(
        id=m.id, user_id=m.user_id, status=m.status,
        items=[OrderItem(i.product_id, i.quantity, i.unit_price) for i in m.items],
    )

class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session):
        self.session = session

    async def add(self, order: Order) -> Order:
        model = OrderModel(
            user_id=order.user_id, status=order.status,
            items=[OrderItemModel(product_id=i.product_id, quantity=i.quantity,
                                  unit_price=i.unit_price) for i in order.items],
        )
        self.session.add(model)
        await self.session.flush()
        order.id = model.id
        return order

    async def get(self, order_id: int) -> Order | None:
        stmt = (select(OrderModel).where(OrderModel.id == order_id)
                .options(selectinload(OrderModel.items)))     # obligatoire en async
        m = (await self.session.execute(stmt)).scalar_one_or_none()
        return _to_entity(m) if m else None