import sqlite3
from config import db_name_prod
import config
from utils.generator import generate_random_value

# create and connect
conn = sqlite3.connect(db_name_prod)
cursor = conn.cursor()

# drop all for debugging
cursor.execute('DROP TABLE IF EXISTS Ships')
cursor.execute('DROP TABLE IF EXISTS Weapons')
cursor.execute('DROP TABLE IF EXISTS Hulls')
cursor.execute('DROP TABLE IF EXISTS Engines')

# create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Ships (
    ship TEXT PRIMARY KEY,
    weapon TEXT NOT NULL,
    hull TEXT NOT NULL,
    engine TEXT NOT NULL,
    FOREIGN KEY (weapon) REFERENCES Weapons(weapon),
    FOREIGN KEY (hull) REFERENCES Hulls(hull),
    FOREIGN KEY (engine) REFERENCES Engines(engine)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Weapons (
    weapon TEXT PRIMARY KEY,
    reload_speed INTEGER NOT NULL,
    rotational_speed INTEGER NOT NULL,
    diameter INTEGER NOT NULL,
    power_volley INTEGER NOT NULL,
    count INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Hulls (
    hull TEXT PRIMARY KEY,
    armor INTEGER NOT NULL,
    type INTEGER NOT NULL,
    capacity INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Engines (
    engine TEXT PRIMARY KEY,
    power INTEGER NOT NULL,
    type INTEGER NOT NULL
)
''')

# filling weapons
for weapon_index in range(1, config.number_of_weapons + 1):
    weapon = f'Weapon-{weapon_index}'
    reload_speed = generate_random_value()
    rotational_speed = generate_random_value()
    diameter = generate_random_value()
    power_volley = generate_random_value()
    count = generate_random_value()

    cursor.execute('''
    INSERT INTO Weapons (weapon, reload_speed, rotational_speed, diameter, power_volley, count)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (weapon, reload_speed, rotational_speed, diameter, power_volley, count))

# filling hulls
for hull_index in range(1, config.number_of_hulls + 1):
    hull = f'Hull-{hull_index}'
    armor = generate_random_value()
    hull_type = generate_random_value()
    capacity = generate_random_value()

    cursor.execute('''
    INSERT INTO Hulls (hull, armor, type, capacity)
    VALUES (?, ?, ?, ?)
    ''', (hull, armor, hull_type, capacity))

# filling engines
for engine_index in range(1, config.number_of_engines + 1):
    engine = f'Engine-{engine_index}'
    power = generate_random_value()
    engine_type = generate_random_value()

    cursor.execute('''
    INSERT INTO Engines (engine, power, type)
    VALUES (?, ?, ?)
    ''', (engine, power, engine_type))

# filling ships
for ship_index in range(1, config.number_of_ships + 1):
    ship = f'Ship-{ship_index}'
    weapon = f'Weapon-{generate_random_value(1, config.number_of_weapons)}'
    hull = f'Hull-{generate_random_value(1, config.number_of_hulls)}'
    engine = f'Engine-{generate_random_value(1, config.number_of_engines)}'

    cursor.execute('''
    INSERT INTO Ships (ship, weapon, hull, engine)
    VALUES (?, ?, ?, ?)
    ''', (ship, weapon, hull, engine))

# save
conn.commit()
print(f"DB {db_name_prod} creation successfully")
conn.close()
