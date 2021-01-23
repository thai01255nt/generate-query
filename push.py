from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

db_measure = client.dbMeasure
# Load data
cursor = db_measure.rawProfile.find({})
raw_profile = []
for c in cursor:
    c.pop('_id')
    raw_profile.append(c)

raw_order = []
cursor = db_measure.rawOrder.find({})
for c in cursor:
    c.pop('_id')
    raw_order.append(c)

profile_wh = []
cursor = db_measure.profileWH.find({})
for c in cursor:
    c.pop('_id')
    profile_wh.append(c)

order_wh = []
cursor = db_measure.orderWH.find({})
for c in cursor:
    c.pop('_id')
    order_wh.append(c)


cloud = MongoClient("mongodb+srv://root:root_password@mongothai.mcbsw.mongodb.net/measure?retryWrites=true&w=majority")
cloud_measure = cloud.dbMeasure

try:
    cloud_measure.rawOrder.insert_many(raw_order)
except:
    pass
try:
    cloud_measure.orderWH.insert_many(order_wh)
except:
    pass
try:
    cloud_measure.profileWH.insert_many(profile_wh)
except:
    pass