from sqlalchemy import select

from app.crud.base import CRUDBase
from app.db.initial_models import User

class CRUDUsers(CRUDBase):
    async def get(self, email: str):
        async with self.get_session() as session:
            result = await session.execute(select(User).filter(self.model.email == email))
            return result.scalar_one_or_none()

crud_users = CRUDUsers(User)