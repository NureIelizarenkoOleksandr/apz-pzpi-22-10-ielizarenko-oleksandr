from fastapi import FastAPI, APIRouter, Request
from fastapi_pagination import add_pagination
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi.middleware.cors import CORSMiddleware


from app.api.core.config import settings
from app.api.endpoints import schedule, routes, auth
from app.db.initial_models import User, StopTime, Schedule, RouteStop, Stop, Route, Vehicle
from app.db.session import engine


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"token": "authenticated"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("token") == "authenticated"

api_router = APIRouter()

api_router.include_router(schedule.router, tags=["schedule"], prefix="/schedule")
api_router.include_router(routes.router, tags=["routes"], prefix="/routes")
api_router.include_router(auth.router, tags=["auth"])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

add_pagination(app)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(app, engine, authentication_backend=authentication_backend)


class VehicleAdmin(ModelView, model=Vehicle):
    column_list = [Vehicle.id, Vehicle.vehicle_type, Vehicle.registration_number, Vehicle.brand, Vehicle.model, Vehicle.capacity]
    column_searchable_list = [Vehicle.vehicle_type, Vehicle.registration_number, Vehicle.brand, Vehicle.model]
    form_excluded_columns = [Vehicle.id, Vehicle.schedules]

class RouteAdmin(ModelView, model=Route):
    column_list = [Route.id, Route.route_number, Route.name, Route.distance]
    column_searchable_list = [Route.route_number, Route.name]
    form_excluded_columns = [Route.id]

class StopAdmin(ModelView, model=Stop):
    column_list = [Stop.id, Stop.name, Stop.latitude, Stop.longitude]
    column_searchable_list = [Stop.name]
    form_excluded_columns = [Stop.id]

class RouteStopAdmin(ModelView, model=RouteStop):
    column_list = [RouteStop.id, RouteStop.route_id, RouteStop.stop_id, RouteStop.stop_order]
    form_excluded_columns = [RouteStop.id]

class ScheduleAdmin(ModelView, model=Schedule):
    column_list = [
        Schedule.id,
        Schedule.route_id,
        Schedule.vehicle_id,
        Schedule.departure_time,
        Schedule.arrival_time,
        Schedule.actual_arrival_time,
        Schedule.delay_minutes,
    ]
    column_searchable_list = []  # Можно добавить, если нужно
    form_excluded_columns = [Schedule.id]


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.username]
    column_searchable_list = [User.email, User.username]
    form_excluded_columns = [User.id]

class StopTimeAdmin(ModelView, model=StopTime):
    column_list = [
        StopTime.id,
        StopTime.schedule_id,
        StopTime.stop_id,
        StopTime.arrival_time,
        StopTime.departure_time,
        StopTime.stop_order,
    ]
    form_excluded_columns = [StopTime.id]

admin.add_view(VehicleAdmin)
admin.add_view(RouteAdmin)
admin.add_view(StopAdmin)
admin.add_view(RouteStopAdmin)
admin.add_view(ScheduleAdmin)
admin.add_view(UserAdmin)
admin.add_view(StopTimeAdmin)
