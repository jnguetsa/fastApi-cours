from fastapi import Depends
from infrastructure.db.session import SessionFactory
from infrastructure.db.uow import SqlAlchemyUnitOfWork
from application.use_case.use_case_regiter_user import RegisterUser
from application.use_case.place_order import PlaceOrder

def get_uow() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(SessionFactory)

def get_register_user(uow=Depends(get_uow)) -> RegisterUser:
    return RegisterUser(uow)

def get_place_order(uow=Depends(get_uow)) -> PlaceOrder:
    return PlaceOrder(uow)