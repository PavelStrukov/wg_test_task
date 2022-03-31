import pytest

from data_base.db_commands import (get_ship_parameter,
                                   get_ship_parameter_options)
from utils.data_generation_utils import generate_test_cases


@pytest.mark.parametrize(
    'ship_to_check, component_to_check', generate_test_cases()
)
def test_ships_configuration(ship_to_check, component_to_check, db_connector,
                             dumped_db_connector):

    expected_component_value = get_ship_parameter(db_connector, ship_to_check,
                                                  component_to_check)
    actual_component_value = get_ship_parameter(dumped_db_connector,
                                                ship_to_check,
                                                component_to_check)

    assert expected_component_value == actual_component_value, \
        f'{ship_to_check}, {component_to_check}:'

    expected_component_options = get_ship_parameter_options(db_connector,
                                                            ship_to_check,
                                                            component_to_check)
    actual_component_options = get_ship_parameter_options(dumped_db_connector,
                                                          ship_to_check,
                                                          component_to_check)

    assert expected_component_options == actual_component_options, \
        f'{ship_to_check}, {component_to_check}:'
