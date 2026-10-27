from fastapi import APIRouter, Depends, status
from application.use_case.place_order import PlaceOrder, PlaceOrderCommand, OrderLine
from presentation.api.deps import get_place_order
from presentation.api.schemas import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def place_order(body: OrderCreate, use_case: PlaceOrder = Depends(get_place_order)):
    cmd = PlaceOrderCommand(
        user_id=body.user_id,
        lines=[OrderLine(l.product_id, l.quantity) for l in body.lines],
    )
    return await use_case.execute(cmd)