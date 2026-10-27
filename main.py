from fastapi import FastAPI
from domain.exception import DomainError
from presentation.api.error_handlers import domain_error_handler
from presentation.api.routers import users, orders

app = FastAPI(title="Shop API")
app.add_exception_handler(DomainError, domain_error_handler)
app.include_router(users.router)
app.include_router(orders.router)