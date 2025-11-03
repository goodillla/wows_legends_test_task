from config import ship_model
from utils.generator import generate_random_value
from random import choice


def randomize_ships(cursor):
    print('Randomizing ships...')
    # select all
    cursor.execute("SELECT ship FROM ships")
    rows = cursor.fetchall()

    for (ship,) in rows:
        col_to_update = choice(list(ship_model.keys()))
        new_value = f'{col_to_update.capitalize()}-{generate_random_value(1, ship_model[col_to_update])}'

        cursor.execute(f'''
            UPDATE ships
            SET {col_to_update} = ? WHERE ship = ?
        ''', (new_value, ship))


def randomize_parameter(cursor, parameter_name, table_name, model):
    print(f'Randomizing {table_name}...')
    # select all
    cursor.execute(f"SELECT {parameter_name} FROM {table_name}")
    rows = cursor.fetchall()

    for (parameter,) in rows:
        col_to_update = choice(model)
        new_value = generate_random_value()

        cursor.execute(f'''
            UPDATE {table_name}
            SET {col_to_update} = ? WHERE {parameter_name} = ?
        ''', (new_value, parameter))
