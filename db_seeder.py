import psycopg2
from core.config import settings
from typing import List, Tuple


def seed_buildings(connector, cursor, list_buildings: List[Tuple[str]]):
    try:
        query_building = f"INSERT INTO public.building (building_name) values (%s)"
        _ = cursor.executemany(query_building, list_buildings)
        connector.commit()
        print("Success added buildings")
    except Exception as error:
        print("Error then added buildings. More info: ", error)


def seed_important_s(connector, cursor, list_important_s: List[Tuple[str]]):
    try:
        query_important = f"INSERT INTO public.important (important_name) values (%s)"
        _ = cursor.executemany(query_important, list_important_s)
        connector.commit()
        print("Success added important s")
    except Exception as error:
        print("Error then added important s. More info: ", error)


def seed_statuses(connector, cursor, list_statuses: List[Tuple[str]]):
    try:
        query_status = f"INSERT INTO public.status (status_name) values (%s)"
        _ = cursor.executemany(query_status, list_statuses)
        connector.commit()
        print("Success added statuses")
    except Exception as error:
        print("Error then added statuses. More info: ", error)


def seed_systems(connector, cursor, list_systems: List[Tuple[str]]):
    try:
        query_system = f"INSERT INTO public.system (system_name) values (%s)"
        _ = cursor.executemany(query_system, list_systems)
        connector.commit()
        print("Success added systems")
    except Exception as error:
        print("Error then added systems. More info: ", error)


try:
    conn = psycopg2.connect(settings.DATABASE_URL)
    curs = conn.cursor()

    buildings = [("НГ, Паркинг",), ("НГ, Паркинг Этап 2",), ("НГ, корпус 1",),
                 ("НГ, корпус 2",), ("НГ, корпус 3",), ("НГ, корпус 4",), ("Офис",)]
    seed_buildings(connector=conn, cursor=curs, list_buildings=buildings)

    important_s = [("Не срочно",), ("Срочно",), ("Высокая срочность",), ("Критически важно",)]
    seed_important_s(connector=conn, cursor=curs, list_important_s=important_s)

    statuses = [("В пути",), ("Доставлено",), ("Возврат",), ("Заказан",), ("Утерян",), ("В работе",)]
    seed_statuses(connector=conn, cursor=curs, list_statuses=statuses)

    systems = [("ЕГРН",), ("ПИФ",), ("АПВСС",)]
    seed_systems(connector=conn, cursor=curs, list_systems=systems)
    conn.commit()
    print("Success insert superuser")
except (Exception, psycopg2.DatabaseError) as err:
    print("ERROR: ", err)
finally:
    # closing database connection.
    if conn:
        curs.close()
        conn.close()
        print("Connection close")
