import pytest

from configs.db_constants_and_configs import (TABLES_CONFIG, DB_NAME,
                                              NEW_DB_NAME)
from data_base.db_processing import DBConnector
from data_base.db_commands import (initialize_db, generate_random_db_data,
                                   generate_updated_db_data)


@pytest.fixture(scope='session')
def dumped_db_connector(db_connector: DBConnector) -> tuple:
    """
    Pytest fixture that dumps and replaces data from original db
    :param db_connector: connection to original db
    :return: connector to dumped db with new data
    """
    db_connector.dump_db(NEW_DB_NAME)
    with DBConnector(NEW_DB_NAME) as dumped_db:
        generate_updated_db_data(dumped_db)

        yield dumped_db

        for table_name in TABLES_CONFIG:
            dumped_db.drop_table(table_name)


@pytest.fixture(scope='session')
def db_connector() -> DBConnector:
    """
    Pytest fixture that creates/destroys db connection and generates data in it
    :return: connector db
    """
    with DBConnector(DB_NAME) as db:
        initialize_db(db)
        generate_random_db_data(db)
        yield db

        for table_name in TABLES_CONFIG:
            db.drop_table(table_name)


@pytest.hookimpl(trylast=True)
def pytest_assertrepr_compare(op, left, right) -> list:
    """
    Pytest hook that replaces assertion error output on custom one
    (didn't work in my PyCharm version,
    needs additional exploration of the problem)
    :return: list of strings with error messsages
    """
    if isinstance(left, str) and isinstance(right, str) and op == '==':
        return [
            'Comparing ship components',
            f'   expected: {left}, actual: {right}',
        ]
    elif isinstance(left, dict) and isinstance(right, dict) and op == '==':
        for component_item, item_value in left.items():
            if item_value != right[component_item]:
                return [
                    'Comparing ship component values',
                    f'   {component_item}: expected {item_value}, actual '
                    f'{right[component_item]}',
                ]
