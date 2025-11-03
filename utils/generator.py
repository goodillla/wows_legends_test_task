from random import randint
import config


def generate_random_value(min_value=config.min_random_value, max_value=config.max_random_value) -> int:
    return randint(min_value, max_value)
