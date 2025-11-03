import pytest
import sqlite3
import os
from config import db_name_prod, db_name_test, number_of_weapons, number_of_engines, number_of_hulls
from config import engine_model, weapon_model, hull_model
from random import choice, randint
from utils.generator import generate_random_value
from utils.randomizer import randomize_ships, randomize_parameter
from models.ship_model import Ship, Engine, Weapon, Hull


def get_all_ships(conn):
    query = """
            SELECT s.ship,
                    w.weapon, w.reload_speed, w.rotational_speed, w.diameter, w.power_volley, w.count,
                    h.hull, h.armor, h.type, h.capacity,
                    e.engine, e.power, e.type
            FROM ships s
            JOIN weapons w
                ON s.weapon = w.weapon
            JOIN hulls h
                ON s.hull = h.hull
            JOIN engines e
                ON s.engine = e.engine
    """
    rows = conn.execute(query).fetchall()

    ships = [
        Ship(
            ship=row[0],
            weapon=Weapon(row[1], row[2], row[3], row[4], row[5], row[6]),
            hull=Hull(row[7], row[8], row[9], row[10]),
            engine=Engine(row[11], row[12], row[13])
        )
        for row in rows
    ]
    return ships


def create_db_copy(source_db_name: str, test_db_name: str):
    source_db = sqlite3.connect(source_db_name)
    test_db = sqlite3.connect(test_db_name)

    with test_db:
        source_db.backup(test_db)

    source_db.close()
    test_db.close()


def randomize_db(temp_db_name: str):
    conn = sqlite3.connect(db_name_test)
    cursor = conn.cursor()

    randomize_ships(cursor=cursor)
    randomize_parameter(cursor=cursor, parameter_name='weapon', table_name='weapons', model=weapon_model)
    randomize_parameter(cursor=cursor, parameter_name='hull', table_name='hulls', model=hull_model)
    randomize_parameter(cursor=cursor, parameter_name='engine', table_name='engines', model=engine_model)

    conn.commit()
    cursor.close()
    conn.close()


# def pytest_generate_tests(metafunc):
#     if {"ship_prod", "ship_test", "check_attr"} <= set(metafunc.fixturenames):
#         conn = sqlite3.connect(db_name_prod)
#         ships_prod = get_all_ships(conn)
#         conn.close()
#         print(f'\nGot ships from {db_name_prod}: {len(ships_prod)}')
#
#         conn = sqlite3.connect(db_name_test)
#         ships_test = get_all_ships(conn)
#         conn.close()
#         print(f'\nGot ships from {db_name_test}: {len(ships_test)}')
#
#         attrs_to_check = ['weapon', 'hull', 'engine']
#
#         dataset = [
#             (ships_prod[i], ships_test[i], attr)
#             for i in range(200)
#             for attr in attrs_to_check
#         ]
#
#         metafunc.parametrize("ship_prod, ship_test, check_attr", dataset, indirect=True)


@pytest.fixture
def get_dataset(clone_test_db, request):
    """Возвращает один элемент dataset для текущего parametrize"""
    with sqlite3.connect(db_name_prod) as conn:
        ships_prod = get_all_ships(conn)
    with sqlite3.connect(db_name_test) as conn:
        ships_test = get_all_ships(conn)

    attrs = ['weapon', 'hull', 'engine']

    dataset = [
        (ships_prod[i], ships_test[i], attr)
        for i in range(len(ships_prod))
        for attr in attrs
    ]

    # request.param будет индекс текущего кейса
    return dataset[request.param]


@pytest.fixture(scope="session", autouse=True)
def clone_test_db():
    # creating test copy
    print(f'\nCreating temporary db copy {db_name_test}')
    create_db_copy(db_name_prod, db_name_test)
    # Randomizing
    randomize_db(db_name_test)

    yield db_name_test

    print('\nFinished')
