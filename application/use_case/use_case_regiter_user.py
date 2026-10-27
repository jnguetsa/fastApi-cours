from dataclasses import dataclass
from domain.entities.entities import User
from domain.exception.exception import UserAlreadyExists
from application.unit_of_work import UnitOfWork

@dataclass
class RegisterUserCommand:
    email: str
    full_name: str

class RegisterUser:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, cmd: RegisterUserCommand) -> User:
        async with self.uow:
            if await self.uow.users.get_by_email(cmd.email):
                raise UserAlreadyExists(cmd.email)
            user = await self.uow.users.add(User(email=cmd.email, full_name=cmd.full_name))
            await self.uow.commit()
            return user




