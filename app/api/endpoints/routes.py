# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy import select, update
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import joinedload
#
# from my_project.app.api.shemas.routes import AverageDelayResponse, RouteOut, CreateRoute
# from my_project.app.crud.routes import CRUDRoutes
# from my_project.app.db.initial_models import Schedule, Route
# from my_project.app.db.session import get_db
# from fastapi_pagination.ext.sqlalchemy import paginate
# from fastapi_pagination import Page
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api.shemas.routes import RouteOut, AverageDelayResponse, DetailedRouteOut
from app.crud.routes import CRUDRoutes, crud_routes
from app.db.initial_models import Schedule, Route
from app.db.session import get_db

router = APIRouter()

@router.get("/routes/test")
async def test_endpoint():
    print("right func")
    return "new message hope it works"

@router.get("/routes", response_model=Page[RouteOut]
            )
async def get_routes(
):
    result = await crud_routes.get_all()
    return result


async def get_average_delay(db: AsyncSession, route_id: int):
    result = await db.execute(
        select(Schedule).filter(Schedule.route_id == route_id).order_by(Schedule.departure_time.desc()).limit(10)
    )
    schedules = result.scalars().all()

    total_delay = 0
    count = 0

    for schedule in schedules:
        if schedule.actual_arrival_time:
            dt_actual = datetime.combine(date.today(), schedule.actual_arrival_time)
            dt_expected = datetime.combine(date.today(), schedule.arrival_time)

            delay = (dt_actual - dt_expected).total_seconds() / 60
            total_delay += delay
            count += 1

    return total_delay / count if count > 0 else 0


@router.get("/routes/{route_id}/average-delay", response_model=AverageDelayResponse)
async def get_route_average_delay(route_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Route).where(Route.id == route_id)
    result = await db.execute(query)
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    avg_delay = await get_average_delay(db, route_id)
    return {"route_id": route_id, "route_name": route.name, "average_delay_minutes": avg_delay}


@router.get("/routes/{route_id}", response_model=DetailedRouteOut)
async def get_route(route_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Route).options(joinedload(Route.schedules)).where(Route.id == route_id)
    result = await db.execute(query)
    route = result.unique().scalar_one_or_none()
    avg_delay = await get_average_delay(db, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    result = DetailedRouteOut.model_validate(route)
    result.average_delay_minutes = avg_delay

    return result


# @router.post("/routes", response_model=RouteOut)
# async def create_route(route: CreateRoute, db: AsyncSession = Depends(get_db)):
#     new_route = Route(
#         route_number=route.route_number,
#         name=route.name,
#         distance=route.distance
#     )
#     db.add(new_route)
#     await db.commit()
#     await db.refresh(new_route)
#     return new_route


# @router.put("/routes/{route_id}", response_model=Route)
# async def update_route(route_id: int, route: CreateRoute, db: AsyncSession = Depends(get_db)):
#     stmt = (
#         update(Route)
#         .where(Route.id == route_id)
#         .values(**route.model_dump(exclude_unset=True))
#         .execution_options(synchronize_session="fetch")
#     )
#
#     result = await db.execute(stmt)
#     await db.commit()
#
#     if result.rowcount == 0:
#         raise HTTPException(status_code=404, detail="Route not found")
#
#     updated_route = await db.execute(select(Route).where(Route.id == route_id))
#     return updated_route.scalars().first()


# @router.delete("/routes/{route_id}")
# async def delete_route(route_id: int, db: AsyncSession = Depends(get_db)):
#     query = select(Route).where(Route.id == route_id)
#     result = await db.execute(query)
#     existing_route = result.scalars().first()
#     if not existing_route:
#         raise HTTPException(status_code=404, detail="Route not found")
#
#     await db.delete(existing_route)
#     await db.commit()
#     return {"detail": "Route deleted"}