from sqlalchemy import Column, Integer, String, Float, ForeignKey, Time
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vehicle_type = Column(String, nullable=False)
    registration_number = Column(String, unique=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

    schedules = relationship("Schedule", back_populates="vehicle")


class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    route_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    distance = Column(Float, nullable=False)
    schedules = relationship("Schedule", back_populates="route")



class Stop(Base):
    __tablename__ = "stops"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class RouteStop(Base):
    __tablename__ = "route_stops"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    stop_id = Column(Integer, ForeignKey("stops.id"), nullable=False)
    stop_order = Column(Integer, nullable=False)


class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    departure_time = Column(Time, nullable=False)
    arrival_time = Column(Time, nullable=False)

    actual_arrival_time = Column(Time, nullable=True)
    delay_minutes = Column(Integer, nullable=True)

    vehicle = relationship("Vehicle", back_populates="schedules")
    route = relationship("Route", back_populates="schedules")
    stop_times = relationship("StopTime", back_populates="schedule", cascade="all, delete-orphan")

    def calculate_delay(self):
        if self.actual_arrival_time:
            planned_minutes = (self.arrival_time.hour * 60 + self.arrival_time.minute)
            actual_minutes = (self.actual_arrival_time.hour * 60 + self.actual_arrival_time.minute)
            self.delay_minutes = actual_minutes - planned_minutes
            return self.delay_minutes
        return 0

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)


class StopTime(Base):
    __tablename__ = "stop_times"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    stop_id = Column(Integer, ForeignKey("stops.id"), nullable=False)
    arrival_time = Column(Time, nullable=False)
    departure_time = Column(Time, nullable=False)
    stop_order = Column(Integer, nullable=False)

    schedule = relationship("Schedule", back_populates="stop_times")
    stop = relationship("Stop")