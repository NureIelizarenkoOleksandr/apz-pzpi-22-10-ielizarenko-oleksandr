from datetime import datetime, date, time
from random import uniform

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, Session, aliased

from app.api.endpoints.auth import get_current_user
from app.api.shemas.routes import RouteOut, AverageDelayResponse, DetailedRouteOut, CreateRoute
from app.crud.routes import CRUDRoutes, crud_routes
from app.db.initial_models import Schedule, Route, User, StopTime, Stop, Vehicle, RouteStop
from app.db.session import get_db

router = APIRouter()

@router.get("/routes", response_model=Page[RouteOut]
            )
async def get_routes(
    current_user: User = Depends(get_current_user)
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
async def get_route_average_delay(route_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = select(Route).where(Route.id == route_id)
    result = await db.execute(query)
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    avg_delay = await get_average_delay(db, route_id)
    return {"route_id": route_id, "route_name": route.name, "average_delay_minutes": avg_delay}


@router.get("/routes/{route_id}", response_model=DetailedRouteOut)
async def get_route(route_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = select(Route).options(
        joinedload(Route.schedules).joinedload(Schedule.vehicle)
    ).where(Route.id == route_id)
    result = await db.execute(query)
    route = result.unique().scalar_one_or_none()
    print(route.__dict__["schedules"][0].__dict__)
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
#
#
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
#
#
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

@router.get("/departures-between-stops/{from_stop_name}/{to_stop_name}")
async def get_departures_between_stops(
    from_stop_name: str,
    to_stop_name: str,
    db: AsyncSession = Depends(get_db),
):
    now = datetime.now().time()
    ST1 = aliased(StopTime)
    ST2 = aliased(StopTime)

    to_stop_id_subq = select(Stop.id).where(Stop.name == to_stop_name).scalar_subquery()

    stmt = (
        select(Schedule, ST1, ST2, Route, Vehicle)
        .join(ST1, Schedule.stop_times)
        .join(ST2, Schedule.stop_times)
        .join(Route, Schedule.route_id == Route.id)
        .join(Vehicle, Schedule.vehicle_id == Vehicle.id)
        .join(Stop, ST1.stop_id == Stop.id)
        .where(
            Stop.name == from_stop_name,
            ST2.stop_id == to_stop_id_subq,
            # ST1.schedule_id == ST2.schedule_id,
            ST1.stop_order < ST2.stop_order,
        )
        .order_by(ST1.departure_time)
    )

    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            "route_name": route.name,
            "route_number": route.route_number,
            "vehicle_id": vehicle.id,
            "vehicle_name": f"{vehicle.vehicle_type} {vehicle.brand} {vehicle.model}",
            "from_stop_time": st1.departure_time,
            "to_stop_time": st2.arrival_time,
        }
        for schedule, st1, st2, route, vehicle in rows
    ]

CITIES = {
    1: {"name": "Kyiv", "lat_min": 50.35, "lat_max": 50.52, "lon_min": 30.4, "lon_max": 30.65},
    2: {"name": "Lviv", "lat_min": 49.78, "lat_max": 49.88, "lon_min": 23.9, "lon_max": 24.1},
}

@router.get("/vehicle/{vehicle_id}/location")
def get_random_location(vehicle_id: int):
    city = CITIES.get(vehicle_id)
    if not city:
        return {"error": "City not found"}

    lat = uniform(city["lat_min"], city["lat_max"])
    lon = uniform(city["lon_min"], city["lon_max"])

    res = {
        "city": city["name"],
        "lat": lat,
        "lng": lon,
    }

    print(res)
    return res