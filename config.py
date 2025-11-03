
# global parameters of the project

db_name_prod = 'wows_prod.db'
db_name_test = 'wows_test.db'

# Number of items to generate
number_of_ships = 200
number_of_weapons = 20
number_of_hulls = 5
number_of_engines = 6

# Value range for integer parameters
min_random_value = 1
max_random_value = 20


# db models
ship_model = {'weapon': number_of_weapons, 'hull': number_of_hulls, 'engine': number_of_engines}
weapon_model = ['reload_speed', 'rotational_speed', 'diameter', 'power_volley', 'count']
hull_model = ['armor', 'type', 'capacity']
engine_model = ['power', 'type']
