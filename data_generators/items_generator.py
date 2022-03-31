import logging

from configs.db_constants_and_configs import (TABLES_CONFIG,
                                              NUMBER_OF_ROWS_PER_TABLE,
                                              INTEGER_RANGE)
from utils.data_generation_utils import (generate_n_items,
                                         generate_n_integers,
                                         generate_items_for_ships,
                                         get_random_value)


class ItemsGenerator:
    """Class provides functionality for generating ships random data
    for database"""
    table_item_matcher = {
        'Ships': 'ship',
        'weapons': 'weapon',
        'hulls': 'hull',
        'engines': 'engine'
    }

    def __init__(self, table_name: str):
        self.name = self.table_item_matcher.get(table_name)
        self.table_name = table_name
        self.columns = self.__get_columns()
        self.number_of_rows = NUMBER_OF_ROWS_PER_TABLE.get(self.table_name)

    def __get_columns(self) -> tuple:
        """Method returns available columns for table according to db config"""
        item_config = TABLES_CONFIG.get(self.table_name)
        return tuple(col_name for col_name in item_config
                     if col_name != 'foreign_keys')

    def __generate_data_for_ships(self) -> dict:
        """
        Generating data for Ships table differs from other tables
        :return: dict in the following format
        {column_name: [column_values,...], ...}
        """
        generated_result = {}
        for col_name in self.columns:
            if col_name == 'ship':
                generated_col_data = generate_n_items(self.name,
                                                      self.number_of_rows)
            else:
                table_for_col = [k for k, v in self.table_item_matcher.items()
                                 if v == col_name][0]
                generated_col_data = generate_items_for_ships(
                    col_name, self.number_of_rows, 0,
                    NUMBER_OF_ROWS_PER_TABLE[table_for_col])
            generated_result[col_name] = generated_col_data

        return generated_result

    def generate_data(self) -> dict:
        """Method generates data according to described rules
        :returns dict where value is a list of generated data for each column
        {column_name: [column_values,...], ...}"""
        logging.info(f'Generating data for {self.name} item')
        if self.table_name == 'Ships':
            generated_result = self.__generate_data_for_ships()
        else:
            generated_result = {}
            for col_name in self.columns:
                if col_name in self.table_item_matcher.values():
                    generated_col_data = generate_n_items(self.name,
                                                          self.number_of_rows)
                else:
                    generated_col_data = generate_n_integers(
                        self.number_of_rows, *INTEGER_RANGE)
                generated_result[col_name] = generated_col_data

        return generated_result

    def generate_updated_data(self) -> dict:
        """Method generates data for table update according to described rules
        :returns dict pairs for each primary key row stands tuple with
        (column name, new value) data for update:
        {feature_id: (column_name, new_column_value), ...}"""
        logging.info(f'Generate updated data for {self.table_name} table')
        available_columns_for_update = tuple(set(self.columns) - {self.name})
        result = {}
        for item in generate_n_items(self.name, self.number_of_rows):
            column_to_update = get_random_value(available_columns_for_update)
            if self.table_name == 'Ships':
                table_for_col = [k for k, v in self.table_item_matcher.items()
                                 if v == column_to_update][0]
                value_to_update = generate_items_for_ships(
                    column_to_update, 1, 0,
                    NUMBER_OF_ROWS_PER_TABLE[table_for_col])[0]
            else:
                value_to_update = generate_n_integers(1, *INTEGER_RANGE)[0]
            result[f'{item}'] = (column_to_update, value_to_update)

        return result

    def parse_data_for_insert_query(self, generated_data: dict) -> list:
        """
        Method returns list of tuples based on input dict
        :param generated_data: dict with data in the following format:
                               {column_name: [column_values,...], ...}
        :return: list of tuples in the next format:
        [(value_for_column_0, value_for_column_1, ...), (...), ...]
        """
        result_list = []
        for row_index in range(self.number_of_rows):
            result_list.append(tuple([generated_data[col_name][row_index] for
                                      col_name in self.columns]))

        return result_list

    def parse_data_for_update_query(self, generated_data: dict) -> list:
        """Method returns list of tuples based on input dict
        :param generated_data:
                {feature_id: (column_name, new_column_value), ...}
        :returns [
            (primary column, primary key for each row,
            column name for update, new data),
            ...
        ]"""
        result_list = []
        for primary_key, update_data in generated_data.items():
            result_list.append((self.name, primary_key, ) + update_data)

        return result_list
