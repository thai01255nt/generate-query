import bson
import json


def get_type(value):
    if isinstance(value, str):
        return 'TEXT'
    if isinstance(value, dict):
        return 'JSON'
    if isinstance(value, int):
        return 'INTEGER'
    if isinstance(value, float):
        return 'FLOAT'


def extract_field(data):
    full_field = {}
    for _data in data:
        for key in _data.keys():
            type_value = get_type(_data[key])
            if key not in full_field.keys() and type_value:
                full_field[key] = type_value
    return full_field


def generateCreateTableSql(full_field, table_name):
    create_full_field = ''
    for key in full_field.keys():
        create_full_field += f'{key} {full_field[key]},'
    create_full_field = create_full_field[:-1]
    sql = f'''CREATE TABLE IF NOT EXISTS {table_name} ( id serial PRIMARY KEY,{create_full_field} ); '''
    return sql


def generatInsertSql(data, table_name):
    full_field = extract_field(data)
    sql = ''

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
        sql += f'INSERT INTO {table_name}({list_key}) VALUES ({list_value}) RETURNING id;'
    return sql


def generate_insert_query(raw_order, order_wh, profile_wh):
    insert_raw_order_query = generatInsertSql(raw_order, 'rawOrder')
    insert_order_wh_query = generatInsertSql(order_wh, 'orderWH')
    insert_profile_wh_query = generatInsertSql(profile_wh, 'profileWH')
    return insert_raw_order_query, insert_order_wh_query, insert_profile_wh_query


def generate_join_query():
    sql = '''
        INSERT INTO orderWH (email,value,cdpId)
        SELECT
                    email,
                    value,
                    cdpId
            FROM rawOrder td1
            LEFT JOIN (
                SELECT DISTINCT
                    MAX(id) as cdpId,
                    email as email_mapping_workspace
                FROM profileWH
                GROUP BY email
            )td2 ON td1.email = td2.email_mapping_workspace 
    '''
    return sql
