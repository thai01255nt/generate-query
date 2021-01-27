from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

db_measure = client.dbMeasure


def insert_many(raw_order, order_wh, profile_wh):
    db_measure.measureInsertRawOrder.insert_many(raw_order)
    db_measure.measureInsertOrderWH.insert_many(order_wh)
    db_measure.measureInsertProfileWH.insert_many(profile_wh)
    return


def joinOrder():
    order_pipeline = [
        {
            '$project': {
                '_id': 0,
                'email': "$email",
                'value': "$value"
            }
        },
        {
            '$lookup':
                {
                    'from': "profileWH",
                    'localField': "email",
                    'foreignField': "email",
                    'as': "email_mapping_workspace"
                }
        },
        {'$set': {"cdpId": {'$first': "$email_mapping_workspace._id"}}},
        {'$unset': "email_mapping_workspace"},
        {'$merge': {
            'into': {'db': "dbMeasure", 'coll': "measureInsertOrderWH"}}}
    ]

    db_measure.rawOrder.aggregate(order_pipeline)
    return


db_measure.rawOrder.aggregate(
    [
        {
            '$project': {
                '_id': 0,
                'email': "$email",
                'value': "$value"
            }
        },
        {
            '$lookup':
                {
                    'from': "profileWH",
                    'localField': "email",
                    'foreignField': "email",
                    'as': "email_mapping_workspace"
                }
        },
        {'$set': {"cdpId": {'$first': "$email_mapping_workspace._id"}}},
        {'$unset': "email_mapping_workspace"},
        {'$merge': {
            'into': {'db': "dbMeasure", 'coll': "measureInsertOrderWH"}}}
    ]
)
