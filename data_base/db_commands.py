import logging

from configs.db_constants_and_configs import TABLES_CONFIG, ITEM_TABLE_MATCHER
from data_base.db_processing import DBConnector
from data_generators.items_generator import ItemsGenerator


def initialize_db(db_connector: DBConnector) -> None:
    """
    Function provides database initialization (creating tables)
    :param db_connector: database connector object
    """
    logging.info(f'Initialize {db_connector.db_name} database')
    for table_name, columns in TABLES_CONFIG.items():
        db_connector.add_table(table_name, columns)


def generate_random_db_data(db_connector: DBConnector) -> None:
    """
    Function provides database data generation and insertion
    :param db_connector: database connector object
    """
    logging.info('Start generating data')
    for table_name in TABLES_CONFIG:
        item_generator = ItemsGenerator(table_name)
        raw_generated_data = item_generator.generate_data()
        cleared_data = item_generator.parse_data_for_insert_query(
            raw_generated_data)
        db_connector.insert_data(table_name, item_generator.columns,
                                 cleared_data)


def generate_updated_db_data(db_connector: DBConnector) -> None:
    """
    Function provides new database data generation and updating
    :param db_connector: database connector object
    """
    logging.info('Start generating updated data')
    for table_name in TABLES_CONFIG:
        item_generator = ItemsGenerator(table_name)
        raw_updated_data = item_generator.generate_updated_data()
        cleared_data = item_generator.parse_data_for_update_query(
            raw_updated_data)
        db_connector.update_multiple_data(table_name, cleared_data)


def get_ship_parameter(db_connector: DBConnector, ship_id: str,
                       param_name: str) -> str:
    """
    Function provides selecting ship parameter data from Ships table
    :param db_connector: database connector object
    :param ship_id: concrete id of the ship
    :param param_name: parameter name that should be selected
    :return: parameter value
    """
    logging.info(f'Get {param_name} value for {ship_id} from {db_connector}')
    ship_parameter = db_connector.select_with_condition(
        'Ships', [param_name], f'ship = "{ship_id}"')[0][0]
    return ship_parameter.strip("'")


def get_ship_parameter_options(db_connector: DBConnector, ship_id: str,
                               param_name: str) -> dict:
    """
    Function provides selecting ship parameter options data by
    joining data from Ships and parameter tables
    :param db_connector: database connector object
    :param ship_id: concrete id of the ship
    :param param_name: parameter name that options should be selected
    :return: dict with option values following next format:
    {option_name: option_value, ...}
    """
    logging.info(f'Get options for {param_name} for {ship_id} from '
                 f'{db_connector}')
    result_data = {}
    table_to_select = ITEM_TABLE_MATCHER[param_name]
    parameter_options = list(TABLES_CONFIG[table_to_select].keys())[1:]
    ship_parameter_options = db_connector.select_with_join_and_condition(
        table_to_select, parameter_options,
        'Ships', param_name, f'Ships.ship = "{ship_id}"')[0]

    for option_name, option_value in zip(parameter_options,
                                         ship_parameter_options):
        result_data[option_name] = option_value
    return result_data
