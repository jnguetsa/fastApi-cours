from fastapi import Request
from fastapi.responses import JSONResponse
from domain import exception as exc

STATUS = {
    exc.UserAlreadyExists: 409,
    exc.UserNotFound: 404,
    exc.ProductNotFound: 404,
    exc.InvalidQuantity: 422,
}

async def domain_error_handler(request: Request, error: exc.DomainError):
    return JSONResponse(status_code=STATUS.get(type(error), 400), content={"detail": str(error)})