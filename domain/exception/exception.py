class DomainError(Exception):
    pass
class UserAlreadyExists(DomainError):
    pass
class UserNotFound(DomainError):
    pass
class ProductNotFound(DomainError):
    pass
class InvalidQuantity(DomainError):
    pass