import logging
from random import randint, sample


def generate_n_items(item_name: str, number: int) -> list:
    """
    Function provides string-items generation
    :param item_name: name of the feature to generate
    :param number: number of items that will be generated
    :return: list with generated data
    """
    logging.debug(f'Generate {number} number of {item_name} items')
    return [f'{item_name}-{index}' for index in range(number)]


def generate_n_integers(number_of_digits: int, left_border: int,
                        right_border: int) -> list:
    """
    Function provides digits generation
    :param number_of_digits: number of items that will be generated
    :param left_border: left border of the generation interval
    :param right_border: right border of the generation interval
    :return: list with generated data
    """
    logging.debug(f'Generate {number_of_digits} random numbers from '
                  f'[{left_border}, {right_border}] interval')
    return [randint(left_border, right_border) for _
            in range(number_of_digits)]


def generate_items_for_ships(item_name: str, number: int, left_border: int,
                             right_border: int) -> list:
    """
    Function that generates available items for ship components
    :param item_name: ship component name
    :param number: number of items that will be generated
    :param left_border: left border of the generation interval
    :param right_border: right border of the generation interval
    :return: list with generated data
    """
    logging.debug(f'Generate {number} items for {item_name} of ship '
                  f'from [{left_border}, {right_border}] interval')
    result = []
    for item_index in range(number):
        item_suffix = randint(left_border, right_border-1)
        result.append(f'{item_name}-{item_suffix}')
    return result


def get_random_value(available_items: tuple) -> str:
    """
    Function returns random value from tuple
    :param available_items: available data to get from
    :return: item from tuple
    """
    logging.debug(f'Get random value from {available_items}')
    return sample(available_items, 1)[0]


def generate_test_cases(item_case_name: str = 'ship',
                        number_of_case_items: int = 200,
                        available_components: tuple =
                        ('weapon', 'hull', 'engine')) -> list:
    """
    Method provides test cases generation according to described rules
    :param item_case_name: name for the item for which
                           test cases should be generated
    :param number_of_case_items: number of desired distinct items
    :param available_components: tuple with components for each item
    :return: list of all possible pairs of ship-component
    """
    logging.debug('Generate test cases')
    testing_items = generate_n_items(item_case_name, number_of_case_items)
    result = []
    for item in testing_items:
        for component in available_components:
            result.append((item, component))

    return result
