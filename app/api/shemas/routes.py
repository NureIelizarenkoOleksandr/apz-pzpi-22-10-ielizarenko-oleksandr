from datetime import time
from pydantic import BaseModel


class AverageDelayResponse(BaseModel):
    route_id: int
    average_delay_minutes: float


class BaseSchedulesOut(BaseModel):
    id: int
    vehicle_id: int
    departure_time: time
    arrival_time: time


class RouteOut(BaseModel):
    id: int
    name: str
    schedules: list[BaseSchedulesOut]

class DetailedRouteOut(RouteOut):
    route_number: str
    distance: float
    schedules: list[BaseSchedulesOut]


class CreateRoute(DetailedRouteOut):
    pass