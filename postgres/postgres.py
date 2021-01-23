import psycopg2
import bson
import json




def get_type(value):
    if isinstance(value, str):
        return 'TEXT'
    if isinstance(value, dict):
        return 'JSON'
    if isinstance(value, int):
        return 'INTERGER'
    if isinstance(value, float):
        return 'FLOAT'


def generatInsertProfileSql(data, table_name):
    full_field = {}
    for _data in data:
        for key in _data.keys():
            type_value = get_type(_data[key])
            if key not in full_field.keys() and type_value:
                full_field[key] = type_value
    create_full_field = ''
    for key in full_field.keys():
        create_full_field += f'{key} {full_field[key]},'
    create_full_field = create_full_field[:-1]
    sql = f'''CREATE TABLE {table_name} ( id serial PRIMARY KEY,{create_full_field} ); '''

    for _data in data:
        list_key = ''
        list_value = ''
        for key in full_field:
            type_value = full_field[key]
            value = _data[key]
            if type_value == "JSON":
                value = json.dumps(value)
                value = f"'{value}'"
            if type_value == "TEXT":
                value = f"'{value}'"
            if value is None:
                value = 'NULL'
            list_key += f'{key},'
            list_value += f'{value},'
        list_key = list_key[:-1]
        list_value = list_value[:-1]
        sql += f'INSERT INTO {table_name}({list_key}) VALUES ({list_value}); '
    return sql

def insert_many(raw_order,order_wh,profile_wh):
    