import pytest
from config import number_of_ships

dataset_len = number_of_ships * 3  # 200 ships * 3 attr


@pytest.mark.parametrize("get_dataset", list(range(dataset_len)), indirect=True)
def test_ship(get_dataset):
    ship_prod, ship_test, attr = get_dataset

    print(f'\nTest for {ship_prod.ship} (prod) - {ship_test.ship} (test) - {attr}')
    assert ship_prod.ship == ship_test.ship, 'Ship object name has to be equal'

    ship_prod_attr = getattr(ship_prod, attr)
    ship_test_attr = getattr(ship_test, attr)
    # print(ship_prod_attr, ship_test_attr, sep='\n')

    # print(ship_prod_attr.name, ship_test_attr.name)
    assert ship_prod_attr.name == ship_test_attr.name, \
        f'\n\n{ship_test.ship}, {ship_test_attr.name}:\n\t' \
        f'expected: {ship_prod_attr.name}, got {ship_test_attr.name}'

    # print(ship_prod_attr.__dataclass_fields__)
    for field_name in ship_prod_attr.__dataclass_fields__:
        ship_prod_attr_value = getattr(ship_prod_attr, field_name)
        ship_test_attr_value = getattr(ship_test_attr, field_name)
        # print(field_name, ship_prod_attr_value, ship_test_attr_value)

        assert ship_prod_attr_value == ship_test_attr_value, \
            f'\n\n{ship_test.ship}, {ship_test_attr.name}:\n\t' \
            f'{field_name}: expected {ship_prod_attr_value}, got {ship_test_attr_value}'
