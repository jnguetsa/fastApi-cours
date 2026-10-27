from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.entities import User
from domain.repositories.repository import UserRepository
from infrastructure.db.models import UserModel

def _to_entity(m: UserModel) -> User:
    return User(id=m.id, email=m.email, full_name=m.full_name)

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> User:
        model = UserModel(email=user.email, full_name=user.full_name)
        self.session.add(model)
        await self.session.flush()          # récupère l'id généré
        return _to_entity(model)

    async def get(self, user_id: int) -> User | None:
        m = await self.session.get(UserModel, user_id)
        return _to_entity(m) if m else None

    async def get_by_email(self, email: str) -> User | None:
        m = (await self.session.execute(
            select(UserModel).where(UserModel.email == email))).scalar_one_or_none()
        return _to_entity(m) if m else None