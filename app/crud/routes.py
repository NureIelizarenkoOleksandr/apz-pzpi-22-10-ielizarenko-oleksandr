from select import select

from app.api.shemas.routes import CreateRoute
from app.crud.base import CRUDBase
from app.db.initial_models import Route


class CRUDRoutes(CRUDBase):
    async def get(self, id_: int):
        async with self.get_session() as session:
            result = await session.execute(select(Route).filter(self.model.id == id_))
            return result.scalar_one_or_none()



crud_routes = CRUDRoutes(Route)