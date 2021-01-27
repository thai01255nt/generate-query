import psycopg2
import string
import random
import copy
from postgres.postgres import extract_field, generateCreateTableSql, generatInsertSql


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


conn = psycopg2.connect(
    "dbname=meta_database user=postgres password=abcd1234 host=golangvietnam.com port=5432")
cur = conn.cursor()

workspace_metadata_sample = [{"workspaceName": id_generator(4)}]
table_metadata_sample = [
    {"workspaceId": 1, "tableName": "setelProfile1", "type": 0, "is_deleted": 0},
    # {"workspaceId": 1, "tableName": "order1", "type": 0, "is_deleted":0},
    # {"workspaceId": 1, "tableName": "order2", "type": 0, "is_deleted":0},
    # {"workspaceId": 1, "tableName": "orderDetail", "type": 0, "is_deleted":0},
    # {"workspaceId": 1, "tableName": "setelProfile", "type": 1, "is_deleted":0},
    # {"workspaceId": 1, "tableName": "order", "type": 1, "is_deleted":0},
    # {"workspaceId": 1, "tableName": "orderDetail", "type": 1, "is_deleted":0}
]

source_field_metadata_sample = [
    {"workspaceId": 1, "tableId": 1, "fieldName": "id", "type": "INT", "is_deleted": 0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "email", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "phone1", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "address", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "id", "type": "INT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "email", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "orderId", "type": "INT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "id", "type": "INT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "email", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "orderId", "type": "INT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "phone", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "id", "type": "INT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "productName", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "orderValue", "type": "FLOAT", "is_deleted":0}
]
destination_field_metadata_sample = [
    {"workspaceId": 1, "tableId": 1, "fieldName": "id", "type": "INT", "is_deleted": 0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "email", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "phone", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "address", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "id", "type": "INT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "email", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "orderId", "type": "INT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "phone", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "id", "type": "INT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "productName", "type": "TEXT", "is_deleted":0},
    # {"workspaceId": 1, "tableId": 1, "fieldName": "orderValue", "type": "FLOAT", "is_deleted":0}
]
imap_metadata_sample = [
    {"sourceFieldId": 1, "destinationId": 1, "is_deleted": 0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
    # {"sourceFieldId": 1, "destinationId": 1, "is_deleted":0},
]
jmap_metadata_sample = [
    {"parentFieldId": 1, "childFieldId": 1, "is_deleted": 0},
    # {"parentFieldId": 1, "childFieldId": 1, "is_deleted":0}
]

# Init database
workspace_metadata_fields = extract_field(workspace_metadata_sample)
table_metadata_fields = extract_field(table_metadata_sample)
source_field_metadata_fields = extract_field(source_field_metadata_sample)
destination_field_metadata_fields = extract_field(destination_field_metadata_sample)
imap_metadata_fields = extract_field(imap_metadata_sample)
jmap_metadata_fields = extract_field(jmap_metadata_sample)

workspace_metadata_name = 'workspace'
table_metadata_name = 'table_item'
source_field_metadata_name = 'source_field'
destination_field_metadata_name = 'destination_field'
imap_metadata_name = 'imap'
jmap_metadata_name = 'jmap'

cur.execute(generateCreateTableSql(workspace_metadata_fields, workspace_metadata_name))
conn.commit()
cur.execute(generateCreateTableSql(table_metadata_fields, table_metadata_name))
conn.commit()
cur.execute(generateCreateTableSql(source_field_metadata_fields, source_field_metadata_name))
conn.commit()
cur.execute(generateCreateTableSql(destination_field_metadata_fields, destination_field_metadata_name))
conn.commit()
cur.execute(generateCreateTableSql(imap_metadata_fields, imap_metadata_name))
conn.commit()
cur.execute(generateCreateTableSql(jmap_metadata_fields, jmap_metadata_name))
conn.commit()

# Fake data
num_workspace = 999

for i_workspace in range(num_workspace):
    # Insert new workspace
    workspace_metadata = copy.deepcopy(workspace_metadata_sample)
    workspace_metadata[0]["workspaceName"] = id_generator(4)
    cur.execute(generatInsertSql(workspace_metadata, workspace_metadata_name))
    workspace_id = cur.fetchone()[0]
    conn.commit()

    # Insert new table into table table
    table_metadata = [
        {"workspaceId": workspace_id, "tableName": "setelProfile1", "type": 0, "is_deleted": 0},
        {"workspaceId": workspace_id, "tableName": "order1", "type": 0, "is_deleted": 0},
        {"workspaceId": workspace_id, "tableName": "order2", "type": 0, "is_deleted": 0},
        {"workspaceId": workspace_id, "tableName": "orderDetail", "type": 0, "is_deleted": 0},
        {"workspaceId": workspace_id, "tableName": "setelProfile", "type": 1, "is_deleted": 0},
        {"workspaceId": workspace_id, "tableName": "order", "type": 1, "is_deleted": 0},
        {"workspaceId": workspace_id, "tableName": "orderDetail", "type": 1, "is_deleted": 0}
    ]
    table_metadata_id = []
    for _table_metadata in table_metadata:
        cur.execute(generatInsertSql([_table_metadata], table_metadata_name))
        table_metadata_id.append(cur.fetchone()[0])
        conn.commit()

    source_field_metadata = [
        {"workspaceId": workspace_id, "tableId": table_metadata_id[0], "fieldName": "id", "type": "INT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[0], "fieldName": "email", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[0], "fieldName": "phone1", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[0], "fieldName": "address", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[1], "fieldName": "id", "type": "INT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[1], "fieldName": "email", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[1], "fieldName": "orderId", "type": "INT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[2], "fieldName": "id", "type": "INT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[2], "fieldName": "email", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[2], "fieldName": "orderId", "type": "INT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[2], "fieldName": "phone", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[3], "fieldName": "id", "type": "INT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[3], "fieldName": "productName", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[3], "fieldName": "orderValue", "type": "FLOAT",
         "is_deleted": 0}
    ]
    source_field_metadata_id = []
    for _source_field_metadata in source_field_metadata:
        cur.execute(generatInsertSql([_source_field_metadata], source_field_metadata_name))
        source_field_metadata_id.append(cur.fetchone()[0])
        conn.commit()

    destination_field_metadata = [
        {"workspaceId": workspace_id, "tableId": table_metadata_id[4], "fieldName": "id", "type": "INT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[4], "fieldName": "email", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[4], "fieldName": "phone", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[4], "fieldName": "address", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[5], "fieldName": "id", "type": "INT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[5], "fieldName": "email", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[5], "fieldName": "orderId", "type": "INT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[5], "fieldName": "phone", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[6], "fieldName": "id", "type": "INT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[6], "fieldName": "productName", "type": "TEXT",
         "is_deleted": 0},
        {"workspaceId": workspace_id, "tableId": table_metadata_id[6], "fieldName": "orderValue", "type": "FLOAT",
         "is_deleted": 0}
    ]
    destination_field_metadata_id = []
    for _destination_field_metadata in destination_field_metadata:
        cur.execute(generatInsertSql([_destination_field_metadata], destination_field_metadata_name))
        destination_field_metadata_id.append(cur.fetchone()[0])
        conn.commit()

    imap_metadata = [
        {"sourceFieldId": source_field_metadata_id[0], "destinationId": destination_field_metadata_id[0],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[1], "destinationId": destination_field_metadata_id[1],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[2], "destinationId": destination_field_metadata_id[2],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[3], "destinationId": destination_field_metadata_id[3],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[4], "destinationId": destination_field_metadata_id[4],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[5], "destinationId": destination_field_metadata_id[5],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[6], "destinationId": destination_field_metadata_id[6],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[7], "destinationId": destination_field_metadata_id[4],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[8], "destinationId": destination_field_metadata_id[5],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[9], "destinationId": destination_field_metadata_id[6],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[10], "destinationId": destination_field_metadata_id[7],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[11], "destinationId": destination_field_metadata_id[8],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[12], "destinationId": destination_field_metadata_id[9],
         "is_deleted": 0},
        {"sourceFieldId": source_field_metadata_id[13], "destinationId": destination_field_metadata_id[10],
         "is_deleted": 0},
    ]
    imap_metadata_id = []
    for _imap_metadata in imap_metadata:
        cur.execute(generatInsertSql([_imap_metadata], imap_metadata_name))
        imap_metadata_id.append(cur.fetchone()[0])
        conn.commit()

    jmap_metadata = [
        {"parentFieldId": destination_field_metadata_id[1], "childFieldId": destination_field_metadata_id[5],
         "is_deleted": 0},
        {"parentFieldId": destination_field_metadata_id[6], "childFieldId": destination_field_metadata_id[8],
         "is_deleted": 0}
    ]
    jmap_metadata_id = []
    for _jmap_metadata in jmap_metadata:
        cur.execute(generatInsertSql([_jmap_metadata], jmap_metadata_name))
        jmap_metadata_id.append(cur.fetchone()[0])
        conn.commit()
