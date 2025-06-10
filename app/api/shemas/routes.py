from datetime import time
from pydantic import BaseModel


class AverageDelayResponse(BaseModel):
    route_id: int
    route_name: str
    average_delay_minutes: float


class VehicleOut(BaseModel):
    vehicle_type: str
    registration_number: str
    brand: str
    model: str
    capacity: int

    model_config = {
        "from_attributes": True
    }


class BaseSchedulesOut(BaseModel):
    id: int
    vehicle_id: int
    departure_time: time
    arrival_time: time

    vehicle: VehicleOut = None

    model_config = {
        "from_attributes": True
    }


class RouteOut(BaseModel):
    id: int
    name: str
    schedules: list[BaseSchedulesOut]

    model_config = {
        "from_attributes": True
    }



class DetailedRouteOut(RouteOut):
    route_number: str
    distance: float
    schedules: list[BaseSchedulesOut]
    average_delay_minutes: float = None

    model_config = {
        "from_attributes": True
    }


class CreateRoute(DetailedRouteOut):
    pass