# async def seed_test_data(db):
#     print("adding to db")
#     stops = [
#         Stop(id=1, name="Central Station", latitude=50.4501, longitude=30.5234),
#         Stop(id=2, name="Main Square", latitude=50.4505, longitude=30.5240),
#         Stop(id=3, name="Park", latitude=50.4490, longitude=30.5200),
#         Stop(id=4, name="Airport", latitude=50.4310, longitude=30.5150),
#         Stop(id=5, name="University", latitude=50.4470, longitude=30.5180),
#         Stop(id=6, name="Museum", latitude=50.4480, longitude=30.5210),
#         Stop(id=7, name="Hospital", latitude=50.4495, longitude=30.5225),
#         Stop(id=8, name="Library", latitude=50.4510, longitude=30.5250),
#         Stop(id=9, name="City Hall", latitude=50.4520, longitude=30.5270),
#         Stop(id=10, name="Stadium", latitude=50.4530, longitude=30.5280),
#     ]
#     db.add_all(stops)
#     await db.commit()  # <-- обязательно: фиксируем вставку остановок
#
#     # 2. Добавляем маршруты
#     routes = [
#         Route(id=1, route_number="101", name="Downtown Loop", distance=12.5),
#         Route(id=2, route_number="102", name="Airport Express", distance=25.0),
#         Route(id=3, route_number="103", name="University Shuttle", distance=8.0),
#     ]
#     db.add_all(routes)
#     await db.commit()  # <-- тоже фиксируем
#
#     # 3. Добавляем транспорт
#     vehicles = [
#         Vehicle(id=1, vehicle_type="Bus", registration_number="AB1234CD", brand="Volvo", model="7700", capacity=50),
#         Vehicle(id=2, vehicle_type="Tram", registration_number="TR5678EF", brand="Siemens", model="Avenio",
#                 capacity=120),
#         Vehicle(id=3, vehicle_type="Minibus", registration_number="MB9012GH", brand="Mercedes", model="Sprinter",
#                 capacity=20),
#     ]
#     db.add_all(vehicles)
#     await db.commit()  # фиксируем транспорт
#
#     # 4. Теперь можно безопасно вставлять связи RouteStop
#     route_stops = [
#         # маршрут 1
#         RouteStop(route_id=1, stop_id=1, stop_order=1),
#         RouteStop(route_id=1, stop_id=2, stop_order=2),
#         RouteStop(route_id=1, stop_id=6, stop_order=3),
#         RouteStop(route_id=1, stop_id=7, stop_order=4),
#         RouteStop(route_id=1, stop_id=8, stop_order=5),
#         RouteStop(route_id=1, stop_id=9, stop_order=6),
#         RouteStop(route_id=1, stop_id=10, stop_order=7),
#         RouteStop(route_id=1, stop_id=5, stop_order=8),
#         RouteStop(route_id=1, stop_id=3, stop_order=9),
#         RouteStop(route_id=1, stop_id=1, stop_order=10),
#
#         # маршрут 2
#         RouteStop(route_id=2, stop_id=4, stop_order=1),
#         RouteStop(route_id=2, stop_id=3, stop_order=2),
#         RouteStop(route_id=2, stop_id=2, stop_order=3),
#         RouteStop(route_id=2, stop_id=1, stop_order=4),
#
#         # маршрут 3
#         RouteStop(route_id=3, stop_id=5, stop_order=1),
#         RouteStop(route_id=3, stop_id=6, stop_order=2),
#         RouteStop(route_id=3, stop_id=7, stop_order=3),
#     ]
#     db.add_all(route_stops)
#     await db.commit()
#
#     # Создаём расписания (Schedule) для каждого маршрута и транспортного средства
#     schedules = [
#         Schedule(id=1, route_id=1, vehicle_id=1, departure_time=time(8, 0), arrival_time=time(9, 0)),
#         Schedule(id=2, route_id=1, vehicle_id=2, departure_time=time(10, 0), arrival_time=time(11, 0)),
#         Schedule(id=3, route_id=2, vehicle_id=3, departure_time=time(9, 30), arrival_time=time(10, 30)),
#     ]
#     db.add_all(schedules)
#     await db.commit()
#
#     # Добавляем StopTime для расписаний (с временем прибытия и отправления на каждой остановке)
#     stop_times = [
#         # Schedule 1 (маршрут 1, автобус 1)
#         StopTime(schedule_id=1, stop_id=1, arrival_time=time(8, 0), departure_time=time(8, 5), stop_order=1),
#         StopTime(schedule_id=1, stop_id=2, arrival_time=time(8, 15), departure_time=time(8, 20), stop_order=2),
#         StopTime(schedule_id=1, stop_id=6, arrival_time=time(8, 30), departure_time=time(8, 35), stop_order=3),
#         StopTime(schedule_id=1, stop_id=7, arrival_time=time(8, 45), departure_time=time(8, 50), stop_order=4),
#         StopTime(schedule_id=1, stop_id=8, arrival_time=time(9, 0), departure_time=time(9, 5), stop_order=5),
#
#         # Schedule 2 (маршрут 1, трамвай 2)
#         StopTime(schedule_id=2, stop_id=1, arrival_time=time(10, 0), departure_time=time(10, 5), stop_order=1),
#         StopTime(schedule_id=2, stop_id=2, arrival_time=time(10, 15), departure_time=time(10, 20), stop_order=2),
#         StopTime(schedule_id=2, stop_id=6, arrival_time=time(10, 30), departure_time=time(10, 35), stop_order=3),
#         StopTime(schedule_id=2, stop_id=7, arrival_time=time(10, 45), departure_time=time(10, 50), stop_order=4),
#         StopTime(schedule_id=2, stop_id=8, arrival_time=time(11, 0), departure_time=time(11, 5), stop_order=5),
#
#         # Schedule 3 (маршрут 2, минибас 3)
#         StopTime(schedule_id=3, stop_id=4, arrival_time=time(9, 30), departure_time=time(9, 35), stop_order=1),
#         StopTime(schedule_id=3, stop_id=3, arrival_time=time(9, 50), departure_time=time(9, 55), stop_order=2),
#         StopTime(schedule_id=3, stop_id=2, arrival_time=time(10, 10), departure_time=time(10, 15), stop_order=3),
#         StopTime(schedule_id=3, stop_id=1, arrival_time=time(10, 30), departure_time=time(10, 35), stop_order=4),
#     ]
#     db.add_all(stop_times)
#
#     await db.commit()