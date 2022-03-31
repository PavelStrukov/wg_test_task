CREATE_QUERY = 'CREATE TABLE {} ({});'
FOREIGN_KEYS_QUERY = 'FOREIGN KEY ({}) REFERENCES {} ({})'
INSERT_QUERY = 'INSERT INTO {} VALUES ({});'
UPDATE_QUERY = 'UPDATE {} SET {} = ? WHERE {} = ?;'
SIMPLE_SELECT_QUERY = 'SELECT {} FROM {};'
WHERE_CLAUSE = 'WHERE {}'
JOIN_CLAUSE = 'JOIN {} ON {}'
DB_NAME = 'sqlite_python.db'
NEW_DB_NAME = 'new_sqlite_python.db'

TABLES_CONFIG = {
    'weapons':
        {
            'weapon': 'TEXT PRIMARY KEY',
            '"reload speed"': 'INTEGER',
            '"rotational speed"': 'INTEGER',
            'diameter': 'INTEGER',
            '"power volley"': 'INTEGER',
            'count': 'INTEGER',
        },
    'hulls':
        {
            'hull': 'TEXT PRIMARY KEY',
            'armor': 'INTEGER',
            'type': 'INTEGER',
            'capacity': 'INTEGER',
        },
    'engines':
        {
            'engine': 'TEXT PRIMARY KEY',
            'power': 'INTEGER',
            'type': 'INTEGER',
        },
    'Ships':
        {
            'ship': 'TEXT PRIMARY KEY',
            'weapon': 'TEXT',
            'hull': 'TEXT',
            'engine': 'TEXT',
            'foreign_keys': [('weapon', 'weapons', 'weapon'),
                             ('hull', 'hulls', 'hull'),
                             ('engine', 'engines', 'engine')]
        },
}

ITEM_TABLE_MATCHER = {
        'ship': 'Ships',
        'weapon': 'weapons',
        'hull': 'hulls',
        'engine': 'engines'
}


INTEGER_RANGE = (1, 20)
NUMBER_OF_ROWS_PER_TABLE = {
    'weapons': 20,
    'Ships': 200,
    'hulls': 5,
    'engines': 6
}
