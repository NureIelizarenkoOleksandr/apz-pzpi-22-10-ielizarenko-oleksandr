from fastapi import FastAPI, APIRouter
from fastapi_pagination import add_pagination

from app.api.endpoints import schedule, routes

api_router = APIRouter()

api_router.include_router(schedule.router, tags=["schedule"], prefix="/schedule")
api_router.include_router(routes.router, tags=["routes"], prefix="/routes")

app = FastAPI()

app.include_router(api_router)

add_pagination(app)