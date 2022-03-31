import logging
import sqlite3
from typing import Optional, Union

from configs.db_constants_and_configs import (FOREIGN_KEYS_QUERY, CREATE_QUERY,
                                              INSERT_QUERY, UPDATE_QUERY,
                                              SIMPLE_SELECT_QUERY,
                                              WHERE_CLAUSE, JOIN_CLAUSE)

logger = logging.getLogger()


class DBConnector:
    """
    Class that provides object for interaction with sqlite database
    """
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.cursor = None
        self.conn = None

    def __enter__(self):
        self.create_connection()
        self.create_db()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy_connection()

    def __execute_query(self, query: str, many: bool = False,
                        commit: bool = False,
                        query_data: Optional[Union[list, tuple]] = None
                        ) -> Optional[list]:
        """
        Method provides SQL-query execution process
        :param query: SQL-query that should be executed
        :param many: True - use executemany() method, else - execute() method
        :param commit: True - if make connection.commit()
        :param query_data: list with data that should be inserted in
                           executemany() method
        :return: list with output result if it is possible
        """
        logger.debug(f'Execute query: {query}')
        try:
            if many:
                self.cursor.executemany(query, query_data)
            else:
                if query_data:
                    self.cursor.execute(query, query_data)
                else:
                    self.cursor.execute(query)

            if commit:
                self.conn.commit()

            logger.debug('Query has executed successfully')
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            logger.warning(f'Error while executing query {query}', error)

    def create_connection(self) -> None:
        """
        Method provides creating connection to SQLite database
        """
        logger.debug(f'Create connection to the {self.db_name}')
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            self.cursor = sqlite_connection.cursor()
            self.conn = sqlite_connection
            logger.debug('Database is created and connected to '
                         'SQLite successfully')
        except sqlite3.Error as error:
            logger.debug('Error while connecting to SQLite', error)

    def destroy_connection(self) -> None:
        """
        Method provides destroying connection to SQLite database
        """
        logger.debug('Disconnect from SQLite')
        try:
            self.cursor.close()
        except sqlite3.Error as error:
            logger.debug('Error while closing SQLite connection', error)

    def create_db(self) -> None:
        """
        Method provides destroying connection to SQLite database
        """
        logger.info('Create database')
        self.create_connection()

    def dump_db(self, new_db_name: str) -> None:
        """
        Method provides dumping database
        :param new_db_name: dumped database name
        """
        logger.info(f'Dump current db in new one: {new_db_name}')
        try:
            new_db_conn = sqlite3.connect(new_db_name)
            with new_db_conn:
                self.conn.backup(new_db_conn)
            logger.debug('Database is dumped successfully')
        except sqlite3.Error as error:
            logger.debug('Error while connecting to SQLite', error)
        finally:
            logger.debug(f'Disconnect from SQLite: {new_db_name}')
            new_db_conn.close()

    def add_table(self, table_name: str, fields: dict) -> None:
        """
        Method provides creating table
        :param table_name: name of the table that should be created
        :param fields: dict with table fields configuration
        {field_name: filed_params}
        """
        logger.info(f'Create table: {table_name}')
        columns = []
        for field_name, field_type in fields.items():
            if field_name == 'foreign_keys':
                for foreign_key_config in field_type:
                    columns.append(
                        FOREIGN_KEYS_QUERY.format(*foreign_key_config))
            else:
                columns.append(' '.join([field_name, field_type]))
        fields_query = ', '.join(columns)
        create_query = CREATE_QUERY.format(table_name, fields_query)

        self.__execute_query(create_query)

    def insert_data(self, table_name: str, table_columns: tuple,
                    table_data: list) -> None:
        """
        Method provides inserting data into table
        :param table_name: name of the table that will be filled
        :param table_columns: available table column names that will insert
        :param table_data: columns data that will be filled
        Note: column names and it's data should be in the same order
        """
        logger.info(f'Insert data into {table_name} table')
        data_query = ','.join(['?']*len(table_columns))

        insert_query = INSERT_QUERY.format(table_name, data_query)
        self.__execute_query(insert_query, many=True, commit=True,
                             query_data=table_data)

    def update_data(self, table_name: str, updated_data: tuple) -> None:
        """
        Method provides updating data in table
        :param table_name: name of the table where data should be updated
        :param updated_data: data that should be updated, next format is used:
        (column_name_for_condition, condition_value,
        column_that_will_be_updated, new_data_value)
        """
        logger.info(f'Update data for {updated_data[0]} column '
                    f'in {table_name} table')
        update_query = UPDATE_QUERY.format(table_name, updated_data[2],
                                           updated_data[0])
        values = (updated_data[3], updated_data[1])

        self.__execute_query(update_query, commit=True, query_data=values)

    def update_multiple_data(self, table_name: str, updated_data: list
                             ) -> None:
        """
        Method provides updating multiple data in table
        :param table_name: name of the table where data should be updated
        :param updated_data: list of tuples with data that should be updated
        """
        logger.info(f'Update multiple data for {table_name} table')
        for item_data in updated_data:
            self.update_data(table_name, item_data)

    def select_wo_condition(self, table_name: str, columns_to_select: list
                            ) -> list:
        """
        Method provides selecting data without condition
        :param table_name: name of the table where data should be selected
        :param columns_to_select: list of columns that will be selected
        :return: list with tuples with data from columns in the order
                 like in columns_to_select
        """
        logger.info(f'Select {columns_to_select} from {table_name} table')
        columns_query = (columns_to_select[0] if len(columns_to_select) == 1
                         else ', '.join(columns_to_select))
        select_query = SIMPLE_SELECT_QUERY.format(columns_query, table_name)

        return self.__execute_query(select_query)

    def select_with_condition(self, table_name: str, columns_to_select: list,
                              condition: str) -> list:
        """
        Method provides selecting data with condition
        :param table_name: name of the table where data should be selected
        :param columns_to_select: list of columns that will be selected
        :param condition: string with condition, following format:
                          column_name = column_value, ...
        :return: list with tuples with data from columns in the order
                 like in columns_to_select
        """
        logger.info(f'Select {columns_to_select} from {table_name} '
                    f'table with condition {condition}')
        columns_query = (columns_to_select[0] if len(columns_to_select) == 1
                         else ', '.join(columns_to_select))
        condition_query = f'{table_name} {WHERE_CLAUSE.format(condition)}'
        select_query = SIMPLE_SELECT_QUERY.format(columns_query,
                                                  condition_query)

        return self.__execute_query(select_query)

    def select_with_join_and_condition(self, table_name: str,
                                       columns_to_select: list,
                                       another_table_name: str,
                                       join_filed: str,
                                       condition: str) -> list:
        """
        Method provides selecting data from multiple columns with condition
        (using JOIN statement)
        :param table_name: name of the table where data should be selected
        :param columns_to_select: list of columns that will be selected
        :param another_table_name: table name that will be joined
        :param join_filed: field name that will be used in ON statement
                           (this filed should be present in both tables)
        :param condition: string with condition, following format:
                          column_name = column_value, ...
        :return: list with tuples with data from columns in the order
                 like in columns_to_select
        """
        logger.info(f'Select {columns_to_select} from {table_name} '
                    f'table with condition {condition}')
        columns_query = (columns_to_select[0] if len(columns_to_select) == 1
                         else ', '.join(columns_to_select))
        join_query = JOIN_CLAUSE.format(
            another_table_name,
            f'{table_name}.{join_filed} = {another_table_name}.{join_filed}')
        condition_query = (f'{table_name} {join_query} '
                           f'{WHERE_CLAUSE.format(condition)}')
        select_query = SIMPLE_SELECT_QUERY.format(columns_query,
                                                  condition_query)

        return self.__execute_query(select_query)

    def drop_table(self, table_name: str) -> None:
        """
        Method provides dropping table from database
        :param table_name: name of the table that should be dropped
        """
        logger.info(f'Drop {table_name} table')
        drop_query = f'DROP TABLE {table_name};'
        self.__execute_query(drop_query)
