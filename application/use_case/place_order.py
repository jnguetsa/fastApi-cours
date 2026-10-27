from dataclasses import dataclass
from domain.entities.entities import Order
from domain.exception.exception import UserNotFound, ProductNotFound
from application.unit_of_work import UnitOfWork

@dataclass
class OrderLine:
    product_id: int
    quantity: int

@dataclass
class PlaceOrderCommand:
    user_id: int
    lines: list[OrderLine]

class PlaceOrder:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, cmd: PlaceOrderCommand) -> Order:
        async with self.uow:
            if not await self.uow.users.get(cmd.user_id):
                raise UserNotFound(cmd.user_id)

            order = Order(user_id=cmd.user_id)
            for line in cmd.lines:
                product = await self.uow.products.get(line.product_id)
                if not product:
                    raise ProductNotFound(line.product_id)
                order.add_item(product.id, line.quantity, product.price)  # prix figé

            order = await self.uow.orders.add(order)
            await self.uow.commit()      # tout ou rien
            return order